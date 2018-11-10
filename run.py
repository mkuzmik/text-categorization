from flask import Flask
from flask_restful import Api

from app.main.data.controller import DownloadController, MigrationController, LabeledContentController
from app.main.predicting.controller import PredictCategoryController

app = Flask(__name__)
api = Api(app)

api.add_resource(PredictCategoryController, '/predict')
api.add_resource(DownloadController, '/data/download')
api.add_resource(MigrationController, '/data/migration')
api.add_resource(LabeledContentController, '/data/labeled-content')

if __name__ == '__main__':
    app.run(debug=True)
