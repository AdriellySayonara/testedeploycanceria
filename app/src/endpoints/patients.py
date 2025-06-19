from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.orm import Session

from src import crud, schemas
from src.config import get_db


def get_current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()
	user_id = Authorize.get_jwt_subject()
	user = crud.get_user(db, user_id)
	if user is None:
		raise MissingTokenError(400, "Credencial inválida")

	return user


router = APIRouter(
	prefix="/patients"
)


@router.get('/')
def list_patients(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
	return crud.get_patients_by_user(db=db, user_id=current_user.id)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

@router.get('/{id}')
def get_patient_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
	patient = crud.get_patients_by_id(db=db, id=id)

	exams = crud.get_exam_by_patient_id(db=db, patient_id=id)
	dic = {"patient" : patient, "exams": exams}
	print(dic)

	return dic


@router.post('/')
def create_patient_for_user(patient: schemas.PatientBase,
							db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):

	return crud.create_patient(db=db, patient=patient, user_id=current_user.id)


@router.put('/')
def edit_patient_for_user(patient: schemas.PatientBase,
							db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):
	patientDatabase = crud.get_patients_by_id(db=db, id=patient.id)
	if patientDatabase is None:
		raise HTTPException(status_code=404, detail="Paciente não existe")

	return crud.edit_patient(db=db, patient=patient)
