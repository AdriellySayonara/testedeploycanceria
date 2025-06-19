from fastapi import APIRouter, Depends
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
	prefix="/classifiers"
)


@router.get('/')
def list_models(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
	return crud.get_classifiers(db=db)


@router.post('/')
def create_patient_for_user(patient: schemas.PatientBase,
							db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):

	return crud.create_patient(db=db, patient=patient, user_id=current_user.id)
