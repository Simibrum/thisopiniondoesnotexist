# See: https://stackoverflow.com/questions/65716897/testing-in-fastapi-using-tortoise-orm

import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from app import app
from app.db import MODEL_MODULE

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": [MODEL_MODULE]}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url}")
    if schemas:
        await Tortoise.generate_schemas()
        print("Successfully generated schemas")


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    await init()
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Client is ready")
        yield client
    await Tortoise.close_connections()



