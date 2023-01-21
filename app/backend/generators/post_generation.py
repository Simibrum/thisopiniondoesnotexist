"""Functions and variables for post generation."""
import random
import re
from typing import Optional, Tuple
from app.logger import logger
from app.backend.gpt import TextGenerator
from app.models import Author, Post, Trends, Image
from app.backend.generators.author_generation import summarise_author
from app.backend.generators.image_generation import generate_article_images
from app.utils import get_date_components, get_heading, premier_league_teams, count_paragraphs_in_plan

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

Now start by writing paragraph {{}} from the plan. Don't include any headings. 
Write from the perspective of the author. 
"""


def generate_plan(author_summary: str, date: str, topics: str, num_paragraphs: int = 5) -> str:
    """Generate a plan for an article."""
    prompt = plan_prompt.format(author_summary, date, topics, num_paragraphs)
    logger.debug(f"Plan prompt is: {prompt}")
    generator = TextGenerator()
    generated_text = generator.complete(prompt, max_tokens=1024)
    return generated_text


def generate_paragraphs(plan: str, author_summary: str, num_paragraphs: int = 5) -> str:
    """Generate paragraphs for an article."""
    # Check for number of paragraphs in plan and set num_paragraphs to that
    num_plan_paragraphs = count_paragraphs_in_plan(plan)
    if num_plan_paragraphs != num_paragraphs:
        logger.warning(
            "Number of paragraphs in plan does not match number of paragraphs to generate."
            "Using number of paragraphs in plan."
        )
        num_paragraphs = num_plan_paragraphs
    generator = TextGenerator()
    generated_text = list()
    for para_num in range(1, num_paragraphs+1):
        logger.info(f"Generating paragraph {para_num}")
        prompt = paragraph_prompt.format(author_summary, plan, para_num)
        logger.debug(f"Prompt is: {prompt}")
        generated_text.append(generator.complete(prompt, max_tokens=1024, temperature=0.8))
    return "\n\n".join(generated_text)


async def generate_post_images(plan: str) -> Optional[Tuple[Image, Image]]:
    """Generate lead and body images for a post."""
    logger.info("Generating post images...")
    (lead_image_alt_text, lead_image), (body_image_alt_text, body_image) = generate_article_images(plan)
    logger.info("Generated post images")
    if lead_image:
        logger.info("Saving lead image to database")
        # Get name and caption as first clause or sentence
        lead_image_name = re.split(r".|,|;", lead_image_alt_text)[0] if lead_image_alt_text else ""
        logger.info("Saving lead image to database")
        lead_image_db = await Image.create(
            name=lead_image_name,
            description=lead_image_alt_text,
            image=lead_image,
            caption=lead_image_name,
            width=512,
            height=512
        )
        await lead_image_db.save()
        logger.info("Saved lead image to database")
    else:
        lead_image_db = None
    if body_image:
        logger.info("Saving body image to database")
        # Get name and caption as first clause or sentence
        body_image_name = re.split(r".|,|;", body_image_alt_text)[0] if body_image_alt_text else ""
        body_image_db = await Image.create(
            name=body_image_name,
            description=body_image_alt_text,
            image=body_image,
            caption=body_image_name,
            width=512,
            height=512
        )
        await body_image_db.save()
        logger.info("Saved body image to database")
    else:
        body_image_db = None
    return lead_image_db, body_image_db


async def populate_post(
        date: str, topics: str, num_paragraphs: int = 5, overwrite: bool = True, with_images: bool = True
) -> Post:
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
    title = get_heading(plan)
    logger.info(f"Title is: {title}")
    # Get lead image and body image
    if with_images:
        lead_image, body_image = await generate_post_images(plan)
    else:
        lead_image, body_image = None, None
    # Determine if a post with the same day, month and year already exists
    post = await Post.filter(day=day, month=month, year=year).first()
    if post:
        if overwrite:
            logger.info("Found existing post, overwriting")
            post.title = title
            post.paragraphs = paragraphs
            post.plan = plan
            post.author = author
            post.lead_image = lead_image
            post.body_image = body_image
            logger.info("Saving updated post to database")
            await post.save()
        else:
            logger.info("Found existing post, not overwriting")
    else:
        logger.info("No existing post found, creating new post")
        post = await Post.create(
            title=title,
            paragraphs=paragraphs,
            plan=plan,
            author=author,
            day=day,
            month=month,
            published=True,
            year=year,
            lead_image=lead_image,
            body_image=body_image
        )
        logger.info(f"Created post {post.title} with id {post.id}")
        logger.info("Saving post to database")
        await post.save()
    logger.info("Completed")
    return post


async def trends2posts(
        num_posts: int = 1, overwrite: bool = False, num_paragraphs: int = 5, with_images: bool = True
                       ) -> None:
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
        await populate_post(
            trend_day.date.isoformat(), topics, num_paragraphs, overwrite=overwrite, with_images=with_images)
        num_of_generated_posts += 1
    logger.info("All Requested Posts Generated")
