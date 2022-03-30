from asyncio import gather
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import FastAPI, Header, Query
from loguru import logger
from pydantic import BaseModel
from api.semaphore import Semaphore
from config.config import ADMIN_SECRET, CONCURRENT_TASKS
from core.discover import perform_discovery
from core.types import AntevortaDiscovery
from core.directus import DirectusWebhookEvent, directus_adapter

app = FastAPI()


@Semaphore(CONCURRENT_TASKS)
async def discovery_task(url: str) -> AntevortaDiscovery | None:
    return await perform_discovery(url)


class PerformDiscoveryResult(BaseModel):
    compute_time_ms: float
    error: str | None
    discoveries: List[AntevortaDiscovery | None] | None


@app.get("/perform-discovery")
async def perform_discovery_endpoint(
    urls: List[str] | None = Query(None),
    admin_secret: str | None = Header(None),
) -> PerformDiscoveryResult:
    if ADMIN_SECRET != admin_secret:
        return PerformDiscoveryResult(
            compute_time_ms=0,
            error="Invalid admin token",
            discoveries=None,
        )

    now = datetime.now()
    match urls:
        case None:
            return PerformDiscoveryResult(
                # TODO: Function to get compute time isn't working yet
                compute_time_ms=(datetime.now() - now).microseconds / 1000,
                error="No URLs provided",
            )
        case urls:
            results = await gather(*[discovery_task(url) for url in urls])
            return PerformDiscoveryResult(
                compute_time_ms=(datetime.now() - now).microseconds / 1000,
                error=None,
                discoveries=results,
            )


@Semaphore(CONCURRENT_TASKS)
async def save_discovery(discovery: AntevortaDiscovery) -> AntevortaDiscovery | None:
    res = await directus_adapter.save(discovery)

    if res is None:
        return None

    discovery = AntevortaDiscovery(**(res["data"]))
    discovery.raw = None

    return discovery


class PerformDiscoveryInput(BaseModel):
    urls: List[str]


@app.post("/perform-discovery")
async def perform_discovery_post(
    input: PerformDiscoveryInput,
    admin_secret: str | None = Header(None),
) -> PerformDiscoveryResult:
    if ADMIN_SECRET != admin_secret:
        return PerformDiscoveryResult(
            compute_time_ms=0,
            error="Invalid admin token",
            discoveries=None,
        )

    now = datetime.now()

    results = await perform_discovery_endpoint(input.urls, admin_secret)

    match results:
        case PerformDiscoveryResult(error=None, discoveries=None):
            return results
        case PerformDiscoveryResult(error=error, discoveries=None):
            logger.error(f"Error performing discovery: {error}")
            return results
        case PerformDiscoveryResult(error=None, discoveries=[*discoveries]):
            discoveries = await gather(*[save_discovery(discovery) for discovery in discoveries if discovery is not None])
            return PerformDiscoveryResult(
                compute_time_ms=(datetime.now() - now).microseconds / 1000,
                error=None,
                discoveries=discoveries,
            )

    return results


# Next endpoint is very specific to the Directus API
@app.post("/aggregation-webhook")
async def aggregation_webhook(
    event: DirectusWebhookEvent,
    admin_secret: str | None = Header(None),
) -> None:
    if ADMIN_SECRET != admin_secret:
        return None

    discovery: AntevortaDiscovery | None = None
    revision: int | None = None

    match event:
        case DirectusWebhookEvent(event="items.create", key=id, payload=AntevortaDiscovery(url=url)):
            discovery = await discovery_task(url)

        case DirectusWebhookEvent(event="items.update", key=id, payload=AntevortaDiscovery(url=url, revision=rev, updated_at=updated_at)):
            discovery = await discovery_task(url)
            revision = rev
            if updated_at is not None and datetime.now() - updated_at < timedelta(seconds=10):
                return None

    if discovery is None:
        return None

    discovery.id = id
    discovery.revision = 1 if revision is None else revision + 1

    await directus_adapter.update(discovery)

    return None
