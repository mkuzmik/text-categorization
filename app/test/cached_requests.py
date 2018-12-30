import json
import requests


class CachedRequest(object):
    def __init__(self):
        self.filename = "./cache/cached_requests"
        self.__init_from_file()
        return

    def __init_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                self.request_cache = json.load(file)
        except:
            self.request_cache = {
                'https://www.example.com': 'Example response'
            }

    def persist(self):
        try:
            with open(self.filename, 'w') as file:
                file.write(json.dumps(self.request_cache))
        except:
            print('ERROR: failed to persist request cache')

    def get(self, url):
        cached_response = self.request_cache.get(url)

        if cached_response is None:
            resp = requests.get(url)
            self.request_cache[url] = resp.text

        return self.request_cache[url]
