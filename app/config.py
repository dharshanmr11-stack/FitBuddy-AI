import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Current Gemini model
GEMINI_WORKOUT_MODEL = "gemini-3.8-flash"
GEMINI_TIP_MODEL = "gemini-3.8-flash"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)

ADMIN_KEY = os.getenv(
    "ADMIN_KEY",
    "change-me"
)

APP_NAME = "FitBuddy"