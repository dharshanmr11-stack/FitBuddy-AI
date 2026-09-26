from pydantic import BaseModel, Field, field_validator
from typing import Literal


class UserInput(BaseModel):
    username: str = Field(..., min_length=2, max_length=100)
    user_id: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=13, le=100)
    weight: float = Field(..., gt=0, le=500)
    goal: str = Field(..., min_length=2, max_length=200)
    intensity: Literal["low", "medium", "high"]

    @field_validator("username", "user_id", "goal")
    @classmethod
    def clean_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=100)
    feedback: str = Field(..., min_length=3, max_length=2000)

    @field_validator("user_id", "feedback")
    @classmethod
    def clean_feedback_data(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        return value