from flask_restful import Resource, reqparse

from app.main.data.data_service import DataServiceContainer
from app.main.data.repository import LabeledContentRepositoryContainer


class DownloadController(Resource):

    @staticmethod
    def path():
        return '/data/download'

    def __init__(self):
        self.data_service = DataServiceContainer.instance
        self.parser = reqparse.RequestParser()

    def get(self):
        """
        Fetches labeled content from given source
        Args:
        source - source of data (ex 'inshorts')
        count - items count per category (ex 123)

        :return: Fetched labeled content
        """
        self.parser.add_argument('source')
        self.parser.add_argument('count')
        args = self.parser.parse_args()
        return self.data_service.fetch(args['source'], int(args['count']))


class MigrationController(Resource):

    @staticmethod
    def path():
        return '/data/migration'

    def __init__(self):
        self.data_service = DataServiceContainer.instance
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('source')
        self.parser.add_argument('count')
        args = self.parser.parse_args()
        self.data_service.migrate_to_db(args['source'], int(args['count']))
        return '', 201


class LabeledContentController(Resource):

    @staticmethod
    def path():
        return '/data/labeled-content'

    def __init__(self):
        self.repository = LabeledContentRepositoryContainer.instance

    def get(self):
        """
        Returns labeled content table content from repository
        """
        return self.repository.scan()
