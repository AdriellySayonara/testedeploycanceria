import enum
from typing import Optional
from pydantic import BaseModel


class ClassifierBase(BaseModel):
    name: str
    path: str
    labels: Optional[str] = None
    type: enum.Enum

class Classifier(ClassifierBase):
    id: int
    name: str
    created_at: str