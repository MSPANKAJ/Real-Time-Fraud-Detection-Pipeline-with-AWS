from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import subprocess

def start_spark_job():
    subprocess.run(["spark-submit", "--master", "local", "../spark_streaming/fraud_detector.py"])

def run_lambda_alert():
    subprocess.run(["python3", "../lambda_function/send_alert.py"])

default_args = {"start_date": datetime(2024, 1, 1)}
with DAG("fraud_pipeline_dag", schedule_interval="@hourly", default_args=default_args, catchup=False) as dag:
    spark_task = PythonOperator(task_id="start_spark", python_callable=start_spark_job)
    alert_task = PythonOperator(task_id="run_alert", python_callable=run_lambda_alert)
    spark_task >> alert_task
