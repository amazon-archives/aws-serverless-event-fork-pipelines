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

1. `TopicArn` (required) - The ARN of the SNS topic to which this instance of the pipeline should be subscribed.
1. `DestinationQueueName` (required) - The name of the SQS queue to which the Lambda replay function forwards events, once the replay trigger is enabled. The queue must be in the same accout and region as this pipeline.
1. `SubscriptionFilterPolicy` (optional) - The SNS subscription filter policy, in JSON format, used for filtering the incoming events. The filter policy decides which events are processed by this pipeline. If you don’t enter any value, then no filtering is used, meaning all events are processed.
1. `ReplayQueueRetentionPeriodInSeconds` (optional) - The amount of seconds for which the SQS replay queue should keep the incoming events. If you don’t enter any value, then 1,209,600 (14 days) is used.
1. `LogLevel` (optional) - The level used for logging the execution of the Lambda function that polls events from the SQS queue. Four options are available, namely DEBUG, INFO, WARNING, and ERROR. If you don’t enter any value, then INFO is used.

### Outputs

1. `ReplayFunctionName` - Replay Lambda function name.
1. `ReplayFunctionArn` - Replay Lambda function ARN.
1. `ReplayFunctionMappingId` - Identifier of the event source mapping that connects the Replay Lambda function to the SQS queue.

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
