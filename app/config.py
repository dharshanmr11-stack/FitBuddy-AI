import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Gemini API
# --------------------------------------------------

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
).strip()

GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-2.5-flash"
).strip()

GEMINI_TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-2.5-flash"
).strip()


# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)


# --------------------------------------------------
# Admin
# --------------------------------------------------

ADMIN_KEY = os.getenv(
    "ADMIN_KEY",
    "change-me"
).strip()


# --------------------------------------------------
# Session
# --------------------------------------------------

SESSION_SECRET = os.getenv(
    "SESSION_SECRET",
    "change-this-session-secret"
).strip()


# --------------------------------------------------
# Application
# --------------------------------------------------

APP_NAME = "FitBuddy"