from sqlalchemy.orm import Session

from src import models
from src import schemas


def create_classifier(db: Session, classifier: schemas.ClassifierBase):
	db_item = models.Classifier(**classifier.dict())
	db.add(db_item)
	db.commit()
	db.refresh(db_item)
	return db_item

def get_classifier_by_id(db: Session, id: int)->schemas.Classifier:
	return db.query(models.Classifier).get(id)

def get_classifiers(db: Session):
	return db.query(models.Classifier).all()