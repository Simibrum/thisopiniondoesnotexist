"""File to define the data models."""
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Image(Model):
    """Image data model."""
    # Primary key
    id = fields.IntField(pk=True)
    # Image name
    name = fields.CharField(max_length=255)
    # Image description
    description = fields.TextField()
    # Image data
    image = fields.BinaryField()
    # Image height
    height = fields.IntField()
    # Image width
    width = fields.IntField()
    # Image caption
    caption = fields.TextField()

    class Meta:
        """Meta class."""
        # default_connection = "main_db"
        table = "images"

    def __str__(self):
        return self.name


Image_Pydantic = pydantic_model_creator(Image, name="Image")
