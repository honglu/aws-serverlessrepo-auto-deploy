# aws-serverlessrepo-auto-deploy ![Build Status](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVlI5bVYxaVduUnFmMFhMeFRNUjY3eTJROC93RThlRjZmZmNCKzNzQnNJNnZYZHUyNzlYd0VTbTZ3T0ZZakhkRmJNdklUSFc2YnMzeXZuQ0pIaGlxQnlRPSIsIml2UGFyYW1ldGVyU3BlYyI6IjNIVTNYSFpVTk1nTGt2ZUciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)
This serverless application automatically deploys new versions of an serverless app in AWS Serverless Application repository into your account.

## App Architecture

TODO: arch diagram

## Installation Instructions

1. [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and login
1. Go to the app's page on the [Serverless Application Repository](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:303769779339:applications~aws-serverlessrepo-auto-deploy) and click "Deploy"
1. Click "Copy as SAM Resource"
1. Create your own SAM template by pasting the application resource into your SAM template and fill in the parameters (see parameter details below)
1. Add any permissions that are required to deploy the application you would like to setup the auto deploy as `AWS::IAM::Policy` resource in your SAM template. See [Example](https://github.com/honglu/aws-serverlessrepo-auto-deploy/raw/master/examples/example-template.yml)
1. Deploy your SAM template: ```sam deploy --template-file <path-to-your-sam-template> --stack-name <your-stack-name> --capabilities CAPABILITY_AUTO_EXPAND```

## App Parameters

1. `LogLevel` (optional) - Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: INFO
1. `ApplicationId` (required) - The application id of the application in AWS Serverless Application Repository.
1. `StackName` (required) - The stack name for the application. If you already have a stack that is created by AWS Serverless Application Repository, please provide the stack name you used when you created the stack via AWS Serverless Application Repository. For example, the stack name without `serverlessrepo-` prefix.
1. `ParameterOverrides` (optional) - A JSON string representation of the parameter overrides for the application.
1. `Capabilities` (optional) - A JSON string representation of the capabilities for the application.

## App Outputs

1. `ApplicationAutoDeployerFunctionName` - Application Auto Deployer Lambda function name.
1. `ApplicationAutoDeployerFunctionArn` - Application Auto Deployer Lambda function ARN.
1. `ApplicationAutoDeployerRoleName` - Application Auto Deployer Lambda function role name.
1. `ApplicationAutoDeployerRoleArn` - Application Auto Deployer Lambda function role ARN.

## License Summary

This code is made available under the MIT license. See the LICENSE file.