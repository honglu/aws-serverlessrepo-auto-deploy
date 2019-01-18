# aws-serverlessrepo-auto-deploy ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVlI5bVYxaVduUnFmMFhMeFRNUjY3eTJROC93RThlRjZmZmNCKzNzQnNJNnZYZHUyNzlYd0VTbTZ3T0ZZakhkRmJNdklUSFc2YnMzeXZuQ0pIaGlxQnlRPSIsIml2UGFyYW1ldGVyU3BlYyI6IjNIVTNYSFpVTk1nTGt2ZUciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

This serverless application automatically deploys new versions of an serverless app in AWS Serverless Application repository into your account.

## App Architecture

TODO: arch diagram

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to the app's page on the [Serverless Application Repository](TODO) and click "Deploy"
1. Provide the required app parameters (see parameter details below) and click "Deploy"

## App Parameters

1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO
1. ...

## App Outputs

1. `MyFunctionName` - My Lambda function name.
1. ...

## License Summary

This code is made available under the TODO license. See the LICENSE file.