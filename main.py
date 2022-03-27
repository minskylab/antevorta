from uvicorn import run as run_server
from api.api import app
from config.config import HOST, PORT


def main():
    run_server(app=app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
