from sqlalchemy import update
from sqlalchemy.orm import Session

from src import models
from src import schemas

def create_exam(db: Session, exam: schemas.ExamBase, user_id: int):
	db_item = models.Exam(**exam.dict(), owner_id=user_id)
	db.add(db_item)
	db.commit()
	db.refresh(db_item)
	return db_item

def get_exam_by_id(db: Session, id: int)->schemas.Exam:
	return db.query(models.Exam).get(id)

def get_exam_by_patient_id(db: Session, patient_id: int)->schemas.Exam:
	return db.query(models.Exam).filter(models.Exam.patient_id==patient_id).all()

def update_exam_result_by_id(db: Session, id: int, result: str )->schemas.Exam:
	db.execute(update(models.Exam).where(models.Exam.id == id)
			   .values(result=result))
	db.commit()
