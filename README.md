# Real-Time Anomaly Detection Pipeline

This project is a real-time data processing and machine learning pipeline for detecting anomalies in streaming data. It's built to demonstrate a practical, end-to-end MLOps workflow using containerized services and distributed computing.

## Key Features 

* **Real-Time Data Ingestion:** A Kafka producer sends a continuous stream of time-series data.
* **Streaming Analytics:** An Apache Spark streaming job processes data in real-time batches.
* **Anomaly Detection:** A pre-trained `scikit-learn` model is used to detect anomalies within the data stream.
* **Containerized Environment:** The entire application stack (Zookeeper, Kafka, Spark) is managed with Docker and Docker Compose, making it easy to set up and deploy.
* **Cloud Deployment:** The project is deployed on a live Oracle Cloud VM.

## Architecture

The project's architecture is a classic streaming pipeline. The Kafka producer acts as our data source, sending data to a Kafka topic. The Spark streaming job consumes this data, performs real-time anomaly detection, and outputs the results. Everything is orchestrated using Docker Compose on a single VM.

## Technologies Used

* **Python 3.11**: The primary programming language for the project.
* **Docker & Docker Compose**: For containerizing and orchestrating services.
* **Apache Kafka**: The message broker for real-time data streaming.
* **PySpark**: The distributed processing engine for running the ML pipeline.
* **scikit-learn**: For the anomaly detection model (`IsolationForest`).

## How to Run the Project 

**Prerequisites:**
* A Linux environment with Docker and Docker Compose installed.
* Your project code cloned from this repository.
* A pre-trained `anomaly_model.joblib` file in the `model/` directory.

**Steps:**
1.  **Start the Services:**
    ```bash
    sudo docker-compose up -d --build
    ```
2.  **Run the Kafka Producer** (in a separate terminal):
    ```bash
    sudo docker-compose exec spark python /opt/bitnami/spark/jobs/kafka_producer.py
    ```
3.  **Run the Spark Streaming Job** (in another separate terminal):
    ```bash
    sudo docker-compose exec spark /opt/bitnami/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 /opt/bitnami/spark/jobs/spark_stream_processor.py
    ```
