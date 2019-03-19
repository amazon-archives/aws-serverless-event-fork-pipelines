## AWS Event Fork Pipelines: Event Replay Pipeline

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This AWS Event Fork Pipelines app buffers events from the given Amazon SNS topic into an Amazon SQS queue, so it can replay these events back to another pipeline in a disaster recovery scenario.

## Architecture

![AWS Event Fork Pipelines Replay Pipeline Architecture](https://github.com/aws-samples/aws-serverless-event-fork-pipelines/raw/master/pipelines/event-replay-pipeline/images/event-replay-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function is mapped to the SQS queue, but the event source is initially disabled.
1. In a disaster scenario, such as a data corruption bug, once the bug has been fixed, an operator can manually enable the Lambda event source mapping, and the AWS Lambda function will forward the events from the replay buffer to the given destination SQS queue.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the [app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:077246666028:applications/fork-event-replay-pipeline). Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template, filling in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

### Parameters

1. `TopicArn` (required) - SNS Topic ARN whose events should be backed up to S3.
1. `DestinationQueueName` (required) - Name of destination SQS Queue where replay events should be sent in a disaster recovery scenario. The app assumes the queue is in the same account and region as this app.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for events processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all messages sent to the SNS topic.
1. `ReplayQueueRetentionPeriodInSeconds` (optional) - Retention period in seconds for the replay buffer SQS queue. This controls how long messages will be stored in the replay queue. If not specified, the default value of `1209600` (14 days) is used.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO.

### Outputs

1. `ReplayFunctionName` - Replay Lambda function name.
1. `ReplayFunctionArn` - Replay Lambda function ARN.
1. `ReplayFunctionMappingId` - Identifier of the event source mapping that connects the Replay Lambda function to the SQS queue.

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
