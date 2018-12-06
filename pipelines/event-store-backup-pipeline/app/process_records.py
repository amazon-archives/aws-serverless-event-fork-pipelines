"""Lambda handler for forwarding messages from SQS to Kinesis Firehose."""

import lambdainit  # noqa: F401
import os
import boto3

FIREHOSE = boto3.client('firehose')
FH_STREAM_NAME = os.getenv('FIREHOSE_DELIVERY_STREAM_NAME')


def handler(event, context):
    """Forward SQS messages to Kinesis Firehose Delivery Stream."""
    if 'Records' not in event:
        print('No records in event')
        return

    for record in event['Records']:
        response = FIREHOSE.put_record(
            DeliveryStreamName=FH_STREAM_NAME,
            Record={'Data': record['body'] + "\n"}
        )
        print(response)
