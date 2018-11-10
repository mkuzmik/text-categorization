from flask_restful import Resource
from flask_restful import reqparse

from app.main.predicting.predictor import Predictor, PredictorContainer


class PredictCategoryController(Resource):
    """
    /predict
    """

    def __init__(self):
        self.predictor = PredictorContainer.instance()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        args = parser.parse_args()
        return self.predictor.predict(args.q)
