from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson import LessonCreateRequest, LessonResponse
from datetime import datetime, timedelta
from app.core.exceptions import DomainError


class LessonService:

    def __init__(self, lesson_repo: LessonRepository):
        self.lesson_repo = lesson_repo

    def schedule_lesson(self, body: LessonCreateRequest) -> LessonResponse:
        lessons = self.lesson_repo.get_lessons(body.student_email, body.instrument)

        if body.duration not in (30, 60):
            raise DomainError("Invalid duration: must be 30 or 60")

        dt = datetime.strptime(body.date, "%d-%m-%y %H:%M")
        new_start = dt
        new_end = dt + timedelta(minutes=body.duration)

        for lesson in lessons:
            existing_start = lesson.datetime
            existing_end = lesson.datetime + timedelta(minutes=lesson.duration)

            if new_start < existing_end and new_end > existing_start:
                raise DomainError("Lesson conflict: overlapping lesson exists")

        lesson = self.lesson_repo.create_lesson(
            body.student_email,
            body.instrument,
            dt,
            body.duration
        )

        return lesson

    def get_lessons(self, student_email, instrument, date_from, date_to, offset, limit):

        if date_from is not None and date_to is not None:
            if date_from >= date_to:
                raise DomainError("date_from must be earlier than date_to")

        return self.lesson_repo.get_lessons(
            student_email,
            instrument,
            date_from,
            date_to,
            offset,
            limit
        )

