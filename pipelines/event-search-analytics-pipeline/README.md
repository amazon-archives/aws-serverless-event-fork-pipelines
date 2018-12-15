## SNS Fork Pattern: Event Search and Analytics Pipeline

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This Serverless application provides an SNS Fork pattern pipeline that saves topic events to an Amazon Elasticsearch Service cluster for search and analytics.

## Architecture

![SNS Fork Search and Analytics Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/pipelines/event-search-analytics-pipeline/images/event-search-analytics-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function reads events from the SQS queue and publishes them to an Amazon Kinesis Data Firehose Delivery Stream, which saves them to the given Amazon Elasticsearch Service Domain.
    1. An optional data transformation Lambda function can be specified to transform the data prior to saving it to the Elasticsearch Service cluster.
1. If for some reason Kinesis Data Firehose is not able to write events to the Amazon Elasticsearch Service Domain, the failed events are written to a backup Amazon S3 bucket.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the [app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:077246666028:applications/fork-event-search-analytics-pipeline). Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template, filling in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

### Parameters

1. `SNSTopicArn` (required) - SNS Topic ARN whose events should be sent to the ElasticSearch domain.
1. `ElasticsearchDomainArn` (required) - ARN of the Elasticsearch Domain to write to.
1. `ElasticsearchIndexName` (required) - Elasticsearch index name to write to.
1. `ElasticsearchTypeName` (required) - The Elasticsearch type name that Amazon ES adds to documents when indexing data.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for events processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all events sent to the SNS topic.
1. `ElasticsearchIndexRotationPeriod` (optional) - The frequency of Elasticsearch index rotation. See [the documentation](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#es-index-rotation) for details. If not specified, the default value of `NoRotation` is used.
1. `RetryDurationInSeconds` (optional) - Number of seconds to retry if events cannot be written to Elasticsearch index. Events that fail to get written to ElasticSearch are written to an S3 backup bucket created by the app. See [the documentation](https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchRetryOptions.html) for details. If not specified, the default value of 300 seconds (5 minutes) is used.
1. `BackupPrefix` (optional) - A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket (only used for events that cannot be delivered to the Elasticsearch cluster). If not specified, the default value of `backup/` is used.
1. `BackupCompressionFormat` (optional) - The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket (only used for events that cannot be delivered to the Elasticsearch cluster). For valid values, see the `CompressionFormat` content for the [S3DestinationConfiguration](https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html) data type in the *Amazon Kinesis Data Firehose API Reference*.
1. `BufferingIntervalInSeconds` (optional) - Buffer incoming data for the specified period of time, in seconds, before delivering it to the destination. See https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html for details. If not specified, the defaut value of 300 (5 minutes) is used.
1. `BufferingSizeInMBs` (optional) - Buffer incoming data to the specified size, in MBs, before delivering it to the destination. Note, if you specify a DataTransformationLambdaFunctionArn, you should not set this higher than 6. See https://docs.aws.amazon.com/firehose/latest/dev/data-transformation.html for details. If not specified, the default value of 5 is used.
1. `DataTransformationLambdaFunctionArn` (optional) - ARN of data transformation Lambda function. This optional parameter allows you to configure a Lambda function to be invoked by Kinesis Firehose to transformation incoming events before they are saved to Elasticsearch. For example, you could use this to remove sensitive data to meet compliance regulations.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO.

### Outputs

1. `BackupBucketName` - Failed events backup bucket name.
1. `BackupBucketArn` - Failed events backup bucket ARN.
1. `ElasticsearchDomainName` - Name of Elasticsearch domain created by this app.
1. `ElasticsearchDomainArn` - ARN of Elasticsearch domain created by this app.
1. `ElasticsearchDomainEndpoint` - Endpoint of Elasticsearch domain created by this app.

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
