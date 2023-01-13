
from unittest.mock import patch
import pytest
from app import app
from app.models import Author
from fastapi.testclient import TestClient

from app.backend.generators.author_generation import generate_authors, initial_stats_prompt, generate_bio, \
    bio_generator_prompt, generate_photo_desc, photo_description_generator_prompt, populate_authors


@patch("app.backend.gpt.TextGenerator.complete")
def test_generate_authors(mock_complete):
    # Set up mock return value for the complete method
    mock_complete.return_value = (
        "| John | 25 | Male |\n"
        "| Jane | 30 | Female |\n"
        "| Jack | 35 | Male |\n"
    )

    # Call the generate_authors function with num_authors=3
    result = generate_authors(num_authors=3)

    # Assert that the result is a list of tuples with the correct values
    assert result == [
        ("John", 25, "Male"),
        ("Jane", 30, "Female"),
        ("Jack", 35, "Male"),
    ]

    # Assert that the complete method was called with the correct arguments
    mock_complete.assert_called_once_with(
        initial_stats_prompt.format(3), max_tokens=512,
    )


@patch("app.backend.gpt.TextGenerator.complete")
def test_generate_bio(mock_complete):
    # Set up mock return value for the complete method
    mock_complete.return_value = "John is a 25 year old Male. He enjoys reading and playing sports."

    # Define the author
    author = ("John", 25, "Male")
    # Call the generate_bio function
    result = generate_bio(*author)

    # Assert that the result is a string with the correct value
    assert result == "John is a 25 year old Male. He enjoys reading and playing sports."

    # Assert that the complete method was called with the correct arguments
    mock_complete.assert_called_once_with(
        bio_generator_prompt.format(*author), max_tokens=512,
    )


@patch("app.backend.gpt.TextGenerator.complete")
def test_generate_photo_desc(mock_complete):
    # Set up mock return value for the complete method
    mock_complete.return_value = "This is a mock photo description."

    # Define the author
    author = ("John", 25, "Male")
    # Call the generate_bio function
    result = generate_photo_desc(*author)

    # Assert that the result is a string with the correct value
    assert result == "This is a mock photo description."

    # Assert that the complete method was called with the correct arguments
    mock_complete.assert_called_once_with(
        photo_description_generator_prompt.format(*author), max_tokens=512,
    )


client = TestClient(app)


@pytest.mark.anyio
@patch("app.backend.gpt.TextGenerator.complete")
async def test_author_batch(mock_complete, in_memory_db):
    """Test creating a batch of authors."""
    mock_complete.return_value = "| Test | 35 | TestGender |\n"*10
    await populate_authors(num_authors=10)
    authors = await Author.all()
    assert len(authors) == 10
    for author in authors:
        assert author.name == "Test"
        assert author.age == 35
        assert author.gender == "TestGender"
        assert author.bio == mock_complete.return_value
        assert author.photo_description == mock_complete.return_value
