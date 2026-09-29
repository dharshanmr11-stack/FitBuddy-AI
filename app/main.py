from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import SESSION_SECRET
from .database import init_db
from .routes import router


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="AI-powered fitness planning application using Gemini, FastAPI, SQLAlchemy and Jinja2.",
    version="1.0.0"
)


# Enable secure session support for Admin Login
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


app.include_router(router)


@app.on_event("startup")
def startup():
    init_db()