## SNS Fork Pattern

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

The SNS Fork Pattern is an architectural pattern where an Amazon SNS topic is used to send messages to multiple processing pipelines. The high-level architecture looks like this:

![SNS Fork Pattern Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/images/sns-fork-pattern-architecture.png)

Each processing pipeline creates a separate subscription to the Amazon SNS topic. SNS [Subscription Filter Policies](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html) can be applied for each subscription to ensure each pipeline only receives the messages they want to process.

This repository implements the SNS Fork Pattern as a suite of Serverless applications. Each application implements general purpose, reusable message processing pipelines. All of the apps have been published to the [AWS Serverless Application Repository (SAR)](https://aws.amazon.com/serverless/serverlessrepo/) and can easily be integrated into an existing AWS SAM application using the new nested apps feature of AWS SAM/SAR. An example application is also included that demonstrates composing the different processing pipeline apps together using nested apps.

## Serverless Applications

This repository showcases the following SNS Fork pattern serverless applications:

1. [Event Storage and Backup Pipeline](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/pipelines/event-storage-backup-pipeline/README.md) - Processing pipeline that saves topic messages to an Amazon S3 bucket for use as backups or other purposes, e.g., to query with Amazon Athena.
1. [Event Search and Analytics Pipeline](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/pipelines/event-search-analytics-pipeline/README.md) - Processing pipeline that saves topic messages to an AWS Elasticsearch cluster for search and analytics.
1. [Event Replay Pipeline](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/pipelines/event-replay-pipeline/README.md) - Processing pipeline that saves topic messages to a replay buffer SQS queue. In a disaster recovery scenario, messages from up to 14 days ago can be replayed back to another processing pipeline's SQS queue.

## Examples

This repository also contains the following example applications to demonstrate the SNS Fork pattern:

1. [E-Commerce App](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/examples/ecommerce-app/checkout-api/README.md) - An example of using the SNS Fork pattern pipeline apps in an e-commerce use case.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
