"""File to create database schema."""
# See https://medium.com/nerd-for-tech/python-tortoise-orm-integration-with-fastapi-c3751d248ce1
from tortoise import Tortoise
from app.db.connect_db import connect_to_db


async def init():
    await connect_to_db()
    await Tortoise.generate_schemas()

