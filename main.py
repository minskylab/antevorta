from asyncio import run
from core.discover import extract_meta_tags_open_graph


url = "https://flowcv.io/"


async def main():
    metatags = await extract_meta_tags_open_graph(url)

    print(metatags)

if __name__ == "__main__":
    run(main())
