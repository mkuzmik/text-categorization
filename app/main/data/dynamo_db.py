import boto3
import dependency_injector.containers as containers
import dependency_injector.providers as providers
from config import CONFIG


class DynamoDb(object):

    def __init__(self):
        self.resource = boto3.resource('dynamodb',
                                       endpoint_url=CONFIG.DYNAMO_DB['endpoint_url'],
                                       region_name=CONFIG.DYNAMO_DB['region_name'],
                                       aws_access_key_id=CONFIG.DYNAMO_DB['aws_access_key_id'],
                                       aws_secret_access_key=CONFIG.DYNAMO_DB['aws_secret_access_key'])
        self.on_init()

        self.labeled_content = self.resource.Table('labeled_content')

    def on_init(self):
        if len(list(self.resource.tables.all())) > 0:
            return

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


class DynamoDbContainer(containers.DeclarativeContainer):
    instance = providers.Singleton(DynamoDb)
