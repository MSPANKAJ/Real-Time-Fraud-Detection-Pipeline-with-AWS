# Real-Time Credit Card Fraud Detection Pipeline

This repository implements a real-time fraud detection system using streaming data, Spark, Kafka, Airflow, AWS Lambda, and Redshift.

## Dataset
Download the dataset from [Kaggle Credit Card Fraud Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place `creditcard.csv` inside `kafka_producer/`.

## Components

- **Kafka Producer**: Streams CSV data row-by-row.
- **Spark Streaming**: Detects anomalies in real-time.
- **AWS Lambda**: Sends alert if fraud is detected.
- **Redshift**: Stores valid transactions.
- **Airflow**: Orchestrates the pipeline.

## AWS CLI Setup

```bash
aws configure
aws s3 mb s3://fraud-detection-pipeline-data
aws redshift create-cluster --cli-input-json file://../scripts/redshift_config.json
```

## To Run

1. Start Kafka and Zookeeper
2. Start Spark Streaming Job
3. Trigger Airflow DAG
4. Monitor Lambda Alerts


