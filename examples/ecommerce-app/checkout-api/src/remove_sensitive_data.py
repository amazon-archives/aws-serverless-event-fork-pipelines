"""Lambda function handler."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import base64
import json

import lambdalogging

LOG = lambdalogging.getLogger(__name__)


def handler(event, context):
    """Remove sensitive data from checkout events."""
    LOG.debug('Received event: %s', event)

    if 'records' not in event:
        LOG.warning('No records found in event.')
        return {}

    transformed_records = [_transform(r) for r in event['records']]

    response = {'records': transformed_records}
    LOG.debug("Returning response: %s", response)
    return response


def _transform(record):
    transformed_record = {
        'recordId': record['recordId'],
        'result': 'Ok'
    }
    checkout_event = json.loads(base64.b64decode(record['data']))

    payment_info = checkout_event.get('payment', {})
    sensitive_payment_keys = [key for key in payment_info.keys() if key.startswith('card-')]
    LOG.debug("Removing sensitive payment information from checkout event: %s", sensitive_payment_keys)
    for payment_key in sensitive_payment_keys:
        payment_info.pop(payment_key)

    transformed_record['data'] = base64.b64encode(bytes(json.dumps(checkout_event), 'UTF-8')).decode('UTF-8')
    return transformed_record
