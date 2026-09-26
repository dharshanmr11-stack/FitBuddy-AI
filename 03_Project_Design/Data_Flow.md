# Data Flow

## Project Name
FitBuddy AI

## Data Flow Process

1. User enters personal information.
2. FastAPI receives the submitted data.
3. Pydantic validates the input.
4. User information is stored in SQLite.
5. FastAPI sends the required information to Gemini AI.
6. Gemini AI generates a 7-day wellness and fitness plan.
7. A nutrition and recovery tip is generated.
8. The generated information is stored in the database.
9. The result is displayed on the web page.
10. User can submit feedback.
11. Feedback is sent to Gemini AI.
12. Gemini AI generates an updated plan.
13. The updated plan is stored and displayed.

## Simple Flow

User Input
↓
Validation
↓
Database
↓
Gemini AI
↓
7-Day Plan
↓
Nutrition Tip
↓
Result Page
↓
User Feedback
↓
Updated Plan