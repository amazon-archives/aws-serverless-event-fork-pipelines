# sns-subscription-filter-policy-string

This utility app provides a custom resource that allows an SNS Topic Subscription's filter policy to be specified as a JSON string instead of a JSON object so it can be passed into apps as a template parameter.

## Installation Instructions

This app is a utility that is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the app's page on the AWS Lambda Console. Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template and fill in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

## App Parameters

1. `SNSTopicArn` (required) - ARN of the SNS Topic being subscribed to.
1. `SubscriptionArn` (required) - ARN of the SNS Topic Subscription to apply the filter policy to.
1. `SubscriptionFilterPolicy` (required) - SNS Topic Subscription FilterPolicy as a JSON string. See https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html for details.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO

## App Outputs

1. `SetFilterPolicyFunctionName` - SetFilterPolicy Lambda Function Name.
1. `SetFilterPolicyFunctionArn` - SetFilterPolicy Lambda Function ARN.

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.