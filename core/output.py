

from abc import ABC, abstractmethod
from typing import Any, Dict, Literal

from aiohttp import ClientSession
from core.types import AntevortaDiscovery


class AntevortaOutputAdapter(ABC):
    @abstractmethod
    async def save(self, discovery: AntevortaDiscovery) -> Dict | None:
        pass


RESTMethod = Literal["POST", "GET"]


class RESTAdapter(AntevortaOutputAdapter):
    def __init__(self, endpoint: str, token: str | None = None, method: RESTMethod = "POST", remmaping: Dict[str, str] = {}) -> None:
        super().__init__()
        self.endpoint = endpoint
        self.method = method
        self.remmaping = remmaping
        self.token = token

    async def save(self, discovery: AntevortaDiscovery) -> Dict | None:
        payload = discovery.dict()

        # if len(self.remmaping) > 0:
        #     for last_key, new_key in self.remmaping.items():
        #         payload[new_key] = payload.pop(last_key)
        # logger.info(payload)

        # TODO: Implement better remapping of keys

        data: Any | None = None

        async with ClientSession() as session:
            match self.method:
                case "POST":
                    async with session.post(self.endpoint, headers={
                        "Authorization": f"Bearer {self.token}",
                    }, json=payload) as res:
                        data = await res.json()
                case "GET":
                    async with session.get(self.endpoint, headers={
                        "Authorization": f"Bearer {self.token}",
                    }, json=payload) as res:
                        data = await res.json()

        return data
