"""Lambda handler for forwarding messages from SQS to Kinesis Firehose."""

import lambdainit  # noqa: F401

import boto3

import config
import lambdalogging

LOG = lambdalogging.getLogger(__name__)
FIREHOSE = boto3.client('firehose')


def handler(event, context):
    """Forward SQS messages to Kinesis Firehose Delivery Stream."""
    LOG.debug('Received event: %s', event)
    if 'Records' not in event:
        LOG.info('No records in event')
        return

    for record in event['Records']:
        response = FIREHOSE.put_record(
            DeliveryStreamName=config.FIREHOSE_DELIVERY_STREAM_NAME,
            Record={'Data': record['body'] + "\n"}
        )
        LOG.debug('Firehose response: %s', response)
