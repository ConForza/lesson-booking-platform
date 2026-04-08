# Lesson Reminder API

A production-ready backend service designed to manage lesson scheduling, student tracking, and invoice generation for a music school.

This project implements a layered architecture, domain-driven validation, dependency injection, and API-level testing using FastAPI and Pytest.

![CI](https://github.com/ConForza/lesson-reminder-api/actions/workflows/ci.yml/badge.svg)

---

## Live API

Base URL:
https://lesson-reminder-api.onrender.com

Interactive docs:
https://lesson-reminder-api.onrender.com/docs

---

## Tech Stack

- Python 3.14
- FastAPI
- Pydantic
- Pytest
- Uvicorn

---

## Features

- Student management (create, update, delete, list)
- Lesson scheduling with conflict detection
- Lesson filtering (by date, student, pagination)
- Invoice preview generation
- Authentication with JWT (register, login, protected routes)
- Remaining lesson tracking per student
- Centralised error handling with consistent API responses
- Structured logging and request tracing
- Full API test suite with CI integration

---

## Key Design Decisions

- **Layered architecture** to separate HTTP concerns from business logic
- **Repository pattern** to allow swapping persistence layers (in-memory vs SQLAlchemy)
- **Domain-level validation** handled in the service layer rather than controllers
- **Centralised error handling** for consistent API responses
- **JWT-based authentication** with dependency-injected user context

### Architecture Diagram

![Architecture Diagram](docs/architecture-diagram.png)

---

## Project Structure

- `app/api/v1/` – FastAPI routers
- `app/services/` – Business logic layer
- `app/schemas/` – Pydantic request/response models
- `app/core/` – Domain exceptions and core utilities
- `app/repositories` – SQLite persistence via SQLAlchemy, with optional in-memory implementation
- `app/api/tests/` – API integration tests using FastAPI TestClient

---

## Local Development

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

## Running with Docker

Build the image:

```bash
docker build -t lesson-reminder-api .
```

Run the container:

```bash
docker run -p 8000:8000 \
-e JWT_SECRET_KEY=your-secret-key \
lesson-reminder-api
```

---

## API Endpoints

### System
- GET /api/v1/health

### Students 
- POST /api/v1/students
- POST /api/v1/students/remaining-lessons
- GET /api/v1/students/remaining-lessons
- GET /api/v1/students/{student_email}
- GET /api/v1/students/{student_email}/remaining-lessons
- PUT /api/v1/students/{student_email}
- DELETE /api/v1/students/{student_email}

### Invoices
- POST /api/v1/invoices/preview

Dates for invoice preview are expected in DD-MM-YY format.

### Lessons
- POST /api/v1/lessons
- GET /api/v1/lessons
- GET /api/v1/lessons/{lesson_id}
- PUT /api/v1/lessons/{lesson_id}

Lessons are created using dates in DD-MM-YY HH:MM format.
Lessons are fetched using a range of dates in DD-MM-YY format.
Lesson duration must be 30 or 60.

### Auth
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

## Environment Variables

The application requires the following environment variables:

- `JWT_SECRET_KEY` – secret used to sign JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES` - defaults to 30
- `ENVIRONMENT` - defaults to 'development'
- `APP_NAME` - defaults to 'Lesson Reminder API' 
- `API_V1_PREFIX` - defaults to '/api/v1'
- `VERSION` - defaults to '0.1.0'

You can define these in a `.env` file for local development. Refer to `.env.example` for a template.

---

## API Documentation

Interactive API docs are available locally at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

---

## Deployment

The application is deployed on Render using Docker.

### Key details

- Containerised using Docker
- Environment variables configured via Render dashboard
- Automatic deploys on push via GitHub integration

### Required environment variables

- JWT_SECRET_KEY
- ACCESS_TOKEN_EXPIRE_MINUTES
- ENVIRONMENT
- APP_NAME
- API_V1_PREFIX
- VERSION

This project is designed to be deployment-ready, with environment-based configuration and containerised infrastructure.

---

## Future Improvements

- Add background job processing (e.g. Celery) for scheduled reminders
- Introduce PostgreSQL for production persistence
- Add rate limiting and request throttling
- Implement role-based access control (RBAC)
- Add caching layer (Redis) for frequently accessed data
- Expand test coverage to include repository layer
