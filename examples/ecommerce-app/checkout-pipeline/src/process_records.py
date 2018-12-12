"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import boto3
import json

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)

TABLE = boto3.resource('dynamodb').Table(config.TABLE_NAME)


def handler(event, context):
    """Convert checkout events to Orders table records."""
    LOG.debug('Received event: %s', event)

    if 'Records' not in event:
        LOG.info('No records in event')
        return

    for record in event['Records']:
        TABLE.put_item(
            Item=_to_item(json.loads(record['body']))
        )


def _to_item(checkout_event):
    # TODO: copy more attributes
    return {
        'CustomerId': str(checkout_event['customer']['id']),
        'DateOrderId': '{}-{}'.format(checkout_event['date'], checkout_event['id'])
    }
