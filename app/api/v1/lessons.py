from fastapi import APIRouter, Depends
from datetime import datetime, timedelta

from app.core.auth import get_current_user
from app.core.deps import get_lesson_service
from app.core.exceptions import DomainError
from app.services.lesson_service import LessonService
from app.schemas.lesson import LessonResponse, LessonCreateRequest, LessonUpdateRequest

lessons_router = APIRouter(tags=["lessons"], dependencies=[Depends(get_current_user)])

def parse_date(date_str: str, field_name: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%d-%m-%y")
    except ValueError:
        raise DomainError(f"{field_name} must be in format DD-MM-YY")

@lessons_router.post("/lessons",
                     response_model=LessonResponse, status_code=201,
                     description="Creates a lesson for the given student according to instrument and time."
                                 "Date must be in the format DD-MM-YY HH:MM."
                                 "Duration must be 30 or 60.")
async def create_lesson(
    body: LessonCreateRequest,
    service: LessonService = Depends(get_lesson_service),
) -> LessonResponse:
    return service.schedule_lesson(body)

@lessons_router.get("/lessons",
                    response_model=list[LessonResponse],
                    description="Returns a list of lessons according to selected criteria."
                                "Dates must be in DD-MM-YY format.")
async def get_lessons(
        student_email: str | None = None,
        instrument: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
        service: LessonService = Depends(get_lesson_service)
):
    dt_from = parse_date(date_from, "date_from") if date_from is not None else None
    dt_to = parse_date(date_to, "date_to") + timedelta(days=1) if date_to is not None else None

    return service.get_lessons(student_email, instrument, dt_from, dt_to, offset, limit)


@lessons_router.put(
    "/lessons/{lesson_id}",
    response_model=LessonResponse,
    description="Updates an existing lesson."
                "Date must be in the format DD-MM-YY HH:MM."
                "Duration must be 30 or 60."
)
async def update_lesson(
        lesson_id: int,
        body: LessonUpdateRequest,
        service: LessonService = Depends(get_lesson_service)
):
    return service.update_lesson(lesson_id, body)

@lessons_router.get(
    "/lessons/{lesson_id}",
    response_model=LessonResponse,
    description="Fetches a lesson by lesson_id."
)
async def get_lesson(
        lesson_id: int,
        service: LessonService = Depends(get_lesson_service)
):
    return service.get_lesson(lesson_id)
