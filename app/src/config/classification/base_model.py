from abc import abstractmethod


class BaseModel:
    def __init__(self, path, name, labels):
        self.name = name
        self.labels = labels
        self.model = self.load_model(path=path)

    @abstractmethod
    def load_model(self, path):
        pass

    @abstractmethod
    def pre_process(self, image_path):
        pass

    @abstractmethod
    def decode_prediction(self, path):
        pass

    @abstractmethod
    def classify(self, image_path):
        pass