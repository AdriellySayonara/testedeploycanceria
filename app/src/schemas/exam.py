from pydantic import BaseModel

class ExamBase(BaseModel):
    patient_id: int
    title: str
    image: str
    obs: str
    classifier_id: int

class Exam(ExamBase):
    id: int
    result: str
    created_at: str
