import json
from pprint import pprint
from collections import Counter

import requests
from bs4 import BeautifulSoup

# WATCH OUT sports -> sport
LABELS = ['business', 'sports', 'politics', 'technology', 'entertainment']


def load_seed_file(filename):
    resources_filename = './resources/seeds/' + filename
    try:
        with open(resources_filename) as f:
            return json.load(f)
    except IOError:
        print('ERROR: Cannot open file {}'.format(resources_filename))


def extract_content(url):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        story_body = soup.find("div", {"property": "articleBody"})
        if story_body is None:
            story_body = soup.find("div", {"id": "story-body"})
        text_parts = [i.get_text() for i in story_body.findAll("p")]
        return " ".join(text_parts)
    except:
        print('ERROR: Cannot extract content from {}'.format(url))


def extract_label(url):
    label_dic = {}
    for llb in LABELS:
        label_dic[llb] = [llb, llb[:-1]]

    for label in label_dic:
        for label_part in label_dic[label]:
            if label_part in url:
                return label

    raise Exception("No label found in {}".format(url))


def save_generated_data(seed_file_name, data):
    filename = "./resources/generated/generated_" + seed_file_name
    with open(filename, 'w') as file:
        file.write(json.dumps(data))


if __name__ == '__main__':
    seed_file = 'generated_seed.json'
    seeds = load_seed_file(seed_file)
    labels_list = []
    data_list = []

    print('Building test data, {} urls found', len(seeds))
    processed = 0

    for seed_url in seeds:
        label = extract_label(seed_url)
        labels_list += [label]
        content = extract_content(seed_url)
        if content is None or len(content) < 20:
            continue
        data_list += [
            {
                'url': seed_url,
                'content': content,
                'label': label
            }
        ]
        processed += 1
        print("{}/{} articles fetched".format(processed, len(seeds)))

    save_generated_data(seed_file, data_list)
    pprint(Counter(labels_list))
