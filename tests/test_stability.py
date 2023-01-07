"""Test the Twitter API functions."""

import pytest

from app.backend.stability_api import ImageGenerator


@pytest.fixture
def image_client():
    # Create an ImageGenerator object
    image_client = ImageGenerator()
    return image_client


def test_get_images(image_client):
    # Get a set of test images
    results = image_client.generate_images(
        "A test image with some testy things.", seed=11111, steps=15, samples=1, width=128, height=128
    )
    for img, seed in results:
        assert seed == 11111
        assert img
        assert img.mode == "RGB"
        assert img.size == (128, 128)
        assert img.format == "PNG"
        assert img.getpixel((0, 0)) != (0, 0, 0)
        img.show()


