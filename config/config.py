from decouple import config

HOST: str = config("HOST", default="0.0.0.0", cast=str)
PORT: int = config("PORT", default=8080, cast=int)

CONCURRENT_TASKS: int = config('CONCURRENT_TASKS', default=50, cast=int)
ADMIN_SECRET: str | None = config('ADMIN_SECRET', default=None)
DIRECTUS_CREATE_RESOURCE_ENDPOINT: str = config("DIRECTUS_CREATE_RESOURCE_ENDPOINT", cast=str)
DIRECTUS_TOKEN: str = config("DIRECTUS_TOKEN", cast=str)
