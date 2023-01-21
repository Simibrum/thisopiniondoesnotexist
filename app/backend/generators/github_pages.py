"""Code to generate the GitHub Pages site."""
import os
from jinja2 import Environment, FileSystemLoader
from app.models import Author, Image, Post

# Path: app/backend/generators/github_pages.py
# Get current file path
current_file_path = os.path.dirname(os.path.realpath(__file__))
# Go back up three folders
root_path = os.path.abspath(os.path.join(current_file_path, os.pardir, os.pardir, os.pardir))
# Get the path of the docs folder
docs_path = os.path.join(root_path, "docs")
# Get the path of the templates folder
templates_path = os.path.join(root_path, "app", "templates")


async def save_images(overwrite=False):
    """Save the images to the docs folder."""
    images = await Image.all()
    for image in images:
        # Check if there is an image file for this image
        if os.path.isfile(f"{docs_path}/images/{image.id}.png") and not overwrite:
            continue
        else:
            # Write the image to a file
            with open(f"{docs_path}/images/{image.id}.png", "wb") as f:
                f.write(image.image)


async def generate_author_page_md(overwrite=False):
    """Generate markdown output from the author records."""
    # Load the templates
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("author.md")
    authors = await Author.all()
    for author in authors:
        # Check if there is a md file for this author
        if os.path.isfile(f"{docs_path}/authors/{author.id}.md") and not overwrite:
            continue
        else:
            # Get the author's image
            image = await author.photo
            # Render the template
            output = template.render(author=author, image=image)
            # Write the output to a file
            with open(f"{docs_path}/authors/{author.id}.md", "w") as f:
                f.write(output)


async def generate_post_md(overwrite=False):
    """Generate markdown output from the post records."""
    # Load the templates
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("post.md")
    posts = await Post.all()
    for post in posts:
        # Check if there is a md file for this post
        if os.path.isfile(f"{docs_path}/posts/{post.id}.md") and not overwrite:
            continue
        else:
            # Get the author and photo details to pass to the template
            author = await post.author
            lead_image = await post.lead_image
            body_image = await post.body_image
            # Render the template
            output = template.render(post=post, author=author, lead_image=lead_image, body_image=body_image)
            # Write the output to a file
            with open(f"{docs_path}/posts/{post.id}.md", "w") as f:
                f.write(output)
