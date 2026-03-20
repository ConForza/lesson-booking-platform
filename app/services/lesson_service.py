from app.repositories.lesson_repository import LessonRepository
from app.schemas.lesson import LessonCreateRequest, LessonResponse, LessonUpdateRequest
from datetime import datetime, timedelta
from app.core.exceptions import DomainError


class LessonService:

    def __init__(self, lesson_repo: LessonRepository):
        self.lesson_repo = lesson_repo

    def _has_overlap(self, lessons, new_start, new_end):
        for lesson in lessons:
            existing_start = lesson.datetime
            existing_end = lesson.datetime + timedelta(minutes=lesson.duration)

            if new_start < existing_end and new_end > existing_start:
                return True
        return False

    def _validate_duration(self, duration: int):
        if duration not in (30, 60):
            raise DomainError("Invalid duration: must be 30 or 60")

    def _parse_datetime(self, date: str):
        try:
            return datetime.strptime(date, "%d-%m-%y %H:%M")
        except ValueError:
            raise DomainError("date must be in format DD-MM-YY HH:MM")

    def _calculate_time_window(self, dt, duration: int):
        return dt, dt + timedelta(minutes=duration)

    def schedule_lesson(self, body: LessonCreateRequest) -> LessonResponse:
        lessons = self.lesson_repo.get_lessons(body.student_email, body.instrument)

        self._validate_duration(body.duration)

        dt = self._parse_datetime(body.date)
        new_start, new_end = self._calculate_time_window(dt, body.duration)

        if self._has_overlap(lessons, new_start, new_end):
            raise DomainError("Lesson conflict: overlapping lesson exists")

        lesson = self.lesson_repo.create_lesson(
            body.student_email,
            body.instrument,
            dt,
            body.duration
        )

        return lesson

    def get_lessons(self, student_email, instrument, date_from, date_to, offset, limit) -> list[LessonResponse]:

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

    def update_lesson(self, lesson_id: int, body: LessonUpdateRequest) -> LessonResponse:
        existing_lesson = self.lesson_repo.get_lesson_by_id(lesson_id)
        if not existing_lesson:
            raise DomainError("Lesson not found", status_code=404)

        self._validate_duration(body.duration)
        dt = self._parse_datetime(body.date)
        new_start, new_end = self._calculate_time_window(dt, body.duration)
        other_lessons = [l for l in self.get_lessons(
            existing_lesson.student_email, body.instrument, None, None, None, None
        ) if l.id != existing_lesson.id]
        if self._has_overlap(other_lessons, new_start, new_end):
            raise DomainError("Lesson conflict: overlapping lesson exists")

        return self.lesson_repo.update_lesson(lesson_id, body.instrument, dt, body.duration)

    def get_lesson(self, lesson_id):
        return self.lesson_repo.get_lesson_by_id(lesson_id)

