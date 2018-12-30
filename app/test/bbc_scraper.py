import json
import re
from pprint import pprint
from queue import Queue
from urllib.parse import urlparse

from app.test.cached_requests import CachedRequest
from bs4 import BeautifulSoup

start_urls = [
    'https://www.bbc.com/',
    'https://www.bbc.com/sport'
]

limit_per_pattern = 20

requests = CachedRequest()


def start_queue():
    q = Queue()
    for url in start_urls:
        q.put(url)
    return q


FILTER_PATTERNS = {
    '[^\=]*\/sport\/[a-z]*\/[0-9]*$': 0,
    '[^\=]*\/news\/technology-[0-9]*$': 0,
    '[^\=]*\/news\/entertainment-arts-[0-9]*$': 0,
    '[^\=]*\/news\/business-[0-9]*$': 0,
    '[^\=]*\/news\/.*politics-[0-9]*$': 0
}


def extract_all_hrefs(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True)]


def extract_urls_from(url):
    host = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
    resp = requests.get(url)
    hrefs = extract_all_hrefs(resp)
    return list(map(lambda x: host + x if x[0] == '/' else x, hrefs))


def extract_and_validate_urls_from(url):
    urls = extract_urls_from(url)
    valids = []
    for url in urls:
        for pattern in FILTER_PATTERNS:
            if re.match(pattern, url):
                valids = valids + [{
                    'url': url,
                    'pattern': pattern
                }]
                break
    return valids


def save_generated_data(seed_file_name, data):
    filename = "./resources/seeds/generated_" + seed_file_name
    with open(filename, 'w') as file:
        file.write(json.dumps(data))


def limits_exceeded():
    for pattern in FILTER_PATTERNS:
        if FILTER_PATTERNS[pattern] < limit_per_pattern:
            return False
    return True


if __name__ == '__main__':
    urls = []
    q = start_queue()
    iter = 1
    while not q.empty() and not limits_exceeded():
        for url in start_urls:
            new_urls = extract_and_validate_urls_from(q.get())
            for u in new_urls:
                if u['url'] not in urls and FILTER_PATTERNS[u['pattern']] < limit_per_pattern:
                    urls += [u['url']]
                    FILTER_PATTERNS[u['pattern']] += 1
                    q.put(u['url'])
        pprint(
            {
                "iteration_no": iter,
                "state": FILTER_PATTERNS
            }
        )
        iter += 1

    save_generated_data('seed.json', urls)
    requests.persist()
