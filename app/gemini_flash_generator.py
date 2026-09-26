from google import genai
from google.genai import types

from .config import GOOGLE_API_KEY, GEMINI_TIP_MODEL


def generate_nutrition_tip(goal, intensity):
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy, a friendly wellness assistant.

Give one short, simple nutrition and recovery tip.

Goal: {goal}
Intensity: {intensity}

Rules:
- Give general healthy lifestyle advice.
- Do not give calorie targets.
- Do not recommend restrictive diets or fasting.
- Do not recommend supplements or drugs.
- Do not provide medical treatment.
- Keep the advice suitable for a young student.
- Maximum 100 words.
- Use simple English.

Return only the tip.
"""

    response = client.models.generate_content(
        model=GEMINI_TIP_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=300
        )
    )

    result = response.text

    if not result:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return result.strip()