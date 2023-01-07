"""File for Google BiqQuery API access."""
import os

from google.cloud import bigquery
from google.oauth2 import service_account
from app.utils import load_env_vars

KEY_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if not KEY_PATH:
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Get the grandparent directory of the current file's directory
    grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    # Get the path to the .env file
    env_path = os.path.join(grandparent_dir, ".env")
    load_env_vars(env_path)
    KEY_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


# Query the Google Trends dataset and get the top 5 trending topics for the last 7 days
TREND_QUERY = """
    -- This query shows a list of the daily top Google Search terms for the UK.
    SELECT
       refresh_date AS Day,
       term AS Top_Terms,
       rank,
    FROM `bigquery-public-data.google_trends.international_top_terms`
    WHERE
       country_code = "GB"
       AND rank <= 10
           -- Choose only the top term each day.
       AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 WEEK)
           -- Filter to the last 2 weeks.
    GROUP BY Day, Top_Terms, rank
    ORDER BY Day, rank DESC
       -- Show the days in reverse chronological order.
"""


class GoogleTrends:
    """Class for Google Trends API access."""

    def __init__(self, key_path):
        """Initialise the class."""
        credentials = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
        self.trend_query = TREND_QUERY

    def get_trending_topics(self):
        """Get the trending topics."""
        query_job = self.client.query(self.trend_query)
        return query_job.result()
