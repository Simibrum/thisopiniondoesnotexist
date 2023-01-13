"""File to define the data models."""
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Trends(Model):
    """Author data model."""
    # Primary key
    id = fields.IntField(pk=True)
    # Trends date
    date = fields.DatetimeField()
    # Trends list (strings)
    trends = fields.JSONField()
    # Trends source
    source = fields.CharField(max_length=255)
    # Trends location
    location = fields.CharField(max_length=255)

    class Meta:
        """Meta class."""
        # default_connection = "main_db"
        table = "trends"

    def __str__(self):
        return self.trends


Trends_Pydantic = pydantic_model_creator(Trends, name="Trends")
