from flask_restful import Resource
from flask_restful import reqparse

from app.main.predicting.predictor import PredictorContainer


class PredictCategoryController(Resource):

    @staticmethod
    def path():
        return '/predict'

    def __init__(self):
        self.predictor = PredictorContainer.instance()

    def get(self):
        """
        Parameters:
            q: text input that you want to predict
            size: learning data set size
        """
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        parser.add_argument('size')
        args = parser.parse_args()
        return self.predictor.predict(args.q, int(args.size))
