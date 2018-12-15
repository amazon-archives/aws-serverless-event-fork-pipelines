## SNS Fork Pattern

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

The SNS Fork Pattern is an architectural pattern where an Amazon SNS topic is used to send messages to multiple processing pipelines. The high-level architecture looks like this:

![SNS Fork Pattern Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/images/sns-fork-pattern-architecture.png)

Each processing pipeline creates a separate subscription to the Amazon SNS topic. SNS [Subscription Filter Policies](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html) can be applied for each subscription to ensure each pipeline only receives the messages they want to process.

This repository implements the SNS Fork Pattern as a suite of Serverless applications. Each application implements general purpose, reusable message processing pipelines. All of the apps have been published to the [AWS Serverless Application Repository (SAR)](https://aws.amazon.com/serverless/serverlessrepo/) and can easily be integrated into an existing AWS SAM application using the new nested apps feature of AWS SAM/SAR. An example application is also included that demonstrates composing the different processing pipeline apps together using nested apps.

## Serverless Applications

This repository includes the following serverless apps:

1. [Storage and Backup](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/storage-backup/README.md) - Processing pipeline that saves topic messages to an Amazon S3 bucket for use as backups or other purposes, e.g., to query with Amazon Athena.
1. [Search and Analytics](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/search-analytics/README.md) - Processing pipeline that saves topic messages to an AWS Elasticsearch cluster for search and analytics.
1. [Message Replay](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/blob/master/message-replay/README.md) - Processing pipeline that saves topic messages to a replay buffer SQS queue. In a disaster recovery scenario, messages from up to 14 days ago can be replayed back to another processing pipeline's SQS queue.
1. SNS Fork Example (TODO: link to SAR app page) - Example application showing how the above pipelines can be used in an AWS SAM application.

## Deploying the SNS Fork Example app

Deploying the SNS Fork Example application is simple using the Serverless Application Repository. There is no need to build or package the application from the repository source code. Simply follow these steps:

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login.
1. Go to the [sns-fork-example]() app's page on the Serverless Application Repository and click "Deploy".
1. Edit the stack name if you would like and click "Deploy".

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
