"""Functions to generate images from text."""
from typing import Optional, Tuple
from app.backend.stability_api import ImageGenerator
from app.backend.gpt import TextGenerator
from app.utils import get_alt_text
from app.logger import logger

article_image_generator_prompt = f"""\
{{}}
Given the article plan above, generate an 50-word alt-text specification for a lead image and a body text image from a \
stock photo library to accompany the article. Use very short note-like phrases and single terms. Add specific \
properties of the photo of the photo, such as location, quality and photography terms. Of the form below. \
Make both images different.

Lead image [alt text]:

Body image [alt text]:
"""


def generate_image(text: str) -> Optional[bytes]:
    """Generate an image from the given text."""
    logger.debug(f"Generating image from text: {text}")
    generator = ImageGenerator()
    image = generator.generate_image_binary(text)
    return image


def generate_article_images(plan: str) -> Optional[Tuple[Tuple[str, bytes], Tuple[str, bytes]]]:
    """Generate two images for an article.

    Returns a tuple of tuples with the alt text and image bytes."""
    # Populate the prompt with the article plan
    logger.info("Generating alt text based on article plan...")
    prompt = article_image_generator_prompt.format(plan)
    logger.debug(f"Alt text Generation Prompt: {prompt}")
    # Use the text generator to generate the alt text
    text_generator = TextGenerator()
    alt_text = text_generator.complete(prompt, max_tokens=512, temperature=0.5)
    logger.info("Generated alt text based on article plan")
    logger.debug(f"Alt text: {alt_text}")
    # Split the alt text into two parts
    lead_image_alt_text, body_image_alt_text = get_alt_text(alt_text)
    logger.debug(f"Lead image alt text: {lead_image_alt_text}")
    logger.debug(f"Body image alt text: {body_image_alt_text}")
    if lead_image_alt_text:
        lead_image = generate_image(lead_image_alt_text)
    else:
        lead_image = None
    if body_image_alt_text:
        body_image = generate_image(body_image_alt_text)
    else:
        body_image = None
    return (lead_image_alt_text, lead_image), (body_image_alt_text, body_image)
