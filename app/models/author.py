"""File to define the data models."""
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Author(Model):
    """Author data model."""
    # Primary key
    id = fields.IntField(pk=True)
    # Author name
    name = fields.CharField(max_length=255)
    # Author age
    age = fields.IntField()
    # Author gender
    gender = fields.CharField(max_length=255)
    # Author bio
    bio = fields.TextField()
    # Author photo description
    photo_description = fields.TextField()
    # Author photo linked record
    photo = fields.ForeignKeyField("models.Image", null=True)

    class Meta:
        """Meta class."""
        # default_connection = "main_db"
        table = "authors"

    def __str__(self):
        return self.name


Author_Pydantic = pydantic_model_creator(Author, name="Author", exclude=("image",))
