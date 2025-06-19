from ast import literal_eval

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from src import crud, schemas
from src.config import classify, generate_exam_pdf
from src.config import get_db

from celery import Celery

# create celery application
celery_app = Celery(
    "celery",
    backend="redis://redis:6379",
    broker="redis://redis:6379",
)


def get_current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()
	user_id = Authorize.get_jwt_subject()
	user = crud.get_user(db, user_id)
	if user is None:
		raise MissingTokenError(400, "Credencial inválida")

	return user


router = APIRouter(
	prefix="/exams"
)



@router.post('/')
def create_exam_for_user(exam: schemas.ExamBase,
							db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):
	if not crud.get_patients_by_id(db=db, id = exam.patient_id):
		raise HTTPException(status_code=400, detail="Invalid Patient Id")


	db_item = crud.create_exam(db=db, exam=exam, user_id=current_user.id)
	crud.update_patient_last_exam(db=db, id=exam.patient_id)
	#classify.delay(db_item.id, 1)
	task_name = "hello.task"
    # send task to celery
	task = celery_app.send_task(task_name, args=[db_item.id, 1])
	return db_item.id

@router.get('/{id}')
def get_exam_by_id(id:int, db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):
	db_item = crud.get_exam_by_id(db=db, id=id)
	if not db_item:
		raise HTTPException(status_code=400, detail="Exam Not exists")
	if current_user.id != db_item.owner_id:
		raise HTTPException(status_code=400, detail="Invalid Exam Id")

	return db_item


@router.get('/download/{id}')
def get_exam_by_id(id:int, db: Session = Depends(get_db),
							current_user: schemas.User = Depends(get_current_user)):
	exam = crud.get_exam_by_id(db=db, id=id)

	if not exam:
		raise HTTPException(status_code=400, detail="Exam Not exists")
	if current_user.id != exam.owner_id:
		raise HTTPException(status_code=400, detail="Invalid Exam Id")

	if not exam.result:
		raise HTTPException(status_code=400, detail="Não existe exame")

	classifier = crud.get_classifier_by_id(db=db, id=exam.classifier_id)
	patient = crud.get_patients_by_id(db=db, id=exam.patient_id)

	report_data = {
		"patient_name": patient.name,
		"patient_numSUS": patient.numSUS,
		"patient_dataNasc": patient.dataNasc.strftime("%d/%m/%Y"),
		"patient_obs": patient.obs,
		"classifier_name": classifier.name,
		"exam_title": exam.title,
		"exam_image": exam.image,
		"exam_label": literal_eval(exam.result).get('label', ''),
		"exam_result": exam.result,
	}

	filepath = generate_exam_pdf(report_data)

	if not filepath:
		raise HTTPException(status_code=400, detail="Não foi possivel gerar o exame")

	return FileResponse(path=filepath, filename=exam.image.replace("jpg","pdf"))