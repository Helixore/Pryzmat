from models.stubs import StudentStub
from pydantic import BaseModel
from typing import List, Optional

class StudentClassCreate(BaseModel):
    year: int
    symbol: str
    teacher_id: int | None = None

class StudentClassUpdate(BaseModel):
    year: int | None = None
    symbol: str | None = None
    teacher_id: int | None = None

class StudentClassView(BaseModel):
    id: int
    year: int
    symbol: str
    teacher_id: int | None = None
    students: List[StudentStub] | None = None