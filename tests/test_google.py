"""Test getting Google Trend data from the BigQuery API."""

import pytest
import json
import os

from app.backend.google_bigquery import GoogleTrends, KEY_PATH


@pytest.fixture
def google_trends():
    # Check key values have loaded
    assert KEY_PATH
    # Create a GoogleTrends object
    google_trends = GoogleTrends(KEY_PATH)
    return google_trends


def test_google_trends_mock(google_trends, mocker):
    """Test getting Google Trend data from the BigQuery API."""
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    test_data_path = os.path.abspath(os.path.join(current_dir, "google_trends_test_data.json"))
    # Load test json from the google_trends_test_data.json file
    with open(test_data_path) as f:
        test_json = json.load(f)

    # Mock the GoogleTrends.get_trends() method
    mocker.patch.object(GoogleTrends, "get_trending_topics", return_value=test_json)

    # Call the get_trending_topics method
    trending_topics = google_trends.get_trending_topics()
    assert trending_topics == test_json


def test_google_trends(google_trends):
    """Test getting Google Trend data from the BigQuery API."""
    # Call the get_trending_topics method
    trending_topics = google_trends.get_trending_topics()
    assert trending_topics
    assert isinstance(trending_topics, dict)
