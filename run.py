from flask import Flask
from flask_restful import Api

from app.main.data.controller import FetchController, MigrationController
from app.main.model.controller import PredictCategoryController

app = Flask(__name__)
api = Api(app)

api.add_resource(PredictCategoryController, '/predict')
api.add_resource(FetchController, '/data/fetch')
api.add_resource(MigrationController, '/data/migrate')

if __name__ == '__main__':
    app.run(debug=True)
