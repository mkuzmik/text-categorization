from flask_restful import Resource
from app.main.category_predicting import Predicter
from flask_restful import reqparse


class PredictCategoryController(Resource):
    def __init__(self):
        self.predicter = Predicter(['business', 'sports', 'politics', 'technology', 'entertainment', 'startup'], 20)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        args = parser.parse_args()
        return self.predicter.predict(args.q)
