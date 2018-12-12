import pytest
import json

import process_records


def test_handler(mocker):
    mocker.patch.object(process_records, 'TABLE')
    checkout_events = [
        {
            'id': 1,
            'date': '2018-12-15T23:41:11-08:00',
            'status': 'confirmed',
            'customer': {
                'id': 100
            },
            'payment': {
                'id': 200,
                'amount': 99.99,
                'currency': 'usd'
            },
            'items': [
                {
                    'quantity': 1
                },
                {
                    'quantity': 2
                },
            ],
        },
        {
            'id': 2,
            'date': '2018-12-16T23:41:11-08:00',
            'status': 'confirmed',
            'customer': {
                'id': 101
            },
            'payment': {
                'id': 201,
                'amount': 49.99,
                'currency': 'usd'
            },
            'items': [
                {
                    'quantity': 3
                },
                {
                    'quantity': 5
                },
            ],
        }
    ]
    process_records.handler(_input_event(checkout_events), None)
    process_records.TABLE.put_item.assert_called()
    assert process_records.TABLE.put_item.call_count == 2


def _input_event(checkout_events):
    records = [{'body': json.dumps(e)} for e in checkout_events]
    return {'Records': records}


def test_handler_no_records(mocker):
    mocker.patch.object(process_records, 'TABLE')
    process_records.handler({}, None)
    process_records.TABLE.put_item.assert_not_called()
