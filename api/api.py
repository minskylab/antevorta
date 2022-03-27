from asyncio import gather
from datetime import datetime
from typing import List
from fastapi import FastAPI, Query
from pydantic import BaseModel
from api.semaphore import Semaphore
from core.discover import perform_discovery
from core.types import AntevortaDiscovery, AntevortaDiscoveryStatus
from core.output_directus import directus_adapter

app = FastAPI()

CONCURRENT_TASKS = 10


@Semaphore(CONCURRENT_TASKS)
async def discovery_task(url: str):
    return await perform_discovery(url)


class PerformDiscoveryResult(BaseModel):
    compute_time_ms: float
    error: str | None
    discoveries: List[AntevortaDiscovery | None] | None


@app.get("/perform-discovery")
async def perform_discovery_endpoint(urls: List[str] | None = Query(None)) -> PerformDiscoveryResult:
    now = datetime.now()
    match urls:
        case None:
            return PerformDiscoveryResult(
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
async def save_discovery(discovery: AntevortaDiscovery) -> AntevortaDiscoveryStatus:
    return await directus_adapter.save(discovery)


class PerformDiscoveryInput(BaseModel):
    urls: List[str]


@app.post("/perform-discovery")
async def perform_discovery_post(input: PerformDiscoveryInput) -> PerformDiscoveryResult:
    results = await perform_discovery_endpoint(input.urls)

    match results:
        case PerformDiscoveryResult(error=None, discoveries=None):
            return results
        case PerformDiscoveryResult(error=error, discoveries=None):
            return results
        case PerformDiscoveryResult(error=None, discoveries=[*discoveries]):
            await gather(*[save_discovery(discovery) for discovery in discoveries if discovery is not None])
            return results

    return results
