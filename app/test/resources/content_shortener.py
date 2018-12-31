# This script will shortend content of every news to n sentences

import json
import random

shorten_to_sentences = 3
filename = 'generated_generated_seed.json'


if __name__ == '__main__':
    with open('./generated/' + filename, 'r') as file:
        data = json.load(file)

    for entity in data:
        sentences = entity['content'].split('. ')
        shortened = ""
        for i in range(shorten_to_sentences):
            shortened += random.choice(sentences)
        entity['content'] = shortened

    with open('./generated/shortened_' + filename, 'w') as file:
        file.write(json.dumps(data))
