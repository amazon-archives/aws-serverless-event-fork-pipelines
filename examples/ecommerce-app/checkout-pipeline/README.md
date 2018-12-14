# SNS Fork Pattern: E-commerce Pipeline

This serverless application implements a SNS Fork pattern pipeline for checkout events in an example e-commerce application.

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

1. `ProcessRecordsFunctionName` - Lambda function name.
1. `ProcessRecordsFunctionArn` - Lambda function ARN.
1. `OrdersName` - Orders table name.
1. `OrdersArn` - Orders table ARN.
1. `QueueUrl` - Checkout events queue URL.
1. `QueueArn` - Checkout events queue ARN.
1. `QueueName` - Checkout events queue name.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.