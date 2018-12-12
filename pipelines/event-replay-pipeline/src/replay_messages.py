"""Lambda handler for replaying messages from the replay buffer SQS queue to the destination SQS queue."""

import lambdainit  # noqa: F401

import boto3

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)
SQS = boto3.client('sqs')
DESTINATION_SQS_QUEUE_URL = SQS.get_queue_url(QueueName=config.DESTINATION_SQS_QUEUE_NAME)['QueueUrl']
QUEUE = boto3.resource('sqs').Queue(DESTINATION_SQS_QUEUE_URL)


def handler(event, context):
    """Forward SQS messages to destination queue."""
    LOG.debug('Received event: %s', event)
    if 'Records' not in event:
        LOG.info('No records in event')
        return

    for record in event['Records']:
        request = _to_request(record)
        LOG.debug('Replaying event to SQS queue: queue URL=%s, request=%s', DESTINATION_SQS_QUEUE_URL, request)
        response = QUEUE.send_message(**request)
        LOG.debug('SQS response: %s', response)


def _to_request(record):
    # SQS event lowercases message attribute property names so have to capitalize them again before sending to SQS
    message_attributes = {attr_name: {_capitalize(attr_prop_name): attr_prop_value
                                      for (attr_prop_name, attr_prop_value) in attr_props.items()
                                      if attr_prop_value}
                          for (attr_name, attr_props) in record['messageAttributes'].items()}
    return {
        'MessageBody': record['body'],
        'MessageAttributes': message_attributes
    }


def _capitalize(s):
    """Capitalize first letter.

    Can't use built-in capitalize function because it lowercases any chars after the first one.
    In this case, we want to leave the case of the rest of the chars the same.
    """
    return s[0].upper() + s[1:]
