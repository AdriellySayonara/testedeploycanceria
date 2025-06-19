from sqlalchemy import Date, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    avatar = Column(String, nullable=True)
    name = Column(String)
    dataNasc = Column(Date)
    numSUS = Column(String, index=True)
    address = Column(String, nullable=True,)
    telephone = Column(String, nullable=True,)
    obs = Column(String, nullable=True,)
    lastExam = Column(DateTime, nullable=True,default=None)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="patients")

    exams = relationship("Exam", back_populates="patient")
