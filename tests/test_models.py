"""File to test the various models."""

import pytest
from fastapi.testclient import TestClient
from tortoise.exceptions import DoesNotExist
from datetime import date, datetime, timezone
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


@pytest.mark.anyio
async def test_post_model(in_memory_db):
    """Test the post model."""
    # Create a new author
    author = await Author.create(
        name="Jane Austen",
        age=35,
        gender="Female",
        bio="Jane Austen was an English novelist known for her six major novels.",
        photo_description="A portrait of Jane Austen"
    )
    await author.save()
    # Create a new post
    post = await Post.create(
        day=date.today().day,
        month=date.today().month,
        year=date.today().year,
        title="Hello World",
        content="This is a test post.",
        published=True,
        author=author
    )
    await post.save()

    # Test that the post was saved to the database
    retrieved_post = await Post.get(id=post.id)
    assert retrieved_post.day == date.today().day
    assert retrieved_post.month == date.today().month
    assert retrieved_post.year == date.today().year
    assert retrieved_post.title == "Hello World"
    assert retrieved_post.content == "This is a test post."
    assert retrieved_post.published == True

    # Test updating the post
    retrieved_post.title = "Hello World 2"
    retrieved_post.content = "This is an updated test post."
    retrieved_post.published = False
    await retrieved_post.save()

    # Test that the update was saved to the database
    updated_post = await Post.get(id=post.id)
    assert updated_post.title == "Hello World 2"
    assert updated_post.content == "This is an updated test post."
    assert not updated_post.published

    # Test deleting the post
    await retrieved_post.delete()

    # Test that the post was deleted from the database
    with pytest.raises(DoesNotExist):
        await Post.get(id=post.id)


@pytest.mark.anyio
async def test_trends_model(in_memory_db):
    """Test the trends model."""
    date_now = datetime.now()
    # Create a new trends entry
    trends = await Trends.create(
        date=date_now,
        trends=["trend 1", "trend 2", "trend 3"],
        source="Twitter",
        location="USA"
    )
    await trends.save()

    # Test that the trends entry was saved to the database
    retrieved_trends = await Trends.get(id=trends.id)
    assert retrieved_trends.date.astimezone(timezone.utc) == date_now.astimezone(timezone.utc)
    assert retrieved_trends.trends == ["trend 1", "trend 2", "trend 3"]
    assert retrieved_trends.source == "Twitter"
    assert retrieved_trends.location == "USA"

    # Test updating the trends entry
    retrieved_trends.trends = ["trend 4", "trend 5"]
    retrieved_trends.source = "Google"
    retrieved_trends.location = "UK"
    await retrieved_trends.save()

    # Test that the update was saved to the database
    updated_trends = await Trends.get(id=trends.id)
    assert updated_trends.trends == ["trend 4", "trend 5"]
    assert updated_trends.source == "Google"
    assert updated_trends.location == "UK"

    # Test deleting the trends entry
    await retrieved_trends.delete()

    # Test that the trends entry was deleted from the database
    with pytest.raises(DoesNotExist):
        await Trends.get(id=trends.id)


@pytest.mark.anyio
async def test_image_model(in_memory_db):
    # Create a new image
    image = await Image.create(
        name="test_image.png",
        description="This is a test image.",
        image=b"binary image data",
        height=300,
        width=400,
        caption="Test image caption."
    )
    await image.save()

    # Test that the image was saved to the database
    retrieved_image = await Image.get(id=image.id)
    assert retrieved_image.name == "test_image.png"
    assert retrieved_image.description == "This is a test image."
    assert retrieved_image.image == b"binary image data"
    assert retrieved_image.height == 300
    assert retrieved_image.width == 400
    assert retrieved_image.caption == "Test image caption."

    # Test updating the image
    retrieved_image.description = "This is an updated test image."
    retrieved_image.image = b"updated binary image data"
    retrieved_image.height = 200
    retrieved_image.width = 300
    retrieved_image.caption = "Updated test image caption."
    await retrieved_image.save()

    # Test that the update was saved to the database
    updated_image = await Image.get(id=image.id)
    assert updated_image.description == "This is an updated test image."
    assert updated_image.image == b"updated binary image data"
    assert updated_image.height == 200
    assert updated_image.width == 300
    assert updated_image.caption == "Updated test image caption."

    # Test deleting the image
    await retrieved_image.delete()

    # Test that the image was deleted from the database
    with pytest.raises(DoesNotExist):
        await Image.get(id=image.id)
