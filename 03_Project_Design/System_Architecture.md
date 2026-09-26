# System Architecture

## Project Name
FitBuddy AI

## Architecture

FitBuddy AI follows a simple web application architecture.

### Main Components

1. User Interface
   - HTML
   - CSS
   - Jinja2 Templates

2. Backend
   - Python
   - FastAPI

3. AI Layer
   - Google Gemini AI
   - Generates wellness and fitness plans
   - Generates nutrition and recovery tips
   - Updates plans based on feedback

4. Database Layer
   - SQLite
   - SQLAlchemy

### Architecture Flow

User
↓
Jinja2 Web Interface
↓
FastAPI Backend
↓
Gemini AI
↓
Generated Fitness Plan
↓
SQLite Database
↓
Result Display

## Main Modules

- User Input Module
- Workout Plan Generator
- Nutrition Tip Generator
- Feedback Module
- Database Module
- Admin User View