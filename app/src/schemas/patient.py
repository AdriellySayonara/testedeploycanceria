from typing import  Optional

from pydantic import BaseModel
from pydantic.types import date


class PatientBase(BaseModel):
    id: Optional[int]
    name: str
    #avatar: str
    dataNasc: date
    numSUS: str
    address: Optional[str]
    telephone: Optional[str]
    obs: Optional[str]
