from google import genai
from google.genai import types

from .config import GOOGLE_API_KEY, GEMINI_WORKOUT_MODEL


def generate_updated_plan(
    original_plan,
    feedback,
    goal,
    intensity
):
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy, a friendly fitness planning assistant.

The user already has a 7-day wellness plan and has provided feedback.
Create a revised 7-day plan based on the feedback.

Goal: {goal}
Intensity: {intensity}

Original Plan:
{original_plan}

User Feedback:
{feedback}

Safety rules:
- Keep the plan suitable for a young student.
- Focus on general health, fitness, mobility and wellbeing.
- Do not create extreme exercise routines.
- Do not recommend starvation, fasting, crash diets or restrictive eating.
- Do not recommend supplements, drugs or unsafe substances.
- Do not provide medical treatment or diagnosis.
- Include rest and recovery.
- Do not promote unhealthy body-image goals.

Return a complete revised 7-day plan.

Use this format:

DAY 1
Focus:
Warm-up:
Main Workout:
- Exercise - sets/reps or duration
- Exercise - sets/reps or duration
Rest / Recovery:
Cool-down:

DAY 2
Focus:
Warm-up:
Main Workout:
- Exercise - sets/reps or duration
- Exercise - sets/reps or duration
Rest / Recovery:
Cool-down:

Continue the same format through DAY 7.

Keep the language simple and easy to understand.
"""

    response = client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=5000
        )
    )

    result = response.text

    if not result:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return result.strip()