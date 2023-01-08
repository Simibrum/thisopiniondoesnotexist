"""Functions and classes to generate post authors."""
from typing import List, Tuple
from app.logger import logger
from app.backend.gpt import TextGenerator
from app.models import Author

initial_stats_prompt = f"""\
Generate a table with the following information: name, age, gender 
for {{}} people who are famous opinion writers for national 
newspapers of various types. 

Include a balanced set of ages, nationalities, backgrounds and genders.

|name|age|gender|
|---|---|------|
"""

bio_generator_prompt = f"""\
You are given the information on a famous opinion writers for national newspaper: 
{{}}, {{}}, {{}} 

Write a 300 word bio for this person.
"""

photo_description_generator_prompt = f"""\
You are given the information on a famous opinion writers for national newspaper:
{{}}, {{}}, {{}}

Write a 100 word alt text description of a photo of this person that can be used as a generative image prompt.
"""


def generate_authors(num_authors: int = 10) -> List[Tuple[str, int, str]]:
    """Generate a set of authors and output as a list of tuples with (name, age, gender)."""
    prompt = initial_stats_prompt.format(num_authors)
    generator = TextGenerator()
    generated_text = generator.complete(prompt, max_tokens=512)
    # Convert generated text to a list of tuples
    authors = []
    for line in generated_text.splitlines():
        if line.startswith("|"):
            try:
                name, age, gender = line.split("|")[1:-1]
                authors.append((name.strip(), int(age), gender.strip()))
            except ValueError:
                continue
    return authors


def generate_bio(name: str, age: int, gender: str) -> str:
    """Generate a bio for the given author."""
    prompt = bio_generator_prompt.format(name, str(age), gender)
    generator = TextGenerator()
    generated_text = generator.complete(prompt, max_tokens=512)
    return generated_text


def generate_photo_desc(name: str, age: int, gender: str) -> str:
    """Generate a photo description for the given author."""
    prompt = photo_description_generator_prompt.format(name, str(age), gender)
    generator = TextGenerator()
    generated_text = generator.complete(prompt, max_tokens=512)
    return generated_text


async def populate_authors(num_authors: int = 10):
    """Populate the database with a set of authors."""
    logger.info(f"Populating {num_authors} authors...")
    logger.info("Generating author stats...")
    authors = generate_authors(num_authors)
    logger.info("Generating author bios...")
    for author in authors:
        name, age, gender = author
        logger.info(f"Generating bio for {name}...")
        bio = generate_bio(*author)
        logger.info(f"Generating photo description for {name}...")
        photo_desc = generate_photo_desc(*author)
        db_author = await Author.create(
            name=name,
            age=age,
            gender=gender,
            bio=bio,
            photo_description=photo_desc
        )
        logger.info(f"Created author {db_author.name} with id {db_author.id}")
        await db_author.save()
        logger.info("Saved author!")
    logger.info("Done!")
    return True

