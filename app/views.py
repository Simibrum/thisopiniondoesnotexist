import base64
from fastapi import Request
from fastapi.responses import HTMLResponse
from tortoise.contrib.fastapi import HTTPNotFoundError, DoesNotExist

from app import app, templates

from app.models import Post, Post_Pydantic, PostIn_Pydantic, Author, Author_Pydantic, \
    Image_Pydantic


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    """Home page."""
    post = Post(title='Test', content='This is a test', published=True)
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post}
    )


@app.post("/posts", response_model=Post_Pydantic)
async def create_post(post: PostIn_Pydantic):
    post_obj = await Post.create(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_tortoise_orm(post_obj)


@app.get(
    "/post/{post_id}", response_model=Post_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_post(post_id: int):
    return await Post_Pydantic.from_queryset_single(Post.get(id=post_id))


@app.get(
    "/author/{author_id}", response_model=Author_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_author(author_id: int):
    return await Author_Pydantic.from_queryset_single(Author.get(id=author_id))


@app.get(
    "/html/author/{author_id}", response_class=HTMLResponse, responses={404: {"model": HTTPNotFoundError}}
)
async def get_author(request: Request, author_id: int):
    try:
        db_author = await Author.get(id=author_id)
    except DoesNotExist:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": f"Author with id {author_id} not found"}
        )
    db_image = await db_author.photo
    author = await Author_Pydantic.from_tortoise_orm(db_author)
    if db_image:
        image = await Image_Pydantic.from_tortoise_orm(db_image)
    else:
        image = None
    return templates.TemplateResponse(
        "author.html",
        {"request": request, "author": author, "image": image}
    )


@app.get(
    "/html/post/{post_id}", response_class=HTMLResponse, responses={404: {"model": HTTPNotFoundError}}
)
async def get_post(request: Request, post_id: int):
    try:
        db_post = await Post.get(id=post_id)
    except DoesNotExist:
        return templates.TemplateResponse(
            "404.html",
            {"request": request, "message": f"Post with id {post_id} not found"}
        )
    post = await Post_Pydantic.from_tortoise_orm(db_post)
    """"
    db_image = await db_author.photo
    
    if db_image:
        image = await Image_Pydantic.from_tortoise_orm(db_image)
    else:
        image = None
    """
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post}
    )
