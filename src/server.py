import asyncio
from pathlib import Path

from aiohttp import web
from dotenv import dotenv_values

from views.pages import setup_pages_routes

BASE_DIR = Path(__file__).resolve().parent.parent

config = dotenv_values(BASE_DIR / ".env")

async def init():
    app = web.Application()
    setup_pages_routes(app)
    host = config.get("SERVER_HOST", "127.0.0.1")
    port = config.get("SERVER_PORT", 8000)
    return app, host, port


def main():
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init())
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()
