"""Command line interface functions for the app."""
import click
import asyncio
from tortoise import Tortoise
from app.logger import logger
from app.db.init_db import init
from app.backend.generators.author_generation import populate_authors


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


cli.add_command(test)
cli.add_command(generate_schemas)
cli.add_command(add_authors)

if __name__ == "__main__":
    cli()
