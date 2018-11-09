from flask_restful import Resource

from app.main.data.data_service import DataServiceContainer


class DataController(Resource):
    def __init__(self):
        self.data_service = DataServiceContainer.instance()

    def get(self):
        return self.data_service.fetch_inshorts_stories()
