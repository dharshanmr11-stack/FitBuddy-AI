# Database Design

## Project Name
FitBuddy AI

## Database

SQLite is used as the database for the project.

## Main Tables

### Users Table

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| username | String | User name |
| user_id | String | Unique user ID |
| age | Integer | User age |
| weight | Float | User-provided weight |
| goal | String | Fitness/wellness goal |
| intensity | String | Workout intensity |
| created_at | DateTime | Creation date |

### Plans Table

| Field | Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | String | Connected user ID |
| original_plan | Text | Original generated plan |
| updated_plan | Text | Updated plan |
| nutrition_tip | Text | Nutrition and recovery tip |
| feedback | Text | User feedback |
| created_at | DateTime | Creation date |
| updated_at | DateTime | Last update date |

## Relationship

One user can have multiple plans.

Users
↓
Plans