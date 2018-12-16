from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from app.main.data.repository import LabeledContentRepositoryContainer
from app.main.predicting.learing.tfidf_predictor import TfidfPredictor
from app.main.predicting.text_processing import TextProcessingContainer
from app.main.predicting.text_transformer import TextTransformerContainer


class PredictorContainer(object):
    instances = {
        'naive-bayes': MultinomialNB,
        'svm': SVC(kernel="linear", C=0.025),
        'k-neighbours': KNeighborsClassifier
    }

    default = instances['naive-bayes']

    @staticmethod
    def resolve(model):
        model_class = PredictorContainer.instances.get(model, PredictorContainer.default)
        return TfidfPredictor(repository=LabeledContentRepositoryContainer.instance,
                              text_processor=TextProcessingContainer.instance,
                              text_transformer=TextTransformerContainer.instance,
                              model=model_class())
