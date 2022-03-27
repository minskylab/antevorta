from asyncio import run

from core.discover import perform_discovery
from core.output import RESTAdapter


url = "https://flowcv.io/"


async def main():

    discovery = await perform_discovery(url)
    print(discovery)

    adapter = RESTAdapter(endpoint="http")
    await adapter.save(discovery)

if __name__ == "__main__":
    run(main())
