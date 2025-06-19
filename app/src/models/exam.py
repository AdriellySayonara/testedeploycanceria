from sqlalchemy import  Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Exam(Base):
    __tablename__ = "exam"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image = Column(String)
    result = Column(String, nullable=True)
    obs = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=False), server_default=func.now())
    classifier_id = Column(Integer, ForeignKey("classifier.id"))
    patient = relationship("Patient", back_populates="exams")
    patient_id = Column(Integer, ForeignKey("patients.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="exams")
