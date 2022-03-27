from config.config import DIRECTUS_CREATE_RESOURCE_ENDPOINT
from .output import RESTAdapter


directus_adapter = RESTAdapter(
    endpoint=DIRECTUS_CREATE_RESOURCE_ENDPOINT,
    method="POST",
)
