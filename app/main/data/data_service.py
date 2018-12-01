from app.main.data.inshorts_downloader import InshortsDownloaderContainer
from app.main.data.repository import LabeledContentRepositoryContainer


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
        if source == 'inshorts':
            return self.inshorts_downloader.download(items_per_cat)
        else:
            raise Exception('Unknown source')

    def migrate_to_db(self, source, items_per_cat):
        """
        Fetches items from given source, of given amount and writes it to db.
        """
        data = self.fetch(source, items_per_cat)
        self.repository.write(data)


class DataServiceContainer(object):
    instance = DataService(repository=LabeledContentRepositoryContainer.instance,
                           inshorts_downloader=InshortsDownloaderContainer.instance)
