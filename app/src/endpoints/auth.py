import datetime
from typing import Optional

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from src import crud, schemas
from src.config import get_db, simple_send

router = APIRouter(
    prefix="/auth",
)

class EmailUser(BaseModel):
    email: str

class UserAuth(BaseModel):
    email: str
    password: str


class ChangePasswordUser(BaseModel):
    password: str
    newPassword: str

class ChangeUser(BaseModel):
    name: str
    numCRM: str
    telephone: Optional[str]

def get_current_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
	Authorize.jwt_required()
	user_id = Authorize.get_jwt_subject()
	user = crud.get_user(db, user_id)
	if user is None:
		raise MissingTokenError(400, "Credencial inválida")

	return user

@router.post('/login'
             )
def login(user: UserAuth, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    userDatabase = crud.get_user_by_email(db, email=user.email)

    if userDatabase is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.email != userDatabase.email or bcrypt.hashpw(user.password.encode('utf8'), userDatabase.password)!= userDatabase.password:
        raise HTTPException(status_code=401,detail="Bad username or password")

    expires = datetime.timedelta(days=2)
    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=userDatabase.id, expires_time= expires)
    print(userDatabase)
    user = {
        "id": userDatabase.id,
        "email": userDatabase.email,
        "name": userDatabase.name,
        "avatar": userDatabase.avatar,
        "numCRM": userDatabase.numCRM,
        "telephone": userDatabase.telephone,
        "access_token": access_token
    }
    return user


@router.post("/register",
             response_model=schemas.User)
def create_user(userRequest: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=userRequest.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=userRequest)

from fastapi import Request
@router.post("/forgot-password",
             response_model=schemas.User)
async def send_email_forgot_password(email: EmailUser, request: Request, db: Session = Depends(get_db)):
    print(request.url.hostname, request.url.port)
    adress = 'http://{}:{}'.format(request.url.hostname, request.url.port)
    db_user = crud.get_user_by_email(db, email=email.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exists")

    newRandomToken = crud.update_token_reset_password(db, email=email.email)
    content = await simple_send("riantal@gmail.com", newRandomToken, adress)
    return JSONResponse(content=content)

@router.get("/reset-password/")
async def send_reset_password(email: str, token_reset_password:str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not exists")

    if db_user.token_reset_password is None:
        raise HTTPException(status_code=404, detail="Actual token not reseted")

    if db_user.email != email or db_user.token_reset_password != token_reset_password:
        return JSONResponse(status_code=400, detail={"message": "Invalid token"})

    newPassword = crud.update_reset_password(db, email)
    return HTMLResponse(content="<html><body><p>Sua nova senha é: {}</p></body></html>".format(newPassword))

@router.post("/change-password/",
            )
async def change_password(changePasswordUserData: ChangePasswordUser,
                                     current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=current_user.id)

    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não existe")
    if (not changePasswordUserData.password) or (not changePasswordUserData.newPassword):
        raise HTTPException(status_code=400, detail="Senha é obrigatória")
    print(changePasswordUserData.password, changePasswordUserData.newPassword)

    if bcrypt.hashpw(changePasswordUserData.password.encode('utf8'), user.password) != user.password:
        raise HTTPException(status_code=401, detail="Senha errada")

    crud.change_password_user(db, email=user.email, newPassword=changePasswordUserData.newPassword)
    return JSONResponse(content={"detail": "Senha alterada com sucesso"})


@router.post("/change-user/"
            )
async def change_user(changeUserData: ChangeUser,
                                     current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=current_user.id)

    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não existe")

    crud.change_data_user(db, email=user.email, name=changeUserData.name, numCRM=changeUserData.numCRM, telephone=changeUserData.telephone)
    return JSONResponse(content={"detail": "Usuário alterado com sucesso"})

@router.get('/check-user',
             response_model=schemas.UserBaseWithId)
def check_user(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    userDatabase = crud.get_user_by_email(db=db, email=current_user.email)
    return userDatabase