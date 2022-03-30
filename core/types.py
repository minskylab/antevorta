

from typing import Dict
from datetime import datetime
from pydantic import BaseModel


Metatags = Dict[str, str | None]


class AntevortaDiscoveryRaw(BaseModel):
    html: str | None
    # html_text: str | None
    # headers: Dict[str, str] | None


class AntevortaDiscovery(BaseModel):
    id: str | None
    url: str
    url_title: str | None
    url_description: str | None
    og_title: str | None
    og_type: str | None
    og_url: str | None
    og_description: str | None
    og_image: str | None
    keytrigrams: Dict[str, float] | Dict | str | None
    keyphrase: str | None
    keyword: str | None
    page_text: str | None

    raw: AntevortaDiscoveryRaw | None

    revision: int | None
    created_at: datetime | None
    updated_at: datetime | None


# class AntevortaDiscoveryStatus(Enum):
#     UNKNOWN = 0
#     DISCOVERED = 1
#     DISCOVERED_AND_CACHED = 2
