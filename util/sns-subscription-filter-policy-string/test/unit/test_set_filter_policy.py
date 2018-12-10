import pytest
import set_filter_policy

SUBSCRIPTION_ARN = 'theSubscription'
FILTER_POLICY = '{"pet": ["dog", "cat"]}'


def test_create(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')

    response = set_filter_policy.create(_mock_event(), None)
    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }

    set_filter_policy.SNS.set_subscription_attributes.assert_called_with(
        SubscriptionArn=SUBSCRIPTION_ARN,
        AttributeName='FilterPolicy',
        AttributeValue=FILTER_POLICY
    )


def test_create_sns_exception(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')
    set_filter_policy.SNS.set_subscription_attributes.side_effect = Exception('boom!')

    response = set_filter_policy.create(_mock_event(), None)
    assert response == {
        'Status': 'FAILED',
        'Reason': 'Error setting subscription filter policy: boom!',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }


def test_update(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')

    response = set_filter_policy.update(_mock_event(), None)
    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }

    set_filter_policy.SNS.set_subscription_attributes.assert_called_with(
        SubscriptionArn=SUBSCRIPTION_ARN,
        AttributeName='FilterPolicy',
        AttributeValue=FILTER_POLICY
    )


def test_update_sns_exception(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')
    set_filter_policy.SNS.set_subscription_attributes.side_effect = Exception('boom!')

    response = set_filter_policy.update(_mock_event(), None)
    assert response == {
        'Status': 'FAILED',
        'Reason': 'Error setting subscription filter policy: boom!',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }


def test_delete(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')

    response = set_filter_policy.delete(_mock_event(), None)
    assert response == {
        'Status': 'SUCCESS',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }

    set_filter_policy.SNS.set_subscription_attributes.assert_called_with(
        SubscriptionArn=SUBSCRIPTION_ARN,
        AttributeName='FilterPolicy',
        AttributeValue='{}'
    )


def test_delete_sns_exception(mocker):
    mocker.patch.object(set_filter_policy, 'SNS')
    set_filter_policy.SNS.set_subscription_attributes.side_effect = Exception('boom!')

    response = set_filter_policy.delete(_mock_event(), None)
    assert response == {
        'Status': 'FAILED',
        'Reason': 'Error setting subscription filter policy: boom!',
        'PhysicalResourceId': SUBSCRIPTION_ARN + '-filterpolicy'
    }


def _mock_event():
    return {
        'ResourceProperties': {
            'SubscriptionArn': SUBSCRIPTION_ARN,
            'FilterPolicy': FILTER_POLICY
        }
    }
