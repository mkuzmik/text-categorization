import dependency_injector.containers as containers
import dependency_injector.providers as providers

from app.main.data.dynamo_db import DynamoDbContainer
from app.main.data.inshorts_downloader import InshortsDownloaderContainer


class DataService(object):
    def __init__(self, dynamo_connection, inshorts_downloader):
        self.dynamo_connection = dynamo_connection
        self.inshorts_downloader = inshorts_downloader

    def fetch_inshorts_stories(self):
        return self.inshorts_downloader.extract_inshorts(['business', 'sports'], 20)


class DataServiceContainer(containers.DeclarativeContainer):

    instance = providers.Singleton(DataService,
                                 dynamo_connection=DynamoDbContainer.instance(),
                                 inshorts_downloader=InshortsDownloaderContainer.instance())
