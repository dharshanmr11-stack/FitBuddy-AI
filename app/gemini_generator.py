from google import genai
from google.genai import types

from .config import GOOGLE_API_KEY, GEMINI_WORKOUT_MODEL


def generate_workout_plan(
    username,
    age,
    weight,
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

Create a safe and simple 7-day wellness and fitness plan.

User information:
Name: {username}
Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

Important safety rules:
- Keep the plan suitable for a young student.
- Focus on general health, fitness, mobility and wellbeing.
- Do not give extreme exercise routines.
- Do not recommend starvation, fasting, crash diets or restrictive eating.
- Do not recommend supplements, drugs or unsafe substances.
- Do not give medical treatment or diagnose health conditions.
- Include rest and recovery.
- Encourage stopping exercise if there is pain, dizziness or unusual discomfort.
- Do not promote unhealthy body-image goals.

Return exactly a 7-day plan.

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

    try:

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

    except Exception as e:

        error_text = str(e)

        # Do not retry when quota is exceeded.
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            raise RuntimeError(
                "Gemini AI usage limit has been reached temporarily. "
                "Please try again after the quota resets."
            )

        # Model temporarily unavailable.
        if "503" in error_text or "UNAVAILABLE" in error_text:
            raise RuntimeError(
                "Gemini AI is temporarily busy. "
                "Please try again later."
            )

        raise