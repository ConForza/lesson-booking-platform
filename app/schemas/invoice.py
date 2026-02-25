from pydantic import BaseModel
from typing import List

class InvoicePreviewRequest(BaseModel):
    staff_id: int
    date_from: str
    date_to: str
    preview: bool = False

class LessonPreview(BaseModel):
    name: str
    duration: int
    lesson_cut: float
    paid:bool

class InvoicePreviewResponse(BaseModel):
    staff_id: int
    date_from: str
    date_to: str
    preview: bool
    total_amount: float
    lessons: List[LessonPreview]