## SNS Fork: Storage and Backup Pipeline

This Serverless application provides an SNS Fork processing pipeline that saves topic events to an Amazon S3 bucket for use as backups or other purposes, e.g., to query with Amazon Athena.

## Architecture

![SNS Fork Backup and Storage Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/pipelines/event-store-backup-pipeline/images/event-storage-backup-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function reads events from the SQS queue and publishes them to an Amazon Kinesis Data Firehose Delivery Stream, which saves them to an Amazon S3 bucket.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, paste the following into your SAM template:

```yaml
  StorageBackup:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: TODO
        SemanticVersion: 1.0.0
      Parameters:
        # SNS Topic ARN whose events should be backed up to S3.
        SNSTopicArn: !Ref EventTopic
        # SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering
        # for events processed by this app. See https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html for details.
        #SubscriptionFilterPolicy: '' # Uncomment to override default value
        # Prefix used for S3 backup files
        #BackupPrefix: backup/ # Uncomment to override default value
        # Compression format for S3 backup files
        #BackupCompressionFormat: UNCOMPRESSED # Uncomment to override default value
```

Alternatively, you can deploy the application into your account manually via the [sns-fork-storage-backup SAR page](TODO).

### Parameters

1. `SNSTopicArn` (required) - SNS Topic ARN whose events should be backed up to S3.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for events processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all events sent to the SNS topic.
1. `BackupPrefix` (optional) - A prefix that Kinesis Data Firehose adds to the files that it delivers to the Amazon S3 bucket. If not specified, the default value of `backup/` is used.
1. `BackupCompressionFormat` (optional) - The type of compression that Kinesis Data Firehose uses to compress the data that it delivers to the Amazon S3 bucket. For valid values, see the `CompressionFormat` content for the [S3DestinationConfiguration](https://docs.aws.amazon.com/firehose/latest/APIReference/API_S3DestinationConfiguration.html) data type in the *Amazon Kinesis Data Firehose API Reference*.

### Outputs

1. `BackupBucketName` - Backup bucket name.
1. `BackupBucketArn` - Backup bucket ARN.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
