"""Runs the webserver."""
import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Get and define absolute path to static and template files
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=template_path)

from app import views




