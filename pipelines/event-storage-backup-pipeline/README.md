## AWS Event Fork Pipelines: Event Storage and Backup Pipeline

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This AWS Event Fork Pipelines app backs up events from the given Amazon SNS topic to an Amazon S3 bucket, using an Amazon Kinesis Data Firehose stream.

## Architecture

![AWS Event Fork Pipelines Backup and Storage Architecture](https://github.com/aws-samples/aws-serverless-event-fork-pipelines/raw/master/pipelines/event-storage-backup-pipeline/images/event-storage-backup-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function reads events from the SQS queue and publishes them to an Amazon Kinesis Data Firehose Delivery Stream, which saves them to an Amazon S3 bucket.
    1. An optional data transformation Lambda function can be specified to transform the data prior to saving it to the S3 bucket.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the [app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:077246666028:applications/fork-event-storage-backup-pipeline). Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template, filling in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

### Parameters

1. `TopicArn` (required) - The ARN of the SNS topic to which this instance of the pipeline should be subscribed.
1. `SubscriptionFilterPolicy` (optional) - The SNS subscription filter policy, in JSON format, used for filtering the incoming events. The filter policy decides which events are processed by this pipeline. If you don’t enter any value, then no filtering is used, meaning all events are processed.
1. `StreamPrefix` (optional) - The string prefix used for naming files stored in the S3 bucket. If you don’t enter any value, then no prefix is used.
1. `StreamCompressionFormat` (optional) - The format used for compressing the incoming events. Three options are available, namely GZIP, ZIP, and SNAPPY. If you don’t enter any value, then data compression is disabled.
1. `BucketArn` (optional) - The ARN of the S3 bucket to which incoming events are loaded. If you don't enter any value, then a new S3 bucket is created in your account.
1. `StreamBufferingIntervalInSeconds` (optional) - The amount of seconds for which the stream should buffer incoming events before delivering them to the destination. Any integer value from 60 to 900 seconds. If you don't enter any value, then 300 is used.
1. `StreamBufferingSizeInMBs` (optional) - The amount of data, in MB, that the stream should buffer before delivering them to the destination. Any integer value from 1 to 100. If you don't enter any value, then 5 is used.
1. `DataTransformationFunctionArn` (optional) - The ARN of the Lambda function used for transforming the incoming events. If you don’t enter any value, then data transformation is disabled.
1. `LogLevel` (optional) - The level used for logging the execution of the Lambda function that polls events from the SQS queue. Four options are available, namely DEBUG, INFO, WARNING, and ERROR. If you don’t enter any value, then INFO is used.

### Outputs

1. `BackupBucketName` - Backup bucket name (only output if this app created a backup bucket).
1. `BackupBucketArn` - Backup bucket ARN (only output if this app created a backup bucket).

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
