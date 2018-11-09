import boto3
import dependency_injector.containers as containers
import dependency_injector.providers as providers


class DynamoDb(object):

    def __init__(self):
        self.resource = boto3.resource('dynamodb',
                                  endpoint_url='http://192.168.99.100:8000',
                                  region_name='us-west-1',
                                  aws_access_key_id="anything",
                                  aws_secret_access_key="anything")
        self.on_init()

    def on_init(self):
        if len(list(self.resource.tables.all())) > 0:
            return

        self.resource.create_table(
            TableName='labeled_content',
            KeySchema=[
                {
                    'AttributeName': 'label',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'label',
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