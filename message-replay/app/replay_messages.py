"""Lambda handler for replaying messages from the replay buffer SQS queue to the destination SQS queue."""

import lambdainit  # noqa: F401
import os
import boto3

SQS = boto3.client('sqs')
DESTINATION_SQS_QUEUE_NAME = os.getenv('DESTINATION_SQS_QUEUE_NAME')
DESTINATION_SQS_QUEUE_URL = SQS.get_queue_url(QueueName=DESTINATION_SQS_QUEUE_NAME)['QueueUrl']


def handler(event, context):
    """Forward SQS messages to destination queue."""
    if 'Records' not in event:
        print('No records in event')
        return

    response = SQS.send_message_batch(
        QueueUrl=DESTINATION_SQS_QUEUE_URL,
        Entries=[_to_request_record(index, record)
                 for index, record in enumerate(event['Records'])]
    )
    if response['Failed']:
        raise RuntimeError('Failed to send messages to destination queue: queue={}, failures={}'.format(
                DESTINATION_SQS_QUEUE_URL, response['Failed']
        ))


def _to_request_record(id, record):
    return {
        'Id': str(id),
        'MessageBody': record['body'],
        'MessageAttributes': record['messageAttributes']
    }
