"""Pydantic data models for the app."""
from typing import Optional
from pydantic import BaseModel


class Post(BaseModel):
    """Post data model."""
    title: str
    content: str
    published: Optional[bool]
