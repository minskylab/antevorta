from asyncio import run

from core.discover import perform_discovery
from core.output import RESTAdapter
from uvicorn import run as run_server
from api.api import app


def main():
    run_server(app=app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
