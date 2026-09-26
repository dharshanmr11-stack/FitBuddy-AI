from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from pathlib import Path

from .database import (
    get_db,
    save_user,
    save_plan,
    get_user,
    get_latest_plan,
    update_plan,
    get_all_users
)

from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate_workout_plan
from .gemini_flash_generator import generate_nutrition_tip
from .updated_plan import generate_updated_plan
from .config import ADMIN_KEY


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

router = APIRouter()


# --------------------------------------------------
# Gemini error message helper
# --------------------------------------------------

def get_friendly_error(error):
    error_text = str(error)

    if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
        return (
            "Gemini AI usage limit has been reached temporarily. "
            "Please try again after the quota resets."
        )

    if "503" in error_text or "UNAVAILABLE" in error_text:
        return (
            "Gemini AI is temporarily busy. "
            "Please try again in a few moments."
        )

    if "404" in error_text or "NOT_FOUND" in error_text:
        return (
            "The selected Gemini AI model is currently unavailable. "
            "Please check the Gemini model configuration."
        )

    if "API key" in error_text or "GOOGLE_API_KEY" in error_text:
        return (
            "Gemini API key is not configured correctly. "
            "Please check the project configuration."
        )

    return error_text


# --------------------------------------------------
# Home page
# --------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# Generate workout from website form
# --------------------------------------------------

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    try:

        # Validate user input
        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        # Save user
        user = save_user(
            db,
            user_data.username,
            user_data.user_id,
            user_data.age,
            user_data.weight,
            user_data.goal,
            user_data.intensity
        )

        # Generate AI workout plan
        workout_plan = generate_workout_plan(
            user_data.username,
            user_data.age,
            user_data.weight,
            user_data.goal,
            user_data.intensity
        )

        # Generate nutrition/recovery tip
        nutrition_tip = generate_nutrition_tip(
            user_data.goal,
            user_data.intensity
        )

        # Save plan
        plan = save_plan(
            db,
            user_data.user_id,
            workout_plan,
            nutrition_tip
        )

        # Show result
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan
            }
        )

    except Exception as e:

        print("ERROR:", repr(e))

        friendly_error = get_friendly_error(e)

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": friendly_error
            },
            status_code=500
        )


# --------------------------------------------------
# Submit feedback and create revised plan
# --------------------------------------------------

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    try:

        # Validate feedback
        feedback_data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )

        # Find user
        user = get_user(
            db,
            feedback_data.user_id
        )

        if not user:
            raise ValueError("User not found.")

        # Find latest plan
        plan = get_latest_plan(
            db,
            feedback_data.user_id
        )

        if not plan:
            raise ValueError("No workout plan found.")

        # Generate revised plan
        revised_plan = generate_updated_plan(
            plan.original_plan,
            feedback_data.feedback,
            user.goal,
            user.intensity
        )

        # Save updated plan
        update_plan(
            db,
            plan,
            revised_plan,
            feedback_data.feedback
        )

        # Show updated result
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "plan": plan
            }
        )

    except Exception as e:

        print("FEEDBACK ERROR:", repr(e))

        friendly_error = get_friendly_error(e)

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": friendly_error
            },
            status_code=500
        )


# --------------------------------------------------
# Admin - View all users
# --------------------------------------------------

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    key: str = "",
    db: Session = Depends(get_db)
):

    if key != ADMIN_KEY:

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "error": "Invalid admin key."
            },
            status_code=403
        )

    users = get_all_users(db)

    user_data = []

    for user in users:

        latest_plan = get_latest_plan(
            db,
            user.user_id
        )

        user_data.append(
            {
                "user": user,
                "plan": latest_plan
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": user_data
        }
    )


# --------------------------------------------------
# Health check API
# --------------------------------------------------

@router.get("/api/health")
def health_check():

    return {
        "status": "ok",
        "app": "FitBuddy"
    }


# --------------------------------------------------
# API - Generate workout
# --------------------------------------------------

@router.post("/api/generate-workout")
def api_generate_workout(
    data: UserInput,
    db: Session = Depends(get_db)
):

    try:

        # Save user
        user = save_user(
            db,
            data.username,
            data.user_id,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        # Generate workout
        workout_plan = generate_workout_plan(
            data.username,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        # Generate nutrition tip
        nutrition_tip = generate_nutrition_tip(
            data.goal,
            data.intensity
        )

        # Save plan
        plan = save_plan(
            db,
            data.user_id,
            workout_plan,
            nutrition_tip
        )

        return {
            "success": True,
            "user_id": user.user_id,
            "plan_id": plan.id,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip
        }

    except Exception as e:

        print("API WORKOUT ERROR:", repr(e))

        friendly_error = get_friendly_error(e)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": friendly_error
            }
        )


# --------------------------------------------------
# API - Submit feedback
# --------------------------------------------------

@router.post("/api/submit-feedback")
def api_submit_feedback(
    data: FeedbackRequest,
    db: Session = Depends(get_db)
):

    try:

        # Find user
        user = get_user(
            db,
            data.user_id
        )

        if not user:
            raise ValueError("User not found.")

        # Find latest plan
        plan = get_latest_plan(
            db,
            data.user_id
        )

        if not plan:
            raise ValueError("No workout plan found.")

        # Generate revised plan
        revised_plan = generate_updated_plan(
            plan.original_plan,
            data.feedback,
            user.goal,
            user.intensity
        )

        # Save updated plan
        update_plan(
            db,
            plan,
            revised_plan,
            data.feedback
        )

        return {
            "success": True,
            "user_id": data.user_id,
            "updated_plan": revised_plan
        }

    except Exception as e:

        print("API FEEDBACK ERROR:", repr(e))

        friendly_error = get_friendly_error(e)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": friendly_error
            }
        )