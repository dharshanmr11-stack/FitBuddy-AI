from google import genai
from google.genai import types
import time

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
You are FitBuddy, a friendly wellness and fitness assistant.

Create a safe, simple 7-day wellness and fitness plan.

User information:
Name: {username}
Age: {age}
Weight: {weight}
Goal: {goal}
Intensity: {intensity}

Safety rules:
- Keep the plan suitable for a young student.
- Focus on general health, fitness, mobility and wellbeing.
- Do not give extreme exercise routines.
- Do not recommend starvation, fasting, crash diets or restrictive eating.
- Do not recommend supplements, drugs or unsafe substances.
- Do not diagnose medical conditions or provide medical treatment.
- Include rest and recovery.
- Encourage stopping exercise if there is pain, dizziness or unusual discomfort.
- Do not promote unhealthy body-image goals.

Return exactly 7 days.

Use this format:

DAY 1
Focus:
Warm-up:
Main Workout:
- Exercise
- Exercise
Rest / Recovery:
Cool-down:

DAY 2
Focus:
Warm-up:
Main Workout:
- Exercise
- Exercise
Rest / Recovery:
Cool-down:

Continue the same format through DAY 7.

Keep the language simple and easy to understand.
"""

    max_attempts = 4

    for attempt in range(max_attempts):

        try:

            print(
                f"Gemini workout attempt "
                f"{attempt + 1}/{max_attempts}"
            )

            response = client.models.generate_content(
                model=GEMINI_WORKOUT_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=5000
                )
            )

            result = response.text

            if not result:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            print("Workout plan generated successfully.")

            return result.strip()

        except Exception as e:

            error_text = str(e)

            print(
                "Gemini workout error:",
                repr(e)
            )

            # ----------------------------------------
            # Gemini temporarily busy
            # ----------------------------------------

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):

                if attempt < max_attempts - 1:

                    print(
                        "Gemini is temporarily busy. "
                        "Retrying in 10 seconds..."
                    )

                    time.sleep(10)
                    continue

                raise RuntimeError(
                    "Gemini AI is temporarily busy. "
                    "Please wait a few moments and try again."
                )

            # ----------------------------------------
            # Gemini usage limit
            # ----------------------------------------

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < max_attempts - 1:

                    print(
                        "Gemini usage limit detected. "
                        "Retrying in 10 seconds..."
                    )

                    time.sleep(10)
                    continue

                raise RuntimeError(
                    "Gemini AI usage limit has been reached temporarily. "
                    "Please try again after the quota resets."
                )

            # ----------------------------------------
            # Model not available
            # ----------------------------------------

            if (
                "404" in error_text
                or "NOT_FOUND" in error_text
            ):

                raise RuntimeError(
                    "The configured Gemini model is unavailable. "
                    "Please check the Gemini model configuration."
                )

            # ----------------------------------------
            # API key problem
            # ----------------------------------------

            if (
                "API key" in error_text
                or "GOOGLE_API_KEY" in error_text
            ):

                raise RuntimeError(
                    "Gemini API key is not configured correctly."
                )

            raise