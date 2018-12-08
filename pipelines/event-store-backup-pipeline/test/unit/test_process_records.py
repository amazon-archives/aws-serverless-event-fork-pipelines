import pytest
import test_constants

import process_records


def test_handler(mocker):
    mocker.patch.object(process_records, 'FIREHOSE')
    process_records.FIREHOSE.put_record.return_value = {}

    event = {
        'Records': [
            {'body': 'foo'},
            {'body': 'bar'}
        ]
    }
    process_records.handler(event, None)

    assert process_records.FIREHOSE.put_record.call_count == 2
    process_records.FIREHOSE.put_record.assert_any_call(
        DeliveryStreamName=test_constants.FIREHOSE_DELIVERY_STREAM_NAME,
        Record={'Data': 'foo\n'}
    )
    process_records.FIREHOSE.put_record.assert_any_call(
        DeliveryStreamName=test_constants.FIREHOSE_DELIVERY_STREAM_NAME,
        Record={'Data': 'bar\n'}
    )


def test_handler_no_records(mocker):
    mocker.patch.object(process_records, 'FIREHOSE')
    process_records.handler({}, None)
    process_records.FIREHOSE.put_record.assert_not_called()
