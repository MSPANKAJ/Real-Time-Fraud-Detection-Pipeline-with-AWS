import pandas as pd
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))
df = pd.read_csv('creditcard.csv')

for _, row in df.iterrows():
    msg = row.to_dict()
    producer.send('creditcard_topic', msg)
    time.sleep(0.05)
