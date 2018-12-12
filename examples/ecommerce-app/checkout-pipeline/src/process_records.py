"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import boto3
from decimal import Decimal
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
    item = {
        'CustomerId': str(checkout_event['customer']['id']),
        'DateOrderId': '{}-{}'.format(checkout_event['date'], checkout_event['id']),
        'PaymentId': checkout_event['payment']['id'],
        'PaymentAmount': Decimal(str(checkout_event['payment']['amount'])),
        'PaymentCurrency': checkout_event['payment']['currency'],
        'TotalQuantity': sum([i['quantity'] for i in checkout_event['items']]),
    }

    if config.BUG_ENABLED:
        LOG.info("Data corruption bug enabled.")
        item['PaymentId'] = 'CORRUPTED!'
        item['PaymentAmount'] = 'CORRUPTED!'
        item['PaymentCurrency'] = 'CORRUPTED!'
        item['TotalQuantity'] = 'CORRUPTED!'

    return item
