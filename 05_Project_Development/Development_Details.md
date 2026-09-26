# Project Development

## Project Name
FitBuddy AI

## Development Overview

FitBuddy AI was developed as an AI-powered web application for generating simple personalized 7-day wellness and fitness plans.

## Technologies Used

- Python
- FastAPI
- Google Gemini AI
- SQLite
- SQLAlchemy
- Pydantic
- Jinja2
- HTML
- CSS

## Backend Development

The backend was developed using FastAPI.

Main backend components:

- User input validation
- Workout plan generation
- Nutrition and recovery tip generation
- Feedback processing
- Updated plan generation
- Database operations
- Error handling

## AI Integration

Google Gemini AI is integrated into the application to:

1. Generate a 7-day wellness and fitness plan.
2. Generate a short nutrition and recovery tip.
3. Create an updated plan using user feedback.

## Database Development

SQLite is used for storing:

- User information
- Generated plans
- Nutrition tips
- User feedback
- Updated plans

SQLAlchemy is used to communicate with the database.

## Frontend Development

The frontend was developed using:

- HTML
- CSS
- Jinja2 templates

Main pages include:

- Home page
- Result page
- Error page
- Admin user page

## Feedback Feature

Users can submit feedback about their generated plan.

The feedback is sent to Gemini AI and used to generate an updated 7-day plan.

## Error Handling

The application provides friendly error messages for:

- Invalid input
- Missing API key
- Temporary Gemini API problems
- Missing or unavailable AI model
- Other application errors

## Project Structure

```text
Fitbuddy AI
├── app
│   ├── config.py
│   ├── database.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static
│   └── css
│       └── style.css
├── templates
│   ├── all_users.html
│   ├── error.html
│   ├── index.html
│   └── result.html
└── requirements.txt