"""Functions to get trend data."""

from app.logger import logger
from app.models import Trends
from app.backend.google_bigquery import GoogleTrends


async def populate_uk_trends_from_google(period_days: int = 7):
    """Function to populate the trends table from Google for the UK.

    period_days (int): Number of days in the past to get trends for. Limited to 180.

    The function will check for existing trends in the database and only
    add new trends.
    """
    if period_days > 180:
        period_days = 180
    logger.info(f"Getting trends for last {period_days} days")
    gt = GoogleTrends()
    trends_dict = gt.get_formatted_trending_topics(period_days)
    logger.info(f"Got trends for {len(trends_dict)} days")
    logger.info("Syncing trends with database")
    for day, trends in trends_dict.items():
        # Check if the day is already in the database
        if await Trends.filter(date=day.isoformat()).first():
            logger.info(f"Day {day} already in database")
            continue
        # Add the trends to the database
        logger.info(f"Adding trends for {day}")
        trend_obj = await Trends(date=day.isoformat(), trends=trends, location="UK", source="Google")
        await trend_obj.save()
        logger.info(f"Added trends for {day}")
