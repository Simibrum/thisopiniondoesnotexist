"""Test syncing the database with Google Trends."""
import pytest
import datetime
from unittest.mock import patch
from app.backend.generators.trend_generator import populate_uk_trends_from_google
from app.models import Trends


@pytest.mark.anyio
@patch("app.backend.google_bigquery.GoogleTrends.get_formatted_trending_topics")
async def test_author_batch(mock_get_formatted_trending_topics, in_memory_db):
    """Test creating a batch of authors."""
    mock_get_formatted_trending_topics.return_value = {
        datetime.date(2023, 1, 14): ['Justin Roiland', 'Margot Robbie', 'Joao Felix', 'Leeds United']
    }
    await populate_uk_trends_from_google(period_days=1)
    trends = await Trends.all()
    assert len(trends) == 1
    for trends_record in trends:
        assert trends_record.date.date().isoformat() == datetime.date(2023, 1, 14).isoformat()
        assert trends_record.source == "Google"
        assert trends_record.location == "UK"
        assert trends_record.trends == ['Justin Roiland', 'Margot Robbie', 'Joao Felix', 'Leeds United']