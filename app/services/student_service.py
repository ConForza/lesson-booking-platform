import logging
from app.core.exceptions import DomainError
from app.repositories.lesson_repository import LessonRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.remaining_lessons import RemainingLessonsResponse, RemainingLessonsRequest
from app.schemas.student import StudentRequest, StudentResponse, CreateStudentRequest, UpdateStudentRequest

logger = logging.getLogger(__name__)

class StudentService:

    def __init__(self, lesson_repo: LessonRepository, student_repo: StudentRepository):
        self.lesson_repo = lesson_repo
        self.student_repo = student_repo

    def construct_student_response(self, student) -> StudentResponse:
        return StudentResponse(
            student_email=student.student_email,
            first_name=student.first_name,
            surname=student.surname,
            instrument=student.instrument,
        )

    def get_remaining_lessons(self, body: RemainingLessonsRequest) -> RemainingLessonsResponse:
        if body.student_email.strip() == "":
            raise DomainError("student_email must not be left blank")
        if body.instrument.lower().strip() != "piano":
            raise DomainError("Instrument is not supported")

        lessons = self.lesson_repo.get_lessons(body.student_email, body.instrument)

        if not lessons:
            logger.warning("No lessons found for %s (%s)", body.student_email, body.instrument)
            raise DomainError("No lessons found", status_code=404)

        lessons_30 = [l for l in lessons if l.duration == 30]
        lessons_60 = [l for l in lessons if l.duration == 60]

        return RemainingLessonsResponse(
            student_email=body.student_email,
            instrument=body.instrument,
            lessons_30=len(lessons_30),
            lessons_60=len(lessons_60),
        )

    def get_student(self, body: StudentRequest) -> StudentResponse:
        if body.student_email.strip() == "":
            logger.warning("Blank student email input")
            raise DomainError("student_email must not be left blank")

        student = self.student_repo.get_student_by_email(body.student_email)

        if student is not None:
            return self.construct_student_response(student)
        else:
            logger.warning("Student not found with email %s", body.student_email)
            raise DomainError("Student not found", status_code=404)

    def create_student(self, body: CreateStudentRequest) -> StudentResponse:
        if body.student_email.strip() == "":
            logger.warning("Blank student email input")
            raise DomainError("student_email must not be left blank")

        if self.student_repo.get_student_by_email(body.student_email) is not None:
            logger.warning("Cannot create student with email %s: student already exists", body.student_email)
            raise DomainError("Student already exists", status_code=400)
        else:
            student = self.construct_student_response(body)

            self.student_repo.create_student(student)
            logger.info("Student created with email %s", body.student_email)
            return student

    def list_students(self, instrument: str | None = None) -> list[StudentResponse]:
        students = self.student_repo.list_students(instrument)

        return [self.construct_student_response(student) for student in students]

    def delete_student(self, body: StudentRequest) -> None:
        if body.student_email.strip() == "":
            logger.warning("Blank student email input")
            raise DomainError("student_email must not be left blank")

        if self.student_repo.get_student_by_email(body.student_email) is None:
            logger.warning("Student not found with email %s", body.student_email)
            raise DomainError("Student not found", status_code=404)

        self.student_repo.delete_student(body.student_email)
        logger.info("Student deleted with email %s", body.student_email)

    def update_student(self, email: str, body: UpdateStudentRequest) -> StudentResponse:
        if email.strip() == "":
            logger.warning("Blank student email input")
            raise DomainError("student_email must not be left blank")

        existing = self.student_repo.get_student_by_email(email)
        if existing is None:
            logger.warning("Student not found with email %s", email)
            raise DomainError("Student not found", status_code=404)

        updated = StudentResponse(
            student_email=email,
            first_name=body.first_name,
            surname=body.surname,
            instrument=body.instrument,
        )

        self.student_repo.update_student(email, updated)
        logger.info("Student updated with email %s", email)
        return updated
