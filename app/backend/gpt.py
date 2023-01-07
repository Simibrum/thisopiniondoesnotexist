"""Functions based on OpenAI's GPT-3 API."""

import os
import openai
from app.utils import load_env_vars

# Load environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Get the grandparent directory of the current file's directory
    grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    # Get the path to the .env file
    env_path = os.path.join(grandparent_dir, ".env")
    load_env_vars(env_path)
    API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
if not API_KEY:
    raise ValueError("Missing OpenAI API key.")


class TextGenerator:
    def __init__(self, model="text-davinci-003"):
        """Initialize the Completion class with the specified model engine."""
        self.model = model

    def complete(self, prompt, max_tokens=1024, temperature=0.5):
        """Generate a completion for the given prompt."""
        prompt = (f"{prompt}")
        completions = openai.Completion.create(
            model=self.model, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
        message = completions.choices[0].text
        return message
