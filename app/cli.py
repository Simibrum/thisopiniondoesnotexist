"""Command line interface functions for the app."""
import click
import asyncio
from tortoise import Tortoise
from app.logger import logger
from app.db.init_db import init
from app.backend.generators.author_generation import populate_authors
from app.backend.generators.post_generation import populate_post
from app.backend.generators.trend_generator import populate_uk_trends_from_google
from app.utils import get_current_date


@click.group()
def cli():
    """Command line interface for the app."""
    pass


@click.command()
def test():
    """Run the tests."""
    import subprocess
    import sys

    tests = subprocess.run([sys.executable, "-m", "pytest"])
    sys.exit(tests.returncode)


@click.command()
async def generate_schemas():
    """Generate the schemas for the database."""
    await init()


@click.command()
@click.option("--num_authors", default=10, help="Number of authors to generate.")
def add_authors(num_authors: int = 10):
    """Populate the database with authors."""
    # Connecting to DB
    logger.info("Connecting to database...")
    asyncio.run(init())
    # Adding authors
    logger.info("Adding authors from command line...")
    asyncio.run(populate_authors(num_authors))
    logger.info("Done!")
    asyncio.run(Tortoise.close_connections())


@click.command()
@click.option("--date", default=get_current_date(), help="Date for the post.")
@click.option("--topics", help="Topics for the post.")
@click.option("--num_paragraphs", default=6, help="Number of paragraphs for the post.")
def add_post(date: str, topics: str, num_paragraphs: int):
    """Populate the database with a post."""
    if not date:
        date = get_current_date()
    # Connecting to DB
    logger.info("Connecting to database...")
    asyncio.run(init())
    # Adding post
    logger.info(f"Adding post on {topics} from command line...")
    asyncio.run(populate_post(date, topics, num_paragraphs))
    logger.info("Done!")
    asyncio.run(Tortoise.close_connections())


@click.command()
@click.option("--period_days", default=7, help="Number of days in the past to get trends (max 180)")
def get_trends(period_days: int = 7):
    """Populate the database with trends."""
    # Connecting to DB
    logger.info("Connecting to database...")
    asyncio.run(init())
    # Adding post
    logger.info(f"Gettings trends from command line...")
    asyncio.run(populate_uk_trends_from_google(period_days))
    logger.info("Done!")
    asyncio.run(Tortoise.close_connections())


cli.add_command(test)
cli.add_command(generate_schemas)
cli.add_command(add_authors)
cli.add_command(add_post)
cli.add_command(get_trends)

if __name__ == "__main__":
    cli()
