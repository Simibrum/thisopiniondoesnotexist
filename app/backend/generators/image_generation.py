"""Functions to generate images from text."""

from app.backend.stability_api import ImageGenerator
from app.models import Image


def generate_image(text: str) -> Image:
    """Generate an image from the given text."""
    generator = ImageGenerator()
    image = generator.generate_image_binary(text)
    return image
