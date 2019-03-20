# AWS Event Fork Pipelines: E-Commerce Example

![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoidEVpU1Nmd0gzaEtUaE1XWGo3OVY3dmVDTVRBUllsUXFlbTZZQS9pZkRDaGhKZFZkczZEQVJLcEovQko3VmpYeHZrQ24wL041bWI4SWUyUUxJMDhHbXRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IjZESXdFTTJBd2RWZGVKSXEiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This serverless application is an example of using the AWS Event Fork Pipelines apps in an e-commerce use case.

## App Architecture

![AWS Event Fork Pipelines E-Commerce Architecture](https://github.com/aws-samples/aws-serverless-event-fork-pipelines/raw/master/examples/ecommerce-app/checkout-api/images/ecommerce-architecture.png)

1. The e-commerce application takes orders from buyers through a RESTful API, which is hosted by Amazon API Gateway and is backed by an AWS Lambda function named “Checkout”.
1. This function publishes all orders received to an Amazon SNS topic named “CheckoutEvents”, which in turn fans out the orders to four different pipelines.
1. The first pipeline is the regular checkout processing pipeline designed and implemented by the e-commerce application owner, which saves all orders to an Amazon DynamoDB table.
1. The second pipeline is the fork-event-storage-backup-pipeline app, which is configured to remove sensitive data from the events and save them to a backup S3 bucket, compressed and encrypted at rest.
1. The third pipeline is the fork-event-search-analytics-pipeline app, which is configured to save events for orders where the amount was greater than or equal to 100 USD to an Amazon Elasticsearch Service Domain.
1. The fourth pipeline is the fork-event-replay-pipeline app, which is configured to buffer events for replay to the checkout pipeline in the event of a disaster scenario. The checkout pipeline's event processing functions comes with the ability to simulate a data corruption bug scenario to demo the replay app.

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to this app's [page on the Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:077246666028:applications~fork-example-ecommerce-checkout-api) and click "Deploy"
1. Provide the required app parameters (see parameter details below) and click "Deploy"

## App Parameters

1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO

## App Outputs

1. `CheckoutApiUri` - Checkout API Prod stage URI.
1. `CheckoutApiBackendFunctionName` - Checkout API handler Function Name.
1. `CheckoutApiBackendFunctionArn` - Checkout API handler Function ARN.
1. `CheckoutEventsTopicName` - Checkout events SNS topic name.
1. `CheckoutEventsTopicArn` - Checkout events SNS topic ARN.

## Testing the app

Once the app has been deployed to your account, go to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home) and find the top-level stack. It will be named something like serverlessrepo-fork-example-ecommerce-api. Click on the stack details and find the CheckoutApiUri output. This is the API endpoint to send checkout events to.

Using a tool like curl or postman, send checkout events by POSTing to the endpoint. Checkout events must be in the following format:

```json
{
    "id": 15311,
    "date": "2018-12-15T23:41:11-08:00",
    "status": "confirmed",
    "customer": {
        "id": 65144,
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    "payment": {
        "id": 2509,
        "amount": 450.00,
        "currency": "usd",
        "method": "credit",
        "card-network": "visa",
        "card-number": "1234 5678 9012 3456",
        "card-expiry": "10/2022",
        "card-owner": "John Doe",
        "card-cvv": "123"
    },
    "shipping": {
        "id": 7600,
        "time": 2,
        "unit": "days",
        "method": "courier"
    },
    "items": [
        {
            "id": 6512,
            "product": 8711,
            "name": "Hockey Jersey - Canucks - Large",
            "quantity": 1,
            "price": 400.00,
            "subtotal": 400.00
        }, {
            "id": 9954,
            "product": 7600,
            "name": "Hockey Puck - Bauer",
            "quantity": 2,
            "price": 25.00,
            "subtotal": 50.00
        }
    ]
}
```

Here is an example of using curl on a unix system to send a test event, assuming the file `test_event.json` contains the test event above:

```bash
curl -d "$(cat test_event.json)" https://<your api id>.execute-api.us-east-1.amazonaws.com/Prod/checkout
```

Exercises:

1. POST checkout events to the API endpoint and confirm the checkout pipeline has written them to the DynamoDB table.
1. Send events and confirm they have been written to the S3 backups bucket. Confirm credit card information has been removed from backup data.
1. Send events with amounts above and below 100 USD. Confirm only the events greater than or equal to 100 USD are visible in the Elasticsearch Domain.
1. Find the checkout-pipeline ProcessRecords Lambda function.
    1. Change its BUG_ENABLED environment variable to true and save the function configuration.
    1. Send more checkout events to the API. Confirm the data in DynamoDB is corrupted by the bug.
    1. Go to the [SQS console](https://console.aws.amazon.com/sqs/home) and note that the ReplayBuffer SQS queue has messages available.
    1. Change the BUG_ENABLED environment variable back to false and save the function configuration. This simulates fixing the data corruption bug.
    1. Find the ReplayMessages Lambda function and enable its SQS event source trigger. Confirm the data in DynamoDB is eventually fixed.
    1. Confirm in the [SQS console](https://console.aws.amazon.com/sqs/home) that the ReplayBuffer SQS queue is now empty (messages were sent to the checkout pipeline).
    1. Disable the SQS event source trigger on the ReplayMessages Lambda function again so it can buffer any new checkout events.

## License Summary

This sample code is made available under a modified MIT license. See the LICENSE file.
