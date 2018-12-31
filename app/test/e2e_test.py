import json
import time
from json import JSONDecodeError
from pprint import pprint

import requests

URL = 'http://localhost:5000/classify'
METHOD = 'POST'


def load_json_safely(serialized):
    try:
        return json.loads(serialized)
    except JSONDecodeError:
        print('ERROR: cannot deserialize json: {}'.format(serialized))
        return {
            'label': 'server error'
        }


def predict(content, model, dataset_size):
    req = requests.request(METHOD, URL,
                           data={'q': content, 'model': model, 'size': dataset_size})
    response_data = load_json_safely(req.text)
    return response_data['label']


def load_test_data(filename):
    resources_filename = './resources/' + filename
    try:
        with open(resources_filename) as f:
            return json.load(f)
    except IOError:
        print('ERROR: Cannot open file {}'.format(resources_filename))


def load_and_validate(filename):
    loaded_data = load_test_data(filename)
    for entity in loaded_data:
        if not (isinstance(entity['content'], str) and isinstance(entity['label'], str)):
            print('ERROR: Invalid test data entity found: {}'.format(entity))
            raise Exception()
    return loaded_data


def perform_test(data, model, dataset_size):
    result = {
        'test_cases': len(data),
        'passed': 0,
        'failed': 0,
        'fail_info': [],
        'test_params': {
            'model': model,
            'dataset_size': dataset_size
        }
    }

    start_time = time.time()

    for entity in data:
        predicted_label = predict(entity['content'], model, dataset_size)
        if entity['label'] == predicted_label:
            result['passed'] += 1
        else:
            result['failed'] += 1
            result['fail_info'] += [
                {
                    'content': entity['content'][:50],
                    'expected_label': entity['label'],
                    'actual_label': predicted_label
                }
            ]

    end_time = time.time()

    result['execution_time'] = end_time - start_time

    with open("./test_results_shortened.json", "a") as myfile:
        myfile.write('\n' + json.dumps(result))

    return result


if __name__ == '__main__':
    data = load_and_validate('generated/generated_generated_seed.json')

    models = [
        'naive-bayes',
        'svm',
        'k-neighbours'
    ]

    sizes = [
        10,
        50,
        100,
        200,
        500,
        1000,
        2000
    ]

    for model in models:
        for size in sizes:
            pprint(perform_test(data, model, size))

