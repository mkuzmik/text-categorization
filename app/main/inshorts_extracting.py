import json
from flask import current_app as app
from json import JSONDecodeError

import pandas as pd
import requests
from bs4 import BeautifulSoup

from app.main.pandas_util import PandasUtil


class InshortsDownloader:
    def extract_inshorts(self, categories, min_items):
        """
        Download stories from https://inshorts.com

        :param categories: list of categories that you want to download
        :param min_items: minimal amount of stories per each category
        :return: list of (story, category) touples
        """
        result = []
        for category in categories:
            app.logger.info("Downloading stories for %s", category)
            labeled = []
            offset = ''
            while len(labeled) < min_items:
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


class InshortsDfDownloader(InshortsDownloader):
    def __init__(self):
        self.inshorts_downloader = InshortsDownloader()

    def extract_inshorts(self, categories, min_items):
        data_frame = pd.DataFrame(self.inshorts_downloader.extract_inshorts(categories, min_items))
        return PandasUtil.shuffle(data_frame)
