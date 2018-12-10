from app.main.data.dynamo_db import DynamoDbContainer
from boto3.dynamodb.conditions import Key, Attr


class LabeledContentRepository(object):
    def __init__(self, dynamo_connection):
        self.dynamo_connection = dynamo_connection
        self.table = self.dynamo_connection.content_by_label

    def scan(self):
        return self.table.scan()["Items"]

    def get_by_label(self, label):
        response = self.table.query(
            KeyConditionExpression=Key('label').eq(label)
        )
        return response['Items']

    def write(self, data):
        """
        Writes given data into dynamo db
        :param data: objects { label, content } or list of objects [{ label, content }]
        """
        if isinstance(data, list):
            for entity in data:
                self.write(entity)

        elif isinstance(data, dict):
            # Watch out! Getting stack overflow without casting (deepcopy issue)
            # https://github.com/amzn/ion-python/issues/61
            label = str(data['label'])
            source = str(data['source'])
            content = str(data['content'])

            self.table.put_item(
                Item={
                    'label': label,
                    'content': content
                }
            )

        else:
            raise Exception('Only list or dict are acceptable')


class LabeledContentRepositoryContainer(object):
    instance = LabeledContentRepository(dynamo_connection=DynamoDbContainer.instance)
