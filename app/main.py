from app import app
from app.db import DB_URL, MODEL_MODULE
from tortoise.contrib.fastapi import register_tortoise

# Initialise models
# Tortoise.init_models(["app.models"], "models")
# Configure tortoise-orm to use the app's DB config
register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": [MODEL_MODULE]},
    generate_schemas=True,  # Creates the tables if they do not exist
    add_exception_handlers=True,
)
