import datetime
from sqlalchemy import update
from sqlalchemy.orm import Session

from src import models
from src import schemas


def create_patient(db: Session, patient: schemas.PatientBase, user_id: int):
	db_item = models.Patient(**patient.dict(), owner_id=user_id)
	db.add(db_item)
	db.commit()
	db.refresh(db_item)
	return db_item

def edit_patient(db: Session, patient: schemas.PatientBase):
	db.execute(update(models.Patient).where(models.Patient.id == patient.id)
			   .values(name= patient.name, numSUS=patient.numSUS, dataNasc= patient.dataNasc))
	db.commit()

def get_patients_by_id(db: Session, id: int):
	return db.query(models.Patient).get(id)

def get_patients_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
	return db.query(models.Patient).filter(models.Patient.owner_id == user_id).offset(skip).limit(limit).all()

def update_patient_last_exam(db: Session, id):
	db.execute(update(models.Patient).where(models.Patient.id == id)
			   .values(lastExam=datetime.datetime.utcnow()))
	db.commit()
