# Refactoring

## Major Issues Identified
- Tight coupling between DB and route logic
- No validation on email or password formats
- Repetitive response logic in routes
- Missing exception handling in DB operations

## Manual Work
1. Centralized DB connection (database.py)
2. Used parameterized queries to prevent SQL injection
3. Added password hashing with bcrypt
4. Introduced utils.py for consistent JSON responses
5. Separated routes into Blueprint (routes.py)
6. Used uuid in pytest to generate random email for testing the new user (POST)

## AI Tools Used
- ChatGPT

## AI Contribution
- Logic of Tight coupling between DB and the route Logic
- Found the missing exception handling in DB operations (pytest)

## AI generated code that are modified or rejected
1. code for pytest that test the users following actions

## Assumptions
- Used SQLite for local development
- No token-based authentication required (login just returns user_id)

## What if given even more time
- Add unit tests with pytest
- Integrate JWT-based authentication
- Improve schema migrations (e.g., Alembic)
- Add logging