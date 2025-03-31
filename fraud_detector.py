from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("FraudDetection").getOrCreate()
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "creditcard_topic").load()
json_df = df.selectExpr("CAST(value AS STRING) as json").selectExpr("from_json(json, 'amount DOUBLE, class INT') as data").select("data.*")
fraud_df = json_df.filter(col("class") == 1)
fraud_df.writeStream.format("console").start().awaitTermination()
