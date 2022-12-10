from fastapi import Request
from fastapi.responses import HTMLResponse
from app import app, templates
from app.data_models import Post


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    """Home page."""
    post = Post(title='Test', content='This is a test', published=True)
    return templates.TemplateResponse(
        "post.html",
        {"request": request, "post": post}
    )
