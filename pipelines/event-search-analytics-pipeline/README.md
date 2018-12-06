## SNS Fork: Event Search and Analytics Pipeline

This Serverless application provides an SNS Fork processing pipeline that saves topic events to an Amazon Elasticsearch Service cluster for searching and analytics.

## Architecture

![SNS Fork Search and Analytics Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/search-analytics/images/search-analytics-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function reads events from the SQS queue and publishes them to an Amazon Kinesis Data Firehose Delivery Stream, which saves them to the given Amazon Elasticsearch Service Domain.
1. If for some reason Kinesis Data Firehose is not able to write events to the Amazon Elasticsearch Service Domain, the failed events are written to a backup Amazon S3 bucket.

**Note:** The app does not create an Amazon Elasticsearch Service cluster as part of the app since Amazon ES Domains have many configuration options and users commonly want to use a single cluster across many pipelines to save cost and perform more advanced queries.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, paste the following into your SAM template:

```yaml
  AnalyticsPipeline:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: TODO
        SemanticVersion: 1.0.0
      Parameters:
        # SNS Topic ARN whose events should be backed up to S3.
        SNSTopicArn: !Ref EventTopic
        # ARN of the Elasticsearch Domain to write to.
        ElasticsearchDomainArn: !GetAtt MyElasticSearchCluster.Arn
        # Elasticsearch index name to write to.
        ElasticsearchIndexName: PROVIDE-VALUE
        # The Elasticsearch type name that Amazon ES adds to documents when indexing data.
        ElasticsearchTypeName: PROVIDE-VALUE
        # The frequency of Elasticsearch index rotation.
        #ElasticsearchIndexRotationPeriod: NoRotation # Uncomment to override default value
        # Number of seconds to retry if events cannot be written to Elasticsearch index.
        #RetryDurationInSeconds: 300 # Uncomment to override default value
        # SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering
        # for events processed by this app. See https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html for details.
        #SubscriptionFilterPolicy: '' # Uncomment to override default value
        # Prefix used for S3 backup files
        #BackupPrefix: backup/ # Uncomment to override default value
        # Compression format for S3 backup files
        #BackupCompressionFormat: UNCOMPRESSED # Uncomment to override default value
```

Alternatively, you can deploy the application into your account manually via the [sns-fork-search-analytics SAR page](TODO).

### Parameters

1. `SNSTopicArn` (required) - SNS Topic ARN whose events should be backed up to S3.
1. `ElasticsearchDomainArn` (required) - ARN of the Elasticsearch Domain to write to.
1. `ElasticsearchIndexName` (required) - Elasticsearch index name to write to.
1. `ElasticsearchTypeName` (required) - The Elasticsearch type name that Amazon ES adds to documents when indexing data.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for events processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all events sent to the SNS topic.
1. `ElasticsearchIndexRotationPeriod` (optional) - The frequency of Elasticsearch index rotation. See [the documentation](https://docs.aws.amazon.com/firehose/latest/dev/basic-deliver.html#es-index-rotation) for details. If not specified, the default value of `NoRotation` is used.
1. `RetryDurationInSeconds` (optional) - Number of seconds to retry if events cannot be written to Elasticsearch index. Events that fail to get written to ElasticSearch are written to an S3 backup bucket created by the app. See [the documentation](https://docs.aws.amazon.com/firehose/latest/APIReference/API_ElasticsearchRetryOptions.html) for details. If not specified, the default value of 300 seconds (5 minutes) is used.
1. `BackupPrefix` (optional) - A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket (only used for events that cannot be delivered to the Elasticsearch cluster). If not specified, the default value of `backup/` is used.
1. `BackupCompressionFormat` (optional) - The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket (only used for events that cannot be delivered to the Elasticsearch cluster). For valid values, see the `CompressionFormat` content for the [S3DestinationConfiguration](https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html) data type in the *Amazon Kinesis Data Firehose API Reference*.

### Outputs

1. `BackupBucketName` - Failed events backup bucket name.
1. `BackupBucketArn` - Failed events backup bucket ARN.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.