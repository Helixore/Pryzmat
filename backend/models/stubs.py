from pydantic import BaseModel, Field

class StudentStub(BaseModel):
    id: int
    student_id: int
    firstName: str
    lastName: str