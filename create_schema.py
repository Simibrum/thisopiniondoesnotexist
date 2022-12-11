"""Script to create DB schema."""
from tortoise import run_async
from app.db.init_db import init


if __name__ == '__main__':
    run_async(init())
