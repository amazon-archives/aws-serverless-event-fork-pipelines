"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import boto3

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)

TABLE = boto3.resource('dynamodb').Table(config.TABLE_NAME)


def handler(event, context):
    """Convert checkout events to Orders table records."""
    LOG.debug('Received event: {}', event)

    if 'Records' not in event:
        LOG.info('No records in event')
        return

    for checkout_event in event['Records']:
        TABLE.put_item(
            Item=_to_item(checkout_event)
        )


def _to_item(checkout_event):
    # TODO: copy more attributes
    return {
        'CustomerId': str(checkout_event['customer']['id']),
        'DateOrderId': '{}-{}'.format(checkout_event['date'], checkout_event['id'])
    }
