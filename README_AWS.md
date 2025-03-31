# Real-Time Credit Card Fraud Detection Pipeline – AWS Deployment

This repository contains a complete, production-grade data engineering pipeline that detects fraudulent credit card transactions in real time. The project integrates Kafka, Spark Structured Streaming, AWS Lambda, Redshift, and Airflow to simulate a real-world streaming data use case.

---

## Architecture Overview

- **Apache Kafka**: Streams incoming credit card transactions.
- **Apache Spark (Structured Streaming)**: Performs real-time fraud detection logic.
- **AWS Lambda**: Sends fraud alerts when anomalies are identified.
- **Amazon Redshift**: Stores cleaned and labeled transaction data.
- **Apache Airflow**: Orchestrates the entire pipeline end-to-end.

---

## Setup Summary (Fully Implemented)

### 1. S3 Bucket and Dataset Upload

Created S3 bucket and uploaded dataset from Kaggle:
```bash
aws s3 mb s3://fraud-stream-bucket
aws s3 cp creditcard.csv s3://fraud-stream-bucket/
```

### 2. Spark Streaming on EMR

- Configured an EMR cluster with Spark to run `fraud_detector.py`
- Subscribed to Kafka topic for transaction stream ingestion
- Used ML model logic to detect anomalies
- Pushed flagged data to Amazon Redshift

### 3. Airflow DAG Orchestration

- Deployed `fraud_detection_dag.py` to Airflow (via EC2 or MWAA)
- DAG Tasks:
  - Start Spark Streaming job
  - Trigger Lambda for fraud alerts
  - Archive processed files to S3

### 4. AWS Lambda Fraud Alert Setup

Created and deployed Lambda function for real-time alerts:
```bash
zip lambda.zip lambda_handler.py
aws lambda create-function   --function-name FraudAlertHandler   --runtime python3.9   --role arn:aws:iam::<ACCOUNT_ID>:role/lambda-exec-role   --handler lambda_handler.lambda_handler   --zip-file fileb://lambda.zip
```

Lambda ARN: `arn:aws:lambda:us-east-2:851725438992:function:FraudAlertHandler`

### 5. Redshift Table Schema

Executed the following SQL on Redshift:
```sql
CREATE TABLE fraud_detection (
    time FLOAT,
    v1 FLOAT, v2 FLOAT, v3 FLOAT, v4 FLOAT, v5 FLOAT, v6 FLOAT, v7 FLOAT, v8 FLOAT,
    v9 FLOAT, v10 FLOAT, v11 FLOAT, v12 FLOAT, v13 FLOAT, v14 FLOAT, v15 FLOAT,
    v16 FLOAT, v17 FLOAT, v18 FLOAT, v19 FLOAT, v20 FLOAT, v21 FLOAT, v22 FLOAT,
    v23 FLOAT, v24 FLOAT, v25 FLOAT, v26 FLOAT, v27 FLOAT, v28 FLOAT,
    amount FLOAT,
    class INT
);
```

- Data ingestion handled via Spark connector or `COPY` command.

### 6. Pipeline Execution Flow

1. Kafka produces streaming transactions.
2. Spark processes the stream and flags suspicious records.
3. Redshift stores transaction records.
4. Lambda triggers fraud alert logic.
5. Airflow schedules and monitors the pipeline.

---

## IAM Role Summary

- **Lambda**: Read/write to S3 and CloudWatch logging
- **EMR/Glue**: S3 access and Redshift write permissions
- **Redshift**: IAM role with COPY permissions from S3 bucket via IAM Role

---

## Dataset Reference

Source: [Kaggle Credit Card Fraud Detection Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)  
- 284,807 transactions  
- 492 frauds (highly imbalanced)  
- Anonymized PCA features (V1 to V28)

---

## Tech Stack

- Python 3.9, PySpark
- Apache Kafka, Spark Structured Streaming
- AWS Lambda, Redshift, S3, EMR
- Apache Airflow (EC2/MWAA)
- IAM, Terraform (optional)

---

## Contributing

Contributions are welcome. You can suggest improvements, open issues, or submit pull requests for:
- Monitoring integrations (Prometheus, Grafana)
- Support for Kinesis or Athena
- Real-time dashboards or visualization tools

---

## Author

**Pankaj M Sajjanar**  
Data Engineer | [LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/)

---

## License

This project is licensed under the MIT License.