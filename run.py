from flask import Flask
from flask_restful import Api

from app.main.data.controller import DownloadController, MigrationController, LabeledContentController
from app.main.predicting.controller import PredictCategoryController

app = Flask(__name__)
api = Api(app)

def add_resource(api, controller):
    api.add_resource(controller, controller.path())
    return


add_resource(api, PredictCategoryController)
add_resource(api, DownloadController)
add_resource(api, MigrationController)
add_resource(api, LabeledContentController)

if __name__ == '__main__':
    app.run(debug=True)
