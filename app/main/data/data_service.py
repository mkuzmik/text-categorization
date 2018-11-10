import dependency_injector.containers as containers
import dependency_injector.providers as providers

from app.main.data.dynamo_db import DynamoDbContainer
from app.main.data.inshorts_downloader import InshortsDownloaderContainer


class DataService(object):
    def __init__(self, dynamo_connection, inshorts_downloader):
        self.dynamo_connection = dynamo_connection
        self.inshorts_downloader = inshorts_downloader

    def fetch(self, source, items_per_cat):
        """
        :param source: source of data
        :param items_per_cat: amount of items to fetch per every category
        :return: fetched items
        """
        if source == 'inshorts':
            return self.inshorts_downloader.download(items_per_cat)
        else:
            raise Exception('Unknown source')

    def migrate_to_db(self, source, items_per_cat):
        """
        Fetches items from given source, of given amount and writes it to db.
        """
        data = self.fetch(source, items_per_cat)
        self.store(data)

    def store(self, data):
        """
        Writes given data into dynamo db
        :param data: list of objects { label, content }
        """
        table = self.dynamo_connection.labeled_content

        for entity in data:

            # Watch out! Getting stack overflow without casting (deepcopy issue)
            # https://github.com/amzn/ion-python/issues/61
            label = str(entity['label'])
            content = str(entity['content'])

            table.put_item(
                Item={
                    'label': label,
                    'content': content
                }
            )


class DataServiceContainer(containers.DeclarativeContainer):
    instance = providers.Singleton(DataService,
                                   dynamo_connection=DynamoDbContainer.instance(),
                                   inshorts_downloader=InshortsDownloaderContainer.instance())
