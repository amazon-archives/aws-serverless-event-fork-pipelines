# SNS Fork Pattern: E-Commerce Pipeline

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This checkout pipeline is meant to be nested in the example e-commerce application that implements the Amazon SNS Fork pattern.

## App Architecture

![SNS Fork Checkout Pipeline Architecture](https://github.com/aws-samples/aws-serverless-sns-fork-pattern/raw/master/examples/ecommerce-app/checkout-pipeline/images/checkout-pipeline-architecture.png)

1. An Amazon SQS queue is subscribed to the given SNS Topic ARN of checkout events.
1. An AWS Lambda function reads events from the SQS queue and writes order data to an Amazon DynamoDB table called "Orders".
    1. The Lambda function provides an environment variable that allows a data corruption bug to be turned on and off in order to demo usage of the fork-event-replay-pipeline app.

## Installation Instructions

This app is not meant to be installed directly in isolation. It's used as a nested application in the fork-example-ecommerce-api app. You should install the fork-example-ecommerce-api app, which will automatically install this app as well.

## App Parameters

1. `SNSTopicArn` (required) - Checkout events SNS Topic ARN.
1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO

## App Outputs

1. `CheckoutFunctionName` - Checkout Lambda function name.
1. `CheckoutFunctionArn` - Checkout Lambda function ARN.
1. `CheckoutTableName` - Checkout DynamoDB table name.
1. `CheckoutTableArn` - Checkout DynamoDB table ARN.
1. `CheckoutQueueUrl` - Checkout SQS queue URL.
1. `CheckoutQueueArn` - Checkout SQS queue ARN.
1. `CheckoutQueueName` - Checkout SQS queue name.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
