"""File to define the data models."""
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Post(Model):
    """Post data model."""
    # Primary key
    id = fields.IntField(pk=True)
    # Store date of post as day-month-year integers (DD-MM-YYYY)
    day = fields.IntField()
    month = fields.IntField()
    year = fields.IntField()
    # Post plan
    plan = fields.TextField(null=True)
    # Post data
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    published = fields.BooleanField(default=False)
    author = fields.ForeignKeyField("models.Author", related_name="posts")
    lead_image = fields.ForeignKeyField("models.Image", related_name="lead_image", null=True)
    body_image = fields.ForeignKeyField("models.Image", related_name="body_image", null=True)

    class Meta:
        """Meta class."""
        # default_connection = "main_db"
        table = "posts"

    def __str__(self):
        return self.title


Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)
