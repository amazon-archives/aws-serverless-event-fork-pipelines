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

1. `TopicArn` (required) - SNS Topic ARN whose events should be backed up to S3.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for events processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all events sent to the SNS topic.
1. `StreamPrefix` (optional) - A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket. If not specified, the default value of `backup/` is used.
1. `StreamCompressionFormat` (optional) - The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. For valid values, see the `CompressionFormat` content for the [S3DestinationConfiguration](https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html) data type in the *Amazon Kinesis Data Firehose API Reference*.
1. `EnableBucketEncryption` (optional) - Set to `true` to enable server-side encryption on the S3 backup bucket using the default aws/s3 AWS KMS master key. If not specified, the default value of `false` is used.
1. `StreamBufferingIntervalInSeconds` (optional) - Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. See https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html for details. If not specified, the default value of 300 is used.
1. `StreamBufferingSizeInMBs` (optional) - Buffer incoming data to the specified size, in MBs, before delivering it to the destination. Note, if you specify a DataTransformationFunctionArn, you should not set this higher than 6. See https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html for details. If not specified, the default value of 5 is used.
1. `DataTransformationFunctionArn` (optional) - ARN of data transformation Lambda function. This optional parameter allows you to configure a Lambda function to be invoked by Kinesis Firehose to transformation incoming events before they are saved to S3. For example, you could use this to remove sensitive data to meet compliance regulations.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO.

### Outputs

1. `BackupBucketName` - Backup bucket name.
1. `BackupBucketArn` - Backup bucket ARN.

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
