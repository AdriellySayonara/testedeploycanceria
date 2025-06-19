import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from database import Base

class ClassifierEnum(enum.Enum):
    savedmodel = "savedmodel"
    h5 = "h5"
    tensorflow_scikit = "tensorflow+scikit"

class Classifier(Base):
    __tablename__ = "classifier"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String)
    labels = Column(String, nullable=True)
    type = Column(Enum(ClassifierEnum))
    created_at = Column(DateTime(timezone=False), server_default=func.now())

