from app.main.data.sources.inshorts_downloader import InshortsDownloaderContainer
from app.main.data.repository import LabeledContentRepositoryContainer
from app.main.tools import logging

logger = logging.get_logger('DataService')


class DataService(object):
    def __init__(self, repository, inshorts_downloader):
        self.repository = repository
        self.inshorts_downloader = inshorts_downloader

    def fetch(self, source, items_per_cat):
        """
        :param source: source of data
        :param items_per_cat: amount of items to fetch per every category
        :return: fetched items
        """
        logger.debug('Fetching %d items per cat from source %s', items_per_cat, source)
        if source == 'inshorts':
            return self.inshorts_downloader.download(items_per_cat)
        else:
            raise Exception('Unknown source')

    def migrate_to_db(self, source, items_per_cat):
        """
        Fetches items from given source, of given amount and writes it to db.
        """
        data = self.fetch(source, items_per_cat)
        data = self.__attach_source(data, source)
        logger.debug('Migrating %d items to DB', len(data))
        self.repository.write(data)

    def __attach_source(self, data, source):
        for entity in data:
            entity['source'] = source
        return data


class DataServiceContainer(object):
    instance = DataService(repository=LabeledContentRepositoryContainer.instance,
                           inshorts_downloader=InshortsDownloaderContainer.instance)
