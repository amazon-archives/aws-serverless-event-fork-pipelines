import json

import pytest

import api


def test_checkout(mocker):
    mocker.patch.object(api, 'TOPIC')
    api.TOPIC.publish.return_value = {'MessageId': 'foo'}
    message = json.dumps({
        'payment': {
            'amount': 99.99
        }
    })
    api_event = {
        'body': message
    }

    response = api.checkout(api_event, None)
    assert response == {
        'statusCode': 200,
        'body': '{}'
    }

    api.TOPIC.publish.assert_called_with(
        Message=message,
        MessageAttributes={
            'amount': {
                'DataType': 'Number',
                'StringValue': '99.99'
            }
        }
    )
