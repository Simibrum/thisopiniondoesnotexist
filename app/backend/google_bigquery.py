"""File for Google BiqQuery API access."""
import os

from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
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
TREND_QUERY = f"""
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
       AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {{}} DAY)
           -- Filter to the last 2 weeks.
    GROUP BY Day, Top_Terms, rank
    ORDER BY Day, rank DESC
       -- Show the days in reverse chronological order.
"""


class GoogleTrends:
    """Class for Google Trends API access."""

    def __init__(self):
        """Initialise the class."""
        credentials = service_account.Credentials.from_service_account_file(
            KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

        self.client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
        self.trend_query = TREND_QUERY

    def get_trending_topics(self, period_days: int = 7):
        """Get the trending topics."""
        df = self.get_trending_topics_as_df(period_days)
        # Convert the dataframe to a dictionary
        df_dict = df.to_dict()
        return df_dict

    def get_trending_topics_as_df(self, period_days: int = 7):
        """Get the trending topics as a dataframe."""
        query_job = self.client.query(self.trend_query.format(period_days))
        results = query_job.result()
        df = results.to_dataframe()
        return df

    def get_formatted_trending_topics(self, period_days: int = 7):
        """Get the trending topics as a formatted string."""
        df = self.get_trending_topics_as_df(period_days)
        # Group the dataframe by day
        grouped_df = df.groupby("Day")
        # Group the top terms as a list
        top_terms_arrays = grouped_df['Top_Terms'].apply(lambda x: x.values.tolist())
        # Output as dict
        return top_terms_arrays.to_dict()
