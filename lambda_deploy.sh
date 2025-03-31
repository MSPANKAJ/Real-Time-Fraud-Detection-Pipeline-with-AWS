#!/bin/bash

zip lambda.zip lambda_handler.py

aws lambda create-function \
  --function-name FraudAlertHandler \
  --runtime python3.9 \
  --role arn:aws:iam::<851725438992>:role/lambda-exec-role \
  --handler lambda_handler.lambda_handler \
  --zip-file fileb://lambda.zip