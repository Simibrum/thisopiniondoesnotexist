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




response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Write a top-level outline in 250 words for an opinion article that combines the following topics: 'Greta Thunberg', 'Liverpool', 'Pope', 'West Ham vs Brentford', 'Happy New Year 2023'. Try to link the topics.\n\nHappy New Year 2023: Reflections on a Year of Unprecedented Change\n\nIntroduction:\n\n• A quick overview of the events of the past year and how they have impacted the world, from Greta Thunberg to the Pope to the football match between West Ham and Brentford\n\n• The need for reflection on these events and the changes they have brought about\n\nBody:\n\n• Greta Thunberg: An examination of the impact Greta has had in the past year and how her presence has brought about unprecedented change in the world\n\n• Liverpool: How the success of Liverpool in the past year has been a source of hope and inspiration for many\n\n• Pope: How the Pope has been an advocate for change and progress in the past year\n\n• West Ham vs Brentford: An exploration of the significance of this match and how it has been a source of inspiration and hope for many\n\n• Happy New Year 2023: Reflections on how the past year has been a period of unprecedented change and how we should all look towards the future with hope and optimism\n\nConclusion:\n\n• A final reflection on the past year and the need to look towards the future with optimism and hope",
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)