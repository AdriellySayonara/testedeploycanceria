from typing import List, Optional
from pydantic import BaseModel
from src.schemas.patient import PatientBase


class UserBase(BaseModel):
    avatar: Optional[str]
    name: str
    email: str
    numCRM: str
    telephone: Optional[str] = None

class UserBaseWithId(BaseModel):
    id: int
    avatar: Optional[str]
    name: str
    email: str
    numCRM: str
    telephone: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    patients: List[PatientBase] = []

    class Config:
        orm_mode = True

