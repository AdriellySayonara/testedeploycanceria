from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    avatar = Column(String, nullable=True)
    name = Column(String)
    numCRM = Column(String)
    telephone = Column(String, nullable=True, )
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    token_reset_password = Column(String, default=None)

    patients = relationship("Patient", back_populates="owner")
    exams = relationship("Exam", back_populates="owner")
