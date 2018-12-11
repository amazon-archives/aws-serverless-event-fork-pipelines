import pytest

import json
import base64

import remove_sensitive_data


def test_handler():
    records = [
        {
            'id': 123,
            'date': '2018-12-15T23:41:11-08:00',
            'status': 'confirmed',
            'customer': {
                'id': 65144,
                'name': 'John Doe',
                'email': 'johndoe@example.com'
            },
            'payment': {
                'id': 2509,
                'amount': 450.00,
                'currency': 'usd',
                'method': 'credit',
                'card-network': 'visa',
                'card-number': '1234 5678 9012 3456',
                'card-expiry': '10/2020',
                'card-owner': 'John Doe',
                'card-cvv': '123'
            }
        },
        {
            'id': 124,
            'date': '2018-12-16T23:41:11-08:00',
            'status': 'confirmed',
            'customer': {
                'id': 66144,
                'name': 'Jane Doe',
                'email': 'janedoe@example.com'
            },
            'payment': {
                'id': 2511,
                'amount': 120.00,
                'currency': 'usd',
                'method': 'credit',
                'card-network': 'mc',
                'card-number': '1234 5678 9012 3456',
                'card-expiry': '11/2021',
                'card-owner': 'Jane Doe',
                'card-cvv': '123'
            }
        }
    ]

    response = remove_sensitive_data.handler(_input_event(records), None)

    assert response == _output_event(
        [
            {
                'id': 123,
                'date': '2018-12-15T23:41:11-08:00',
                'status': 'confirmed',
                'customer': {
                    'id': 65144,
                    'name': 'John Doe',
                    'email': 'johndoe@example.com'
                },
                'payment': {
                    'id': 2509,
                    'amount': 450.00,
                    'currency': 'usd',
                    'method': 'credit',
                }
            },
            {
                'id': 124,
                'date': '2018-12-16T23:41:11-08:00',
                'status': 'confirmed',
                'customer': {
                    'id': 66144,
                    'name': 'Jane Doe',
                    'email': 'janedoe@example.com'
                },
                'payment': {
                    'id': 2511,
                    'amount': 120.00,
                    'currency': 'usd',
                    'method': 'credit',
                }
            }
        ]
    )


def test_handler_no_records():
    assert remove_sensitive_data.handler({}, None) == {}


def _input_event(record_payloads):
    event_records = [_create_input_record(i, rp) for i, rp in enumerate(record_payloads)]
    return {'records': event_records}


def _create_input_record(index, record_payload):
    return {
        'recordId': str(index),
        'data': base64.b64encode(bytes(json.dumps(record_payload), 'UTF-8'))
    }


def _output_event(record_payloads):
    records = [_create_output_record(i, rp) for i, rp in enumerate(record_payloads)]
    return {'records': records}


def _create_output_record(index, record_payload):
    return {
        'recordId': str(index),
        'result': 'Ok',
        'data': base64.b64encode(bytes(json.dumps(record_payload), 'UTF-8')).decode('UTF-8')
    }
