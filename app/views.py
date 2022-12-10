from fastapi.responses import HTMLResponse
from app import app


@app.get('/', response_class=HTMLResponse)
def home():
    return "hello world!"
