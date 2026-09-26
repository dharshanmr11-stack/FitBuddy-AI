# Proposed Solution

## Project Name
FitBuddy AI

## Solution

FitBuddy AI is an AI-powered web application that generates a simple 7-day wellness and fitness plan using user-provided information.

The application uses Google Gemini AI to generate the plan and provide a short wellness tip. User information and generated plans are stored using SQLite.

## Working Process

1. User opens the FitBuddy AI website.
2. User enters basic information such as name, user ID, age, weight, goal and workout intensity.
3. The application validates the information.
4. The information is stored in the SQLite database.
5. Gemini AI generates a 7-day wellness and fitness plan.
6. A short nutrition and recovery tip is generated.
7. The generated plan is displayed to the user.
8. The user can provide feedback.
9. FitBuddy AI generates an updated plan based on the feedback.

## Technologies

- Python
- FastAPI
- Google Gemini AI
- SQLite
- SQLAlchemy
- Jinja2
- HTML
- CSS

## Expected Outcome

The final application provides users with a simple, personalized weekly wellness plan through an easy-to-use web interface.