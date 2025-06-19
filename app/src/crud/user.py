import uuid

import bcrypt
from sqlalchemy import update
from sqlalchemy.orm import Session

from src import models
from src import schemas


def get_user(db: Session, user_id: int):
	return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
	return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
	fake_hashed_password = bcrypt.hashpw(user.password.encode('utf8'), bcrypt.gensalt())
	db_user = models.User(email=user.email,
						  password=fake_hashed_password,
						  numCRM=user.numCRM,
						  name=user.name,
						  avatar=user.avatar,
						  telephone= user.telephone
						  )
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def update_user_avatar(db: Session, id, newAvatar):
	db.execute(update(models.User).where(models.User.id == id)
			   .values(avatar=newAvatar))
	db.commit()
	return newAvatar

def update_token_reset_password(db: Session, email):
	newRandomToken = str(uuid.uuid4())
	db.execute(update(models.User).where(models.User.email == email)
			   .values(token_reset_password=newRandomToken))
	db.commit()
	return newRandomToken

def change_password_user(db: Session, email , newPassword):
	fake_hashed_password = bcrypt.hashpw(newPassword.encode('utf8'), bcrypt.gensalt())
	db.execute(update(models.User).where(models.User.email == email)
			   .values(password=fake_hashed_password))
	db.commit()

def change_data_user(db: Session, email , name, numCRM,telephone):
	db.execute(update(models.User).where(models.User.email == email)
			   .values(name=name,numCRM=numCRM,telephone= telephone))
	db.commit()


def update_reset_password(db: Session, email):
	newPassword = str(uuid.uuid4())[0:6]
	fake_hashed_password = bcrypt.hashpw(newPassword.encode('utf8'), bcrypt.gensalt())
	db.execute(update(models.User).where(models.User.email == email)
			   .values(password=fake_hashed_password, token_reset_password=None))
	db.commit()
	return newPassword
