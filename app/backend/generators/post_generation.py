"""Functions and variables for post generation."""
import random
from app.logger import logger
from app.backend.gpt import TextGenerator
from app.models import Author, Post, Trends
from app.backend.generators.author_generation import summarise_author
from app.utils import get_date_components, get_heading, premier_league_teams

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
Paragraph 1 - introduction: [key points]
Paragraph 2 - body: [key points]
...               : [key points]
etc.
Paragraph N - conclusion: [key points]
"""

# We need to pick 3 trending topic ourselves randomly to reduce the article size

# Use the schema: 1. Introduction, 2. Main Body, 3. Conclusion
paragraph_prompt = f"""/
You are {{}}.

Here is a plan for the article.

{{}}

Now start by writing paragraph {{}} from the plan. Don't include any headings:
"""


def generate_plan(author_summary: str, date: str, topics: str, num_paragraphs: int = 6) -> str:
    """Generate a plan for an article."""
    prompt = plan_prompt.format(author_summary, date, topics, num_paragraphs)
    logger.debug(f"Plan prompt is: {prompt}")
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
        logger.debug(f"Prompt is: {prompt}")
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
    logger.debug(f"Plan is: {plan}")
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


async def trends2posts(num_posts: int = 1, overwrite: bool = False, num_paragraphs: int = 6) -> None:
    """Generate posts for the given number of days."""
    logger.info("Getting trending topics")
    trends = await Trends.all()
    num_of_generated_posts = 0
    logger.info(f"Generating {num_posts} posts")
    for trend_day in trends:
        if num_of_generated_posts >= num_posts:
            break
        # Convert the trend date to day, month, year integers
        day, month, year = get_date_components(trend_day.date.isoformat())
        # Check if a post for this day already exists
        if await Post.filter(day=day, month=month, year=year).first() and not overwrite:
            logger.info(f"Post for {trend_day.date.date()} already exists")
            continue
        logger.info(f"Generating post for {trend_day.date}")
        # Exclude premier league teams from the topics
        topics = [topic for topic in trend_day.trends if topic not in premier_league_teams]
        # Pick 3 topics randomly
        topics = random.sample(topics, 3)
        # Join the topics into a string
        topics = ", ".join(topics)
        logger.info(f"Topics for post: {topics}")
        # Generate the post
        await populate_post(trend_day.date.isoformat(), topics, num_paragraphs)
        num_of_generated_posts += 1
    logger.info("All Requested Posts Generated")
