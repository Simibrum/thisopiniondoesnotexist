"""Specify the Tortoise Configuration.

See here - https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/
"""

from app.db import DB_URL, MODEL_MODULE


TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": [
                MODEL_MODULE, "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}
