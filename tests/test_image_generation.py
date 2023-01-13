"""Test image generation functions"""
from app.backend.generators.image_generation import generate_image


TEST_TEXT = """\
A photo of Gloria Steinem, an iconic American feminist and political activist. She is 85 years old with white hair 
and glasses. She is wearing a black blazer and a white shirt. She is smiling, looking directly at the camera, 
her hands clasped in front of her. Her expression is determined and confident. She is an influential voice for 
gender equality and human rights."""


def test_generate_image():
    image = generate_image(TEST_TEXT)
    assert image
