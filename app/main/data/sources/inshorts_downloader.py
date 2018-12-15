import json
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from flask import current_app as app


class InshortsDownloader:

    def download(self, items_per_cat):
        """
        Extracts inshorts only for suggested categories
        (To be honest - category "World" doesn't make much sense)
        :param items_per_cat: items to fetch per category
        """
        suggested_categories = ['business', 'sports', 'politics', 'technology', 'entertainment']

        return self.extract_inshorts(suggested_categories, items_per_cat)

    def extract_inshorts(self, categories, items_per_cat):
        """
        Download stories from https://inshorts.com

        :param categories: list of categories that you want to download
        :param items_per_cat: minimal amount of stories per each category
        :return: list of (story, category) touples
        """
        result = []
        for category in categories:
            app.logger.info("Downloading stories for %s", category)
            labeled = []
            offset = ''
            while len(labeled) < items_per_cat:
                downloaded = self.__download_for(category, offset)
                offset = downloaded['offset']
                labeled += downloaded['stories']
            result += labeled
        return result

    def __download_for(self, category, offset):
        params = 'category=' + category + '&news_offset=' + offset
        resp = self.__request('POST', 'https://inshorts.com/en/ajax/more_news', params)
        obj = self.__load_json_safely(resp)
        parsed_stories = self.__parse_stories_from(obj['html'])
        stories = {'stories': self.__label(parsed_stories, category),
                   'offset': obj['min_news_id']}
        return stories

    def __label(self, stories, category):
        return [{"label": category, "content": story} for story in stories]

    def __parse_stories_from(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        unflattened = [i.contents for i in soup.findAll("div", {"itemprop": 'articleBody'})]
        stories_list = [item for sublist in unflattened for item in sublist]
        return stories_list

    def __request(self, method, url, payload):
        headers = {
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Cache-Control': "no-cache"
        }
        response = requests.request(method, url, data=payload, headers=headers)
        return response.text

    def __load_json_safely(self, serialized):
        try:
            return json.loads(serialized)
        except JSONDecodeError:
            print('ERROR: cannot deserialize json: ' + serialized)


class InshortsDownloaderContainer(object):
    instance = InshortsDownloader()
