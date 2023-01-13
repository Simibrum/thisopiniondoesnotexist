"""Backend functions for DreamStudio."""

import os
import io
import warnings
import random
from PIL import Image
from typing import Optional
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from app.utils import load_env_vars

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Get API key from environment variable
STABILITY_KEY = os.environ.get('STABILITY_KEY')
if not STABILITY_KEY:
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Get the grandparent directory of the current file's directory
    grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    # Get the path to the .env file
    env_path = os.path.join(grandparent_dir, ".env")
    load_env_vars(env_path)
    STABILITY_KEY = os.environ.get('STABILITY_KEY')


class ImageGenerator:
    def __init__(self, api_key=STABILITY_KEY):
        """Initialize the ImageGenerator class with the specified API key."""
        # Set up our connection to the API.
        self.client = client.StabilityInference(
            key=api_key,  # API Key reference.
            verbose=True,  # Print debug messages.
            engine="stable-diffusion-512-v2-1",  # Set the engine to use for generation.
        )
        # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0
        # stable-diffusion-768-v2-0 stable-diffusion-512-v2-1 stable-diffusion-768-v2-1
        # stable-inpainting-v1-0 stable-inpainting-512-v2-0

    def generate_images(self, prompt, seed=None, steps=30, cfg_scale=8.0, width=512, height=512, samples=1,
                        sampler=generation.SAMPLER_K_DPMPP_2M):
        """Generate images for the given prompt."""
        seed = random.randint(0, 2 ** 32 - 1) if seed is None else seed
        # Set up our initial generation parameters.
        answers = self.client.generate(
            prompt=prompt,
            seed=seed,  # If a seed is provided, the resulting generated image will be deterministic.
            steps=steps,  # Amount of inference steps performed on image generation.
            cfg_scale=cfg_scale,  # Influences how strongly your generation is guided to match your prompt.
            width=width,  # Generation width
            height=height,  # Generation height
            samples=samples,  # Number of images to generate
            sampler=sampler  # Choose which sampler we want to denoise our generation with.
        )

        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, return generated images and seeds.
        results = list()
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    # Add generated image and seed to results list
                    results.append((img, artifact.seed))
        return results

    def generate_image_binary(self, prompt: str, width: int = 512, height: int = 512) -> Optional[bytes]:
        """Get an image from a prompt and return the image binary."""
        # Set up our initial generation parameters.
        answers = self.client.generate(
            prompt=prompt,
            width=width,  # Generation width
            height=height  # Generation height
        )
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    return artifact.binary
        return None

