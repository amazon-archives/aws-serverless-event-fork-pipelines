"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import boto3
import json

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)
TOPIC = boto3.resource('sns').Topic(config.TOPIC_ARN)


def checkout(event, context):
    """Process API call posting a checkout event."""
    LOG.debug('Received event: %s', event)

    checkout_event = json.loads(event['body'])
    amount = checkout_event['payment']['amount']

    LOG.debug('Publishing checkout event with amount: %s', amount)
    TOPIC.publish(
        Message=json.dumps(checkout_event),
        MessageAttributes={
            'amount': {
                'DataType': 'Number',
                'StringValue': str(amount)
            }
        }
    )

    return {
        'statusCode': 200,
        'body': '{}'
    }
