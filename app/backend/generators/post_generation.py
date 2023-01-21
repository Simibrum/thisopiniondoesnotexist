"""Functions and variables for post generation."""
import random
from app.logger import logger
from app.backend.gpt import TextGenerator
from app.models import Author, Post
from app.backend.generators.author_generation import summarise_author
from app.utils import get_date_components, get_heading

plan_prompt = f"""/
Write a outline plan for an online newspaper opinion article based on the information below. Set out the headings 
and sub-headings and write keyword notes on each paragraph contents. The full article will be around 1000 words long. 
Only write the outline plan for now.

Author is {{}}.

The date is {{}}.

The following are the topics for the opinion article: {{}}.

In the plan sketch out how you would tie the topics together. Write from the perspective of the author. 
There are to be {{}} paragraphs in the article.

Use the format:

Article Title: xxxx
Introduction: [key points]
Paragraph 1: [key points]
Paragraph 2: [key points]
etc.
Conclusion: [key points]
"""

# We need to pick 3 trending topic ourselves randomly to reduce the article size

# Use the schema: 1. Introduction, 2. Main Body, 3. Conclusion
paragraph_prompt = f"""/
You are {{}}.

Here is a plan for the article.

{{}}

Now start by writing {{}} from the plan. Don't include any headings:
"""


def generate_plan(author_summary: str, date: str, topics: str, num_paragraphs: int = 6) -> str:
    """Generate a plan for an article."""
    prompt = plan_prompt.format(author_summary, date, topics, num_paragraphs)
    generator = TextGenerator()
    generated_text = generator.complete(prompt, max_tokens=1024)
    return generated_text


def generate_paragraphs(plan: str, author_summary: str, num_paragraphs: int = 3) -> str:
    """Generate paragraphs for an article."""
    generator = TextGenerator()
    generated_text = list()
    for para_num in range(1, num_paragraphs+1):
        logger.info(f"Generating paragraph {para_num}")
        prompt = paragraph_prompt.format(author_summary, plan, para_num)
        generated_text.append(generator.complete(prompt, max_tokens=1024))
    return "\n\n".join(generated_text)


async def populate_post(date: str, topics: str, num_paragraphs: int = 6) -> Post:
    """Generate a post for the given date and topics using a random author and populate the database."""
    logger.info("Selecting random author")
    authors = await Author.all()
    author = random.choice(authors)
    logger.info(f"Selected author {author.name}")
    logger.info("Condensing author bio")
    author_summary = summarise_author(author)
    logger.info("Generating plan")
    plan = generate_plan(author_summary, date, topics, num_paragraphs)
    logger.info("Generating paragraphs")
    paragraphs = generate_paragraphs(plan, author_summary, num_paragraphs)
    logger.info("Generating post")
    # Format date into day, month, year
    day, month, year = get_date_components(date)
    # Get title
    title = get_heading(paragraphs)
    db_post = await Post.create(
        day=day,
        month=month,
        year=year,
        title=title,
        content=paragraphs,
        published=True,
        author=author
    )
    logger.info(f"Created post {db_post.title} with id {db_post.id}")
    logger.info("Saving post to database")
    await db_post.save()
    logger.info("Completed")
    return db_post
