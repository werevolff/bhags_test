import asyncio
from pathlib import Path

from dotenv import dotenv_values
from peewee_async import Manager, PostgresqlDatabase

__all__ = ["database", "objects"]

BASE_DIR = Path(__file__).resolve().parent.parent.parent

config = dotenv_values(BASE_DIR / ".env")

loop = asyncio.get_event_loop()
database = PostgresqlDatabase(
    config.get("DATABASE_NAME"),
    user=config.get("DATABASE_USER"),
    password=config.get("DATABASE_PASSWORD"),
    host=config.get("DATABASE_HOST", "127.0.0.1"),
    port=config.get("DATABASE_PORT", 5432),
)
objects = Manager(database, loop=loop)
