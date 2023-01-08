"""File to test the various models."""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from tortoise.exceptions import DoesNotExist
from app.models import Post, Image, Trends, Author
from app import app


client = TestClient(app)


@pytest.mark.anyio
async def test_author_model(in_memory_db):
    """Test the author model."""
    # Create a new author
    author = await Author.create(
        name="Jane Austen",
        age=35,
        gender="Female",
        bio="Jane Austen was an English novelist known for her six major novels.",
        photo_description="A portrait of Jane Austen"
    )
    await author.save()

    # Test that the author was saved to the database
    retrieved_author = await Author.get(id=author.id)
    assert retrieved_author.name == "Jane Austen"
    assert retrieved_author.age == 35
    assert retrieved_author.gender == "Female"
    assert retrieved_author.bio == "Jane Austen was an English novelist known for her six major novels."
    assert retrieved_author.photo_description == "A portrait of Jane Austen"

    # Test updating the author
    retrieved_author.name = "Jane Austen2"
    retrieved_author.age = 36
    retrieved_author.gender = "Female"
    retrieved_author.bio = "Jane Austen was an English novelist known for her six major novels."
    retrieved_author.photo_description = "A portrait of Jane Austen"
    await retrieved_author.save()

    # Test that the update was saved to the database
    updated_author = await Author.get(id=author.id)
    assert updated_author.name == "Jane Austen2"
    assert updated_author.age == 36
    assert updated_author.gender == "Female"
    assert updated_author.bio == "Jane Austen was an English novelist known for her six major novels."
    assert updated_author.photo_description == "A portrait of Jane Austen"

    # Test deleting the author
    await retrieved_author.delete()

    # Test that the author was deleted from the database
    with pytest.raises(DoesNotExist):
        await Author.get(id=author.id)
