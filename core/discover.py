from aiohttp import ClientSession
from typing import Dict
from bs4 import BeautifulSoup

from yake import KeywordExtractor

from core.types import AntevortaDiscovery, Metatags


async def extract_meta_tags_open_graph(url: str) -> Metatags | None:
    metatags: Metatags = {}
    try:
        async with ClientSession() as session:
            async with session.get(url) as res:
                content = await res.text()
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find("title")
                description = soup.find("meta", attrs={"name": "description"})

                og_title = soup.find("meta", property="og:title")
                og_type = soup.find("meta", property="og:type")
                og_url = soup.find("meta", property="og:url")
                og_description = soup.find("meta", property="og:description")
                og_image = soup.find("meta", property="og:image")

                metatags["title"] = title.text.strip() if title else None
                metatags["description"] = description["content"] if description else None

                metatags["og_title"] = og_title["content"] if og_title else None
                metatags["og_type"] = og_type["content"] if og_type else None
                metatags["og_url"] = og_url["content"] if og_url else None
                metatags["og_description"] = og_description["content"] if og_description else None
                metatags["og_image"] = og_image["content"] if og_image else None
    except Exception as e:
        print(e)
        return None
    return metatags


async def perform_discovery(url: str) -> AntevortaDiscovery | None:
    keyphrases_extractor = KeywordExtractor(top=6, n=6, stopwords=None)
    keywords_extractor = KeywordExtractor(top=6, n=1, stopwords=None)
    keytrigrams_extractor = KeywordExtractor(top=6, n=3, stopwords=None)

    metatags = await extract_meta_tags_open_graph(url)

    if metatags is None:
        return None

    title = (metatags["og_title"] or metatags["title"] or "")
    description = (metatags["og_description"] or metatags["description"] or "")

    full_text = title + " " + description

    keytrigrams = keytrigrams_extractor.extract_keywords(full_text)

    keyphrases = keyphrases_extractor.extract_keywords(full_text)
    keyphrase = keyphrases[0][0] if len(keyphrases) > 0 else ""

    keywords = keywords_extractor.extract_keywords(full_text)
    keyword = keywords[0][0] if len(keywords) > 0 else ""

    return AntevortaDiscovery(
        url=url,
        url_title=metatags["title"],
        url_description=metatags["description"],
        og_title=metatags["og_title"],
        og_type=metatags["og_type"],
        og_url=metatags["og_url"],
        og_description=metatags["og_description"],
        og_image=metatags["og_image"],
        keytrigrams=keytrigrams,
        keyphrase=keyphrase,
        keyword=keyword,
    )
