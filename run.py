from flask import Flask
from flask_restful import Api

from app.main.data.controller import DataController
from app.main.model.controller import PredictCategoryController

app = Flask(__name__)
api = Api(app)

api.add_resource(PredictCategoryController, '/predict')
api.add_resource(DataController, '/data')

if __name__ == '__main__':
    app.run(debug=True)
