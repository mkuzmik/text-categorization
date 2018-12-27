import requests

from app.main.tools import logging
from config import CONFIG

LOGGER = logging.get_logger('NewsApiDownloader')


class NewsApiDownloader:

    def download(self, items_per_cat):
        """
        Fetch news for suggested_categories from newsa
        :param items_per_cat: items to fetch per category (max 100)
        """

        # TODO: fix items_per_cat
        suggested_categories = ['business', 'sports', 'politics', 'technology', 'entertainment']

        res = []
        for cat in suggested_categories:
            LOGGER.info('Downloading articles for {}'.format(cat))
            res = res + self._get_by_category(cat, items_per_cat)

        return res

    def _get_by_category(self, category, size):
        # TODO configurable source
        endpoint = self.__get_endpoint('everything', category, size)
        resp = requests.get(endpoint)
        if resp.status_code != 200:
            LOGGER.error('Cannot fetch NewsAPI data from {}', endpoint)
        else:
            objects = list(
                map(lambda x: {'source': 'news-api',
                               'label': category,
                               'content': self.filter_content(x['content'])},
                    resp.json()['articles']))
            return list(filter(lambda x: x['content'] != "", objects))

    def __get_endpoint(self, source, category, size):
        return 'https://newsapi.org/v2/{}?q={}&pageSize={}&apiKey={}'.format(source, category, size,
                                                                             CONFIG.SECRETS.NEWS_API_KEY)

    def filter_content(self, content):
        return content.split('[')[0] if content is not None else ""


class NewsApiDownloaderContainer(object):
    instance = NewsApiDownloader()
