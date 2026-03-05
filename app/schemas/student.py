from pydantic import BaseModel, EmailStr

class StudentRequest(BaseModel):
    student_email: str

class StudentResponse(BaseModel):
    student_email: EmailStr
    first_name: str
    surname: str
    instrument: str | None

class Student(BaseModel):
    student_email: str
    first_name: str
    surname: str
    instrument: str | None

class CreateStudentRequest(BaseModel):
    student_email: EmailStr
    first_name: str
    surname: str
    instrument: str

class UpdateStudentRequest(BaseModel):
    first_name: str
    surname: str
    instrument: str