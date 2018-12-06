## SNS Fork Message Replay

This Serverless application provides an SNS Fork processing pipeline that saves topic messages to a replay buffer SQS queue. In a disaster recovery scenario, messages from up to 14 days ago can be replayed back to another processing pipeline's SQS queue.

## Architecture

![SNS Fork Message Replay Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/message-replay/images/message-replay-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN with an optional subscription filter policy.
1. An AWS Lambda function is mapped to the SQS queue, but the event source is initially disabled.
1. In a disaster scenario, an operator manually enables the Lambda event source mapping and the AWS Lambda function forwards the messages from the replay buffer to the given destination SQS queue.

## Installation

This app is meant to be used as part of a larger application, so the recommended way to use it is to embed it as a nested app in your serverless application. To do this, paste the following into your SAM template:

```yaml
  Replay:
    Type: AWS::Serverless::Application
    Properties:
      Location:
        ApplicationId: TODO
        SemanticVersion: 1.0.0
      Parameters:
        # SNS Topic ARN whose messages should be backed up to S3.
        SNSTopicArn: !Ref MessageTopic
        # Name of destination SQS Queue where replay messages should be sent in a disaster recovery scenario. The app assumes the queue
        # is in the same account and region as this app.
        DestinationSQSQueueName: !GetAtt OtherPipelineQueue.QueueName
        # Retention period in seconds for the replay buffer SQS queue. This controls how long messages will be stored in the replay buffer.
        #ReplayBufferRetentionPeriodInSeconds: 1209600 # Uncomment to override default value
```

Alternatively, you can deploy the application into your account manually via the [sns-fork-message-replay SAR page](TODO).

### Parameters

1. `SNSTopicArn` (required) - SNS Topic ARN whose messages should be backuped up to S3.
1. `DestinationSQSQueueName` (required) - Name of destination SQS Queue where replay messages should be sent in a disaster recovery scenario. The app assumes the queue is in the same account and region as this app.
1. `SubscriptionFilterPolicy` (optional) - SNS Topic Subscription FilterPolicy as a JSON string. This optional parameter allows you to configure message filtering for messages processed by this app. See [the documentation](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) for details. The default behavior is to use no subscription filter policy so the app will backup all messages sent to the SNS topic.
1. `ReplayBufferRetentionPeriodInSeconds` (optional) - Retention period in seconds for the replay buffer SQS queue. This controls how long messages will be stored in the replay buffer. If not specified, the default value of `1209600` (14 days) is used.

### Outputs

1. `ReplayMessagesFunctionName` - Replay messages Lambda function name.
1. `ReplayMessagesFunctionArn` - Replay messages Lambda function ARN.
1. `ReplayMessagesEventSourceMappingId` - Id of event source mapping of Replay buffer SQS queue to ReplayMessages Lambda function.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.