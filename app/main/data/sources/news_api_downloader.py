import requests

from app.main.tools import logging
from config import CONFIG

LOGGER = logging.get_logger('NewsApiDownloader')


class NewsApiDownloader:

    def download(self, items_per_cat):
        """
        Fetch news for suggested_categories from newsa
        :param items_per_cat: items to fetch per category
        """
        suggested_categories = ['business', 'sports', 'politics', 'technology', 'entertainment']

        res = []
        for cat in suggested_categories:
            LOGGER.info('Downloading articles for {}'.format(cat))
            res = res + self._get_by_category(cat)

        return res

    def _get_by_category(self, category):
        # TODO configurable source
        endpoint = self.__get_endpoint('everything', category)
        resp = requests.get(endpoint)
        if resp.status_code != 200:
            LOGGER.error('Cannot fetch NewsAPI data from {}', endpoint)
        else:
            return list(map(lambda x: {
                'source': 'news-api',
                'label': category,
                'content': x['content']
            }, resp.json()['articles']))

    def __get_endpoint(self, source, category):
        return 'https://newsapi.org/v2/{}?q={}&apiKey={}'.format(source, category, CONFIG.SECRETS.NEWS_API_KEY)


class NewsApiDownloaderContainer(object):
    instance = NewsApiDownloader()
