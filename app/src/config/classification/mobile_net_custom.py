import os

from src.config.classification import BaseModel
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet import preprocess_input


class MobileNetCustom(BaseModel):
    def load_model(self, path):
        model = keras.models.load_model(os.path.join('modelsFiles', path))
        return model

    def pre_process(self, image_path):
        my_image = load_img(os.path.join('privateFiles', image_path),
                            target_size=(224, 224))
        my_image = img_to_array(my_image)
        my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
        my_image = preprocess_input(my_image)
        return my_image

    def decode_prediction(self, predict):
        array_predict = np.around(predict.reshape(2), decimals=4).tolist()
        label = self.labels[np.argmax(predict.reshape(2))]
        return {"array_predict": array_predict, "label":label}

    def classify(self, image_path):
        my_image = self.pre_process(image_path)
        predict = self.model.predict(my_image)
        return self.decode_prediction(predict)