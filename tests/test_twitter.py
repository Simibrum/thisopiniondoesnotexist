"""Test the Twitter API functions."""

import pytest

from app.backend.twitter_api import TwitterTrends, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


@pytest.fixture
def twitter_trends():
    # Check key values have loaded
    assert API_KEY
    assert API_SECRET_KEY
    assert ACCESS_TOKEN
    assert ACCESS_TOKEN_SECRET
    # Create a TwitterTrends object
    twitter_trends = TwitterTrends(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return twitter_trends


def test_get_trending_topics(twitter_trends):
    # Get the trending topics for "Bath"
    trends = twitter_trends.get_trending_topics("Bath")

    # Assert that the list of trends is not empty
    assert trends

    # Assert that the list of trends contains only strings
    assert all(isinstance(trend, str) for trend in trends)

