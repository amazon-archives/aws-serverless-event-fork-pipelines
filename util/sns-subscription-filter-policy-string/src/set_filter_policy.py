"""Lambda handler for custom resource for setting SNS subscription filter policy."""

# must be the first import in files with lambda function handlers
import lambdainit  # noqa: F401

import boto3
import cfn_resource

import lambdalogging

LOG = lambdalogging.getLogger(__name__)
SNS = boto3.client('sns')
handler = cfn_resource.Resource()


@handler.create
def create(event, context):
    """Logic for resource create.

    Set subscription filter policy to JSON string passed to custom resource.
    """
    LOG.debug('CustomResource create handler called with event: %s', event)
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    filter_policy = props['FilterPolicy']
    return _set_filter_policy(subscription_arn, filter_policy)


@handler.update
def update(event, context):
    """Logic for resource update.

    Update subscription filter policy to JSON string passed to custom resource.
    """
    LOG.debug('CustomResource update handler called with event: %s', event)
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    filter_policy = props['FilterPolicy']
    return _set_filter_policy(subscription_arn, filter_policy)


@handler.delete
def delete(event, context):
    """Logic for resource delete.

    Clear subscription filter policy on resource delete.
    """
    LOG.debug('CustomResource delete handler called with event: %s', event)
    props = event['ResourceProperties']
    subscription_arn = props['SubscriptionArn']
    # clear filter policy on delete
    return _set_filter_policy(subscription_arn, '{}')


def _set_filter_policy(subscription_arn, filter_policy):
    response = {
        "Status": "SUCCESS",
        "PhysicalResourceId": "{}-filterpolicy".format(subscription_arn)
    }

    LOG.debug("Setting subscription filter policy: subscription_arn=%s, filter_policy=%s",
              subscription_arn, filter_policy)
    try:
        SNS.set_subscription_attributes(
            SubscriptionArn=subscription_arn,
            AttributeName='FilterPolicy',
            AttributeValue=filter_policy
        )
    except Exception as e:
        LOG.warning(
            'Failure setting filter policy for subscription %s. FilterPolicy=%s, Reason=%s',
            subscription_arn, filter_policy, e
        )
        response['Status'] = 'FAILED'
        response['Reason'] = 'Error setting subscription filter policy: {}'.format(e)

    LOG.debug('Returning response: %s', response)
    return response
