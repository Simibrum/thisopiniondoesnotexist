"""Code to set up a Twitter API wrapper and get the trends."""
import os
import base64
import requests
from app.utils import load_env_vars


def get_settings():
    # Set up your API credentials from environment variables
    api_key = os.environ.get("TWITTER_KEY")
    api_secret_key = os.environ.get("TWITTER_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_TOKEN_SECRET")
    return api_key, api_secret_key, access_token, access_token_secret


# Get the settings
API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_settings()

# If the environment variables are not set, load them from a file
if not (API_KEY and API_SECRET_KEY and ACCESS_TOKEN and ACCESS_TOKEN_SECRET):
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Get the grandparent directory of the current file's directory
    grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    # Get the path to the .env file
    env_path = os.path.join(grandparent_dir, ".env")
    load_env_vars(env_path)
    API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_settings()


class TwitterTrends:
    def __init__(self, api_key, api_secret_key, access_token, access_token_secret):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        if not (self.api_key and self.api_secret_key and self.access_token and self.access_token_secret):
            raise ValueError("Missing Twitter API credentials.")

        # Set up the Bearer Token
        bearer_token = f"{self.api_key}:{self.api_secret_key}"
        bearer_token = base64.b64encode(bearer_token.encode()).decode()

        # Request a Bearer Token
        response = requests.post(
            "https://api.twitter.com/oauth2/token",
            headers={
                "Authorization": f"Basic {bearer_token}",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            },
            data={"grant_type": "client_credentials"},
        )

        # Extract the Bearer Token from the response
        self.bearer_token = response.json()["access_token"]

        # Set up the headers for subsequent requests
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
        }

    def get_trending_topics(self, location):
        # Set the location parameter
        location = location

        # Get the trend locations
        response = requests.get(
            "https://api.twitter.com/1.1/trends/available.json", params={"q": location}, headers=self.headers,
        )
        print(response.json())
        # Extract the WOEID for the location
        location_id = response.json()[0]["woeid"]

        # Get the trending topics for the location
        response = requests.get(
            "https://api.twitter.com/1.1/trends/place.json",
            params={"id": location_id},
            headers=self.headers,
        )

        # Extract the trending topics
        trends = response.json()[0]["trends"]

        # Return the trending topics as a list of strings
        return [trend["name"] for trend in trends]

