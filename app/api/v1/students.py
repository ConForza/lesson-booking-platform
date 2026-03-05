from fastapi import APIRouter, Depends

from app.core.deps import get_student_service
from app.schemas.student import StudentRequest, StudentResponse, CreateStudentRequest, UpdateStudentRequest
from app.services.student_service import StudentService
from app.schemas.remaining_lessons import RemainingLessonsResponse, RemainingLessonsRequest

students_router = APIRouter(tags=["students"])


@students_router.get(
    "/students/{student_email}",
    response_model=StudentResponse,
    summary="Get a student's record",
    description="Returns the student's first name, surname and instrument for the given email. "
                "Student email must not be left blank."
)
async def get_student_record(
        student_email: str,
        service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    return service.get_student(
        StudentRequest(
            student_email=student_email,
        )
    )

@students_router.get(
    "/students",
    response_model=list[StudentResponse],
    summary="Get a list of all students",
    description="Fetches a list of all student's records"
)
async def get_all_students(
        instrument: str | None = None, service: StudentService = Depends(get_student_service)) -> list[StudentResponse]:
    return service.list_students(instrument)

@students_router.post(
    "/students",
    response_model=StudentResponse,
    summary="Create a new student record",
    description="Creates and stores a new student record."
)
async def create_student(
        body: CreateStudentRequest,
        service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    return service.create_student(body)

@students_router.post(
    "/students/remaining-lessons",
    response_model=RemainingLessonsResponse,
    summary="Calculate remaining lessons for a student",
    description="Returns the number of remaining 30-minute and 60-minute lessons for a given student and instrument. "
                "Currently supports piano only. student_email must not be left blank."
)
async def remaining_lessons(
        body: RemainingLessonsRequest,
        service: StudentService = Depends(get_student_service)
) -> RemainingLessonsResponse:
    return service.get_remaining_lessons(body)


@students_router.get(
    "/students/{student_email}/remaining-lessons",
    response_model=RemainingLessonsResponse,
    summary = "Get remaining lessons for a student",
    description = "Returns the number of lessons for a student using path and query parameters. "
              "Currently supports piano only. student_email must not be left blank."
)
async def get_remaining_lessons(student_email: str, instrument: str,
                                service: StudentService = Depends(get_student_service)) -> RemainingLessonsResponse:
    return service.get_remaining_lessons(
        RemainingLessonsRequest(
            student_email=student_email,
            instrument=instrument,
        )
    )

@students_router.delete(
    "/students/{student_email}",
    summary="Delete a student record",
    description="Deletes a student by email."
)
async def delete_student(
    student_email: str,
    service: StudentService = Depends(get_student_service)
):
    service.delete_student(StudentRequest(student_email=student_email))
    return {"detail": "Student deleted successfully"}

@students_router.put(
    "/students/{student_email}",
    response_model=StudentResponse,
    summary="Update a student record",
    description="Updates an existing student's first name, surname, and instrument."
)
async def update_student(
        student_email: str,
        body: UpdateStudentRequest,
        service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    return service.update_student(student_email, body)
