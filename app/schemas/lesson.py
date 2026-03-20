from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class LessonCreateRequest(BaseModel):
    student_email: EmailStr
    instrument: str
    date: str
    duration: int

    model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "student_email": "joe@bloggs.com",
                    "instrument": "piano",
                    "date": "20-03-26 14:00",
                    "duration": 30,
                }
            }
    )

class LessonResponse(BaseModel):
    id: int
    student_email: EmailStr
    instrument: str
    datetime: datetime
    duration: int

class LessonUpdateRequest(BaseModel):
    date: str
    duration: int
    instrument: str