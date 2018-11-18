"""Lambda handler for custom resource for setting SNS subscription filter policy."""

import lambdainit  # noqa: F401
import boto3
import cfn_resource

sns = boto3.client('sns')
handler = cfn_resource.Resource()


@handler.create
def create(event, context):
    """Logic for resource create.

    Set subscription filter policy to JSON string passed to custom resource.
    """
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    filter_policy = props['FilterPolicy']
    return _set_filter_policy(subscription_arn, filter_policy)


@handler.update
def update(event, context):
    """Logic for resource update.

    Update subscription filter policy to JSON string passed to custom resource.
    """
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    filter_policy = props['FilterPolicy']
    return _set_filter_policy(subscription_arn, filter_policy)


@handler.delete
def delete(event, context):
    """Logic for resource delete.

    Clear subscription filter policy on resource delete.
    """
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    # clear filter policy on delete
    return _set_filter_policy(subscription_arn, '{}')


def _set_filter_policy(subscription_arn, filter_policy):
    response = {
        "Status": "SUCCESS",
        "PhysicalResourceId": "{}-filterpolicy".format(subscription_arn)
    }

    try:
        sns.set_subscription_attributes(
            SubscriptionArn=subscription_arn,
            AttributeName='FilterPolicy',
            AttributeValue=filter_policy
        )
    except Exception as e:
        print(
            'Failure setting filter policy for subscription {}. FilterPolicy={}'.format(
                subscription_arn, filter_policy)
        )
        response['Status'] = 'FAILED'
        response['Reason'] = 'Error setting subscription filter policy: {}'.format(e)

    return response
