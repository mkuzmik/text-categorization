import logging


class Config(object):
    # runtime properties
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG

    # dynamo db properties
    DYNAMO_DB = {
        'endpoint_url': 'http://192.168.99.100:8000',
        'region_name': 'us-west-1',
        'aws_access_key_id': 'whatever',
        'aws_secret_access_key': 'whatever'
    }
