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

        self.content_by_label = self.init_content_by_label()
        self.content_by_source = self.init_content_by_source()
        logger.info('DynamoDB connection ready')

    def table_exists(self, table_name):
        existing_tables = list(self.resource.tables.all())
        return table_name in list(map(lambda x: x.name, existing_tables))

    def init_content_by_label(self):
        return self.init_table(
            table_name='content_by_label',
            key_schema=[
                {
                    'AttributeName': 'label',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'content',
                    'KeyType': 'RANGE'
                }
            ],
            attribute_definitions=[
                {
                    'AttributeName': 'label',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'content',
                    'AttributeType': 'S'
                }

            ]
        )

    def init_content_by_source(self):
        return self.init_table(
            table_name='content_by_source',
            key_schema=[
                {
                    'AttributeName': 'source',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'content',
                    'KeyType': 'RANGE'
                }
            ],
            attribute_definitions=[
                {
                    'AttributeName': 'source',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'content',
                    'AttributeType': 'S'
                }

            ]
        )

    def init_table(self, table_name, key_schema, attribute_definitions):
        if self.table_exists(table_name):
            logger.info('Table %s already exists, skipping creation', table_name)
            return

        logger.info('Creating %s table', table_name)
        self.resource.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        return self.resource.Table(table_name)


class DynamoDbContainer(object):
    instance = DynamoDb()
