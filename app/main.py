from app import app
from app.db import DB_URL, MODEL_MODULE
from app.db.config import TORTOISE_ORM
from app.db.register import register_tortoise

# Initialise models
# Tortoise.init_models(["app.models"], "models")
# Configure tortoise-orm to use the app's DB config
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False  # Creates the tables if they do not exist
)
