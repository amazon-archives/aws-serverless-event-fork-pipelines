## AWS Event Fork Pipelines: Event Search and Analytics Pipeline

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This AWS Event Fork Pipelines app indexes events from the given Amazon SNS topic into an Amazon Elasticsearch Service domain for search and analytics, using an Amazon Kinesis Data Firehose stream.

## Architecture

![AWS Event Fork Pipelines Search and Analytics Architecture](https://github.com/aws-samples/aws-serverless-event-fork-pipelines/raw/master/pipelines/event-search-analytics-pipeline/images/event-search-analytics-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function reads events from the SQS queue and publishes them to an Amazon Kinesis Data Firehose Delivery Stream, which saves them to the given Amazon Elasticsearch Service Domain.
    1. An optional data transformation Lambda function can be specified to transform the data prior to saving it to the Elasticsearch Service cluster.
1. If for some reason Kinesis Data Firehose is not able to write events to the Amazon Elasticsearch Service Domain, the failed events are written to a backup Amazon S3 bucket.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, visit the [app's page on the AWS Lambda Console](https://console.aws.amazon.com/lambda/home#/create/app?applicationId=arn:aws:serverlessrepo:us-east-1:077246666028:applications/fork-event-search-analytics-pipeline). Click the "Copy as SAM Resource" button and paste the copied YAML into your SAM template, filling in any required parameters. Alternatively, you can deploy the application into your account directly via the AWS Lambda Console.

### Parameters

1. `TopicArn` (required) - The ARN of the SNS topic to which this instance of the pipeline should be subscribed.
1. `SearchDomainArn` (required) - The ARN of the Elasticsearch domain to be used. A domain is an Elasticsearch cluster in the AWS cloud, setting the compute and storage configuration needed. If you don’t enter any value, then a new domain with default configuration is created in your account.
1. `SearchIndexName` (required) - The name of the Elasticsearch index used for indexing the events, making them available for search and analytics. Max string length of 80, all lowecase, no special characters.
1. `SearchTypeName` (required) - The name of the Elasticsearch type used for organizing the events in an index. Max string length of 100, all lowercase, not starting with an underscore.
1. `SubscriptionFilterPolicy` (optional) - The SNS subscription filter policy, in JSON format, used for filtering the incoming events. The filter policy decides which events are processed by this pipeline. If you don’t enter any value, then no filtering is used, meaning all events are processed.
1. `SearchIndexRotationPeriod` (optional) - The rotation period of the Elasticsearch index. Index rotation appends a timestamp to the index name, facilitating the expiration of old data. Five options are available, namely NoRotation, OneHour, OneDay, OneWeek, and OneMonth. If you don’t enter any value, then option NoRotation is used.
1. `StreamRetryDurationInSeconds` (optional) - The retry duration for cases when the stream is unable to index events in the Elasticsearch index. If you don’t enter any value, then the pipeline sets 60 seconds.
1. `StreamPrefix` (optional) - The string prefix used for naming files stored in the S3 bucket. If you don’t enter any value, then no prefix is used.
1. `StreamCompressionFormat` (optional) - The format used for compressing the incoming events. Three options are available, namely GZIP, ZIP, and SNAPPY. If you don’t enter any value, then data compression is disabled.
1. `StreamBufferingIntervalInSeconds` (optional) - The amount of seconds for which the stream should buffer incoming events before delivering them to the destination. Any integer value from 60 to 900 seconds. If you don't enter any value, then 300 is used.
1. `StreamBufferingSizeInMBs` (optional) - The amount of data, in MB, that the stream should buffer before delivering them to the destination. Any integer value from 1 to 100. If you don't enter any value, then 5 is used.
1. `DataTransformationFunctionArn` (optional) - The ARN of the Lambda function used for transforming the incoming events. If you don’t enter any value, then data transformation is disabled.
1. `LogLevel` (optional) - The level used for logging the execution of the Lambda function that polls events from the SQS queue. Four options are available, namely DEBUG, INFO, WARNING, and ERROR. If you don’t enter any value, then INFO is used.

### Outputs

1. `AnalyticsDeadLetterBucketName` - Dead-letter S3 bucket name
1. `AnalyticsDeadLetterBucketArn` - Dead-letter S3 bucket ARN
1. `AnalyticsDomainName` - Analytics ES domain name (only output if this app created an ES domain)
1. `AnalyticsDomainArn` - Analytics ES domain ARN (only output if this app created an ES domain)
1. `AnalyticsDomainEndpoint` - Analytics ES domain endpoint (only output if this app created an ES domain)

## License Summary

This code is made available under a modified MIT license. See the LICENSE file.
