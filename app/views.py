from fastapi import Request
from fastapi.responses import HTMLResponse
from app import app, templates


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "generic_page.html",
        {"request": request, "title": "Hello World!", "content": "Hello World!"}
    )
