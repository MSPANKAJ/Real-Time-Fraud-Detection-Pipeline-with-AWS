LLM Driven Fraud Detection Stream Processing System


This project demonstrates a real-time fraud detection pipeline built on a streaming architecture. It shows how machine learning and large language models can work together to improve fraud alerts with both accuracy and context.

Overview

The system ingests transaction data in real time, scores it for fraud risk, and sends alerts for suspicious activity. A traditional model (XGBoost) handles the fraud detection, while a lightweight LLM service generates plain-language explanations and recommended actions for flagged transactions.

How It Works!!

1. Data ingestion
producer.py streams transactions from a sample dataset (creditcard.csv) into a Kafka topic called creditcard_topic.

2. Real-time scoring
A Spark Structured Streaming job (fraud_detector.py) reads from Kafka, generates features, and uses an XGBoost model to assign a fraud risk score to each transaction. Transactions over a set threshold are marked as potentially fraudulent.

3. Adding explanations
For flagged transactions, the stream calls a small FastAPI service (llm/service.py).

This service can run in mock mode, or connect to AWS Bedrock or OpenAI, and returns:

1. a short reason for why the transaction is suspicious
2. suggested actions for the fraud team
3. a confidence score for its explanation

The Spark helper in stream/llm_enricher.py attaches these fields to the transaction.

Alerting
The enriched transaction is sent to an AWS Lambda function (lambda_function/send_alert.py) which sends an email alert through Amazon SES. The alert includes the model risk score, the LLM’s reason, and the recommended next steps.

Storage and reporting
The design includes storing scored transactions in S3 or Redshift for dashboards, drift monitoring, and retraining, with example Redshift configuration in redshift.json.

Orchestration
An example Airflow DAG (fraud_pipeline_dag.py) shows how the Spark job and alert step can be orchestrated for batch or demo runs.

Key Features
1. Real-time processing of streaming transactions with Kafka and Spark

2. XGBoost for high-precision fraud detection on tabular features

3. LLM-based explanations and recommendations for analysts

Email alerts sent through AWS SES via Lambda
Configurable through environment variables and simple YAML/JSON config files

Why the LLM Step Matters
Before the LLM service was added, alerts were generic and left analysts to work out the reason for each flag. Now each alert includes a concise explanation of why the transaction is suspicious and what actions to take. This reduces investigation time and improves consistency in handling cases.

Project Structure

producer.py                  # Sends sample transactions to Kafka
fraud_detector.py             # Spark job for feature gen + XGBoost scoring
stream/llm_enricher.py        # Spark UDF that calls the LLM service
llm/service.py                # FastAPI service that generates explanations
lambda_function/send_alert.py # Lambda code to send SES email alerts
fraud_pipeline_dag.py         # Airflow DAG to orchestrate Spark + alert steps
config.yaml                   # Kafka and threshold config
redshift.json                 # Example Redshift cluster config
Intended Use
This code is for learning and discussion. It is not production-ready and does not include full security, scaling, or deployment configuration. The focus is on showing how traditional ML and LLMs can be combined in a streaming fraud detection workflow.
