import os
import datetime
import pdfkit
from src import crud
import database
from src.config.classification import selectModel

import numpy as np
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array

from celery import Celery
from celery.utils.log import get_task_logger  # Initialize celery
from ast import literal_eval

celery = Celery('celery',
				backend="redis://redis:6379",
                broker="redis://redis:6379",)  # Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


def prepare_image(file):
    img = load_img(file, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

@celery.task(name="hello.task", bind=True)
def classify(self, exam_id, classifier_id):
    db = database.SessionLocal()
    try:
        exam = crud.get_exam_by_id(db=db, id=exam_id)
        classifier_db_item = crud.get_classifier_by_id(db=db, id=classifier_id)
        image_path = os.path.join('privateFiles', exam.image)
        print("Started  ID: {}   -  PATH: {}   ".format(exam_id, image_path))

        classifier=selectModel(classifier_db_item.path,classifier_db_item.name,literal_eval(classifier_db_item.labels),classifier_db_item.type)
        results = classifier.classify(exam.image)
        crud.update_exam_result_by_id(db=db, id = exam_id, result=str(results))

        patient = crud.get_patients_by_id(db=db, id=exam.patient_id)

        exam = crud.get_exam_by_id(db=db, id=exam_id)

    except IOError:
        crud.update_exam_result_by_id(db=db, id=exam_id, result="Não foi possível classificar")
        raise Exception("Não possivel classificar")
    finally:
        db.close()

    return results
'''
@celery.task
def classify(exam_id):
    db = database.SessionLocal()
    try:
        exam = crud.get_exam_by_id(db=db, id=exam_id)
        image_path = os.path.join('privateFiles', exam.image)
        print("Started  ID: {}   -  PATH: {}   ".format(exam_id, image_path))

        mobile = tf.keras.applications.mobilenet.MobileNet()
        preprocessed_image = prepare_image(image_path)
        predictions = mobile.predict(preprocessed_image)
        results = imagenet_utils.decode_predictions(predictions)
        crud.update_exam_result_by_id(db=db, id = exam_id, result=str(results))
    except IOError:
        crud.update_exam_result_by_id(db=db, id=exam_id, result="Não foi possível classificar")
        raise Exception("Não possivel classificar")
    finally:
        db.close()

    return results
'''