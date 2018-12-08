import pytest
from unittest.mock import MagicMock

import boto3

QUEUE_URL = 'https://queue.com'


@pytest.fixture
def replay_messages(mocker):
    mock_sqs_client = MagicMock()
    mock_sqs_client.get_queue_url.return_value = {'QueueUrl': QUEUE_URL}

    mocker.patch.object(boto3, 'client')
    boto3.client.return_value = mock_sqs_client
    import replay_messages
    return replay_messages


def test_handler_no_records(mocker, replay_messages):
    replay_messages.handler({}, None)
    replay_messages.SQS.send_message_batch.assert_not_called()


def test_handler_success(mocker, replay_messages):
    replay_messages.SQS.send_message_batch.return_value = {}

    event = {
        'Records': [
            {
                'body': 'foo',
                'messageAttributes': {
                    'fooAttr1': {
                        'dataType': 'String',
                        'stringValue': 'fooAttr1Value'
                    },
                    'fooAttr2': {
                        'dataType': 'String',
                        'stringValue': 'fooAttr2Value'
                    }
                }
            },
            {
                'body': 'bar',
                'messageAttributes': {
                    'barAttr1': {
                        'dataType': 'String',
                        'stringValue': 'barAttr1Value'
                    },
                    'barAttr2': {
                        'dataType': 'String',
                        'stringValue': 'barAttr2Value'
                    }
                }
            },
        ]
    }
    replay_messages.handler(event, None)

    expected = [
        {
            'Id': '0',
            'MessageBody': 'foo',
            'MessageAttributes': {
                'fooAttr1': {
                    'DataType': 'String',
                    'StringValue': 'fooAttr1Value'
                },
                'fooAttr2': {
                    'DataType': 'String',
                    'StringValue': 'fooAttr2Value'
                }
            }
        },
        {
            'Id': '1',
            'MessageBody': 'bar',
            'MessageAttributes': {
                'barAttr1': {
                    'DataType': 'String',
                    'StringValue': 'barAttr1Value'
                },
                'barAttr2': {
                    'DataType': 'String',
                    'StringValue': 'barAttr2Value'
                }
            }
        }
    ]
    replay_messages.SQS.send_message_batch.assert_any_call(
        QueueUrl=QUEUE_URL,
        Entries=expected
    )


def test_handler_sqs_failure(mocker, replay_messages):
    replay_messages.SQS.send_message_batch.return_value = {
        'Failed': [
            {
                'Id': '0'
            }
        ]
    }

    event = {
        'Records': [
            {
                'body': 'foo',
                'messageAttributes': {}
            }
        ]
    }

    with pytest.raises(RuntimeError):
        replay_messages.handler(event, None)
