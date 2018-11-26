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


def load_config():
    if app.config['ENV'] == 'production':
        app.config.from_object('instance.prod.production.ProdConfig')
    else:
        app.config.from_object('instance.dev.development.DevConfig')


if __name__ == '__main__':
    load_config()
    app.run(debug=app.config['DEBUG'])
