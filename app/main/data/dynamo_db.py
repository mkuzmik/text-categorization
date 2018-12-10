import boto3

from app.main.tools import logging
from config import CONFIG

logger = logging.get_logger('DynamoDb')


class DynamoDb(object):

    def __init__(self):
        logger.info('Initializing DynamoDB connection')
        self.resource = boto3.resource('dynamodb',
                                       endpoint_url=CONFIG.DYNAMO_DB['endpoint_url'],
                                       region_name=CONFIG.DYNAMO_DB['region_name'],
                                       aws_access_key_id=CONFIG.DYNAMO_DB['aws_access_key_id'],
                                       aws_secret_access_key=CONFIG.DYNAMO_DB['aws_secret_access_key'])
        self.on_init()

        self.labeled_content = self.resource.Table('labeled_content')
        logger.info('DynamoDB connection ready')

    def on_init(self):
        # TODO get rid of this weird check
        if len(list(self.resource.tables.all())) > 0:
            logger.info('Table labeled_content already exists, skipping creation')
            return

        logger.info('Creating labeled_content table')
        self.resource.create_table(
            TableName='labeled_content',
            KeySchema=[
                {
                    'AttributeName': 'label',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'content',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'label',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'content',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


class DynamoDbContainer(object):
    instance = DynamoDb()
