from config.config import DIRECTUS_CREATE_RESOURCE_ENDPOINT, DIRECTUS_TOKEN
from .output import RESTAdapter


directus_adapter = RESTAdapter(
    endpoint=DIRECTUS_CREATE_RESOURCE_ENDPOINT,
    token=DIRECTUS_TOKEN,
    method="POST",
)
