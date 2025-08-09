from kafka import KafkaProducer
import json
import time
import numpy as np

# Kafka broker connection
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'time-series-data'

# Generate and send data
def generate_data():
    while True:
        # Generate normal data points
        data = {
            'feature1': np.random.randn(),
            'feature2': np.random.randn(),
            'timestamp': time.time()
        }
        # Occasionally send an anomaly
        if np.random.rand() < 0.02: # 2% chance of anomaly
            data['feature1'] = 5 * np.random.randn()
            data['feature2'] = 5 * np.random.randn()

        producer.send(topic_name, json.dumps(data).encode('utf-8'))
        print(f"Sent data: {data}")
        time.sleep(1)

if __name__ == "__main__":
    generate_data()