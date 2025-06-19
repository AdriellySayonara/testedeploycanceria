from src.config.classification.base_model import BaseModel
from src.config.classification.mobile_net_custom import MobileNetCustom
from src.models import ClassifierEnum

def selectModel(path, name, labels, type) -> BaseModel:
    if type == ClassifierEnum.savedmodel:
        return MobileNetCustom(path,name,labels)