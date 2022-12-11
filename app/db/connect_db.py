"""Connection to database."""
from tortoise import Tortoise
from app.db import DB_URL, MODEL_MODULE


async def connect_to_db():
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': [MODEL_MODULE]}
    )
