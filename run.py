from flask import Flask
from flask_restful import Api

from app.main.controller import MainController

app = Flask(__name__)
api = Api(app)

api.add_resource(MainController, '/')

if __name__ == '__main__':
    app.run(debug=True)
