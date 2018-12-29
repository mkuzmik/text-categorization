from flask_restful import Resource
from flask_restful import reqparse

from app.main.predicting.learing.registry import PredictorContainer


class PredictCategoryController(Resource):

    @staticmethod
    def path():
        return '/classify'

    def post(self):
        # alias for get method
        return self.get()

    def get(self):
        """
        Parameters:
            q: text input that you want to predict
            size: learning data set size
            model: choosen learing model ('naive-bayes', 'svm')
        """
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        parser.add_argument('size')
        parser.add_argument('model')
        args = parser.parse_args()
        predicted_label = PredictorContainer.resolve(args.model).predict(args.q, int(args.size))
        return {
            'label': predicted_label
        }

