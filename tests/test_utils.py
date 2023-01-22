import os
import tempfile
import pytest

from app.utils import load_env_vars, get_alt_text, filter_out_football


def test_load_env_vars(monkeypatch):
    # Create a temporary .env file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env") as f:
        # Write some environment variables to the file
        f.write("API_KEY=1234567890\n")
        f.write("API_SECRET_KEY=abcdefghijklmnopqrstuvwxyz\n")
        f.write("ACCESS_TOKEN=0987654321\n")
        f.write("ACCESS_TOKEN_SECRET=zyxwvutsrqponmlkjihgfedcba\n")

        # Flush the file to disk
        f.flush()

        # Load the environment variables from the .env file
        load_env_vars(f.name)

        # Assert that the environment variables have been set
        assert os.getenv("API_KEY") == "1234567890"
        assert os.getenv("API_SECRET_KEY") == "abcdefghijklmnopqrstuvwxyz"
        assert os.getenv("ACCESS_TOKEN") == "0987654321"
        assert os.getenv("ACCESS_TOKEN_SECRET") == "zyxwvutsrqponmlkjihgfedcba"


def test_get_alt_text():
    test_string = """\
    Lead image [alt text]: Female athlete in action, mid-air, against blue sky background. \
    High-quality image, vibrant colors, dynamic composition.\

    Body image [alt text]: Group of female athletes celebrating victory, embracing each other. \
    Outdoor setting, warm lighting, smiling faces.\
    """
    text = get_alt_text(test_string)
    assert len(text) == 2
    assert text[0] == """Female athlete in action, mid-air, against blue sky background. \
    High-quality image, vibrant colors, dynamic composition."""
    assert text[1] == """Group of female athletes celebrating victory, embracing each other. \
    Outdoor setting, warm lighting, smiling faces."""


def test_filter_out_football():
    topic_sets = [
        ["Michelle Williams", "RB Leipzig vs Bayern", "Dani Alves"],
        ["Expected", "Leeds United vs Cardiff City", "Kilmarnock vs Rangers"],
        ["Wolves vs Liverpool", "Australian Open", "the Teachers Strike"],
        ["Chelsea fc", "Michelle Heaton", "Teachers strike"]
    ]
    filtered_topic_sets = [filter_out_football(ts)  for ts in topic_sets]
    assert filtered_topic_sets[0] == ["Michelle Williams", "Dani Alves"]
    assert filtered_topic_sets[1] == ["Expected"]
    assert filtered_topic_sets[2] == ["Australian Open", "the Teachers Strike"]
    assert filtered_topic_sets[3] == ["Michelle Heaton", "Teachers strike"]
