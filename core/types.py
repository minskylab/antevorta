

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


Metatags = Dict[str, str | None]


@dataclass
class AntevortaDiscovery:
    url: str
    url_title: Optional[str]
    url_description: Optional[str]
    og_title: Optional[str]
    og_type: Optional[str]
    og_url: Optional[str]
    og_description: Optional[str]
    og_image: Optional[str]
    keytrigrams: Dict[str, float]
    keyphrase: Optional[str]
    keyword: Optional[str]


class AntevortaDiscoveryStatus(Enum):
    UNKNOWN = 0
    DISCOVERED = 1
    DISCOVERED_AND_CACHED = 2
