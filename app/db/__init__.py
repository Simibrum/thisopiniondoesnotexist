# Set DB URL
import os

DB_URL = os.getenv('DB_URL', 'sqlite://app/db/data/db.sqlite3')
MODEL_MODULE = 'app.models.data_models'
