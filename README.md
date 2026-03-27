# Lesson Reminder API

A FastAPI backend for managing student lesson tracking and invoice preview logic for a music school.

This project implements a layered architecture, domain-driven validation, dependency injection, and API-level testing using FastAPI and Pytest.

---

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Project Structure

- `app/api/v1/` – FastAPI routers
- `app/services/` – Business logic layer
- `app/schemas/` – Pydantic request/response models
- `app/core/` – Domain exceptions and core utilities
- `app/repositories` – SQLite persistence via SQLAlchemy, with optional in-memory implementation
- `app/api/tests/` – API integration tests using FastAPI TestClient

---

## Running the Application

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running Tests

Run all tests with:
```bash
python -m pytest
```
The test suite includes:
- Service-level tests for business logic
- API-level tests using FastAPI TestClient
- Validation and error-handling tests
- Domain exception handling tests

---

## API Endpoints

System
- GET /api/v1/health

---

Students 
- POST /api/v1/students
- POST /api/v1/students/remaining-lessons
- GET /api/v1/students/remaining-lessons
- GET /api/v1/students/{student_email}
- GET /api/v1/students/{student_email}/remaining-lessons
- PUT /api/v1/students/{student_email}
- DELETE /api/v1/students/{student_email}

---

Invoices
- POST /api/v1/invoices/preview

Dates for invoice preview are expected in DD-MM-YY format.

---

Lessons
- POST /api/v1/lessons
- GET /api/v1/lessons
- GET /api/v1/lessons/{lesson_id}
- PUT /api/v1/lessons/{lesson_id}

Lessons are created using dates in DD-MM-YY HH:MM format.
Lessons are fetched using a range of dates in DD-MM-YY format.
Lesson duration must be 30 or 60.

---

Auth
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

---

## Architecture

The application follows a layered architecture:
- Routers handle HTTP concerns.
- Services contain business logic. 
- Schemas define request and response models.
- Domain errors are raised in the service layer and handled globally via a custom exception handler.
- StudentService uses a pluggable LessonRepository, allowing different persistence implementations (e.g. in-memory or SQLAlchemy-backed)

This separation ensures that business logic remains independent of the HTTP layer and allows external integrations (such as scheduling providers) to be swapped without affecting core domain logic.

---

### Layers

- **API Layer** – FastAPI routes
- **Service Layer** – Business logic
- **Repository Layer** – Database access
- **Database Layer** – SQLAlchemy models

---

## Logging

Application logs are written to `app.log`.

- Request/response logging via FastAPI middleware
- Service-level logging for domain events and validation errors

---

## API Documentation

Interactive API docs are available at:

- http://localhost:8000/docs
- http://localhost:8000/redoc
