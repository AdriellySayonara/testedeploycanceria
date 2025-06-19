import io
import os
import uuid

from PIL import Image
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
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
	prefix="/images"
)


@router.post("/avatar")
async def create_avatar_image(in_file: UploadFile = File(...)):
	try:
		filename = str(uuid.uuid4()) + ".jpg"
		in_image = await in_file.read()
		image = Image.open(io.BytesIO(in_image))
		image.thumbnail((640, 640), Image.ANTIALIAS)
		image.save(os.path.join('static', filename), "JPEG")
	except:
		raise HTTPException(status_code=400, detail="Invalid file")
	finally:
		await in_file.close()

	return {"filename": filename}


@router.post("/change-avatar")
async def create_avatar_image(in_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user),db: Session = Depends(get_db)):
	try:
		filename = str(uuid.uuid4()) + ".jpg"
		in_image = await in_file.read()
		image = Image.open(io.BytesIO(in_image))
		image.thumbnail((640, 640), Image.ANTIALIAS)
		image.save(os.path.join('static', filename), "JPEG")
		crud.update_user_avatar(db=db, id=current_user.id, newAvatar=filename)
	except:
		raise HTTPException(status_code=400, detail="Invalid file")
	finally:
		await in_file.close()

	return {"filename": filename}

@router.post("/exam")
async def create_exam_image(in_file: UploadFile = File(...), current_user: schemas.User = Depends(get_current_user)):
	try:
		filename = str(current_user.id)+"-" + str(uuid.uuid4()) + ".jpg"
		in_image = await in_file.read()
		image = Image.open(io.BytesIO(in_image))
		# image.thumbnail((640,640), Image.ANTIALIAS)
		image.save(os.path.join('privateFiles', filename), "JPEG", quality=100)
	except:
		raise HTTPException(status_code=400, detail="Invalid file")
	finally:
		await in_file.close()

	return {"filename": filename}


@router.get("/exam/{exam_id}")
def get_exam_image(exam_id, current_user: schemas.User = Depends(get_current_user)):
	if str(exam_id).split('-')[0] != str(current_user.id):
		raise HTTPException(status_code=400, detail="Invalid Credential")
	return FileResponse(path=os.path.join('privateFiles', exam_id), filename=exam_id)

@router.get("/avatar/{avatar_id}")
def get_exam_image(avatar_id, current_user: schemas.User = Depends(get_current_user)):
	return FileResponse(path=os.path.join('static', avatar_id), filename=avatar_id)