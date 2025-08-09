import os
import joblib
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("AnomalyDetectionStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()
    
spark.sparkContext.setLogLevel("ERROR")

# Define the schema for our data
base_schema = StructType([
    StructField("feature1", DoubleType()),
    StructField("feature2", DoubleType()),
    StructField("timestamp", DoubleType())
])

# Load the pre-trained model as a broadcast variable
model_path = "/opt/bitnami/spark/model/anomaly_model.joblib"
model = joblib.load(model_path)
broadcast_model = spark.sparkContext.broadcast(model)

# UDF to apply the scikit-learn model
def predict_anomaly(iterator):
    model = broadcast_model.value
    for pdf in iterator:
        predictions = model.predict(pdf[['feature1', 'feature2']])
        yield pdf.assign(anomaly=predictions)

# Read from Kafka topic
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "time-series-data") \
    .load()

# Parse JSON data and process the stream
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_data") \
    .select(from_json(col("json_data"), base_schema).alias("data")) \
    .select("data.*")
    
# Define the complete output schema for the mapInPandas UDF
output_schema = StructType(base_schema.fields + [StructField("anomaly", IntegerType(), False)])

# Apply the UDF to detect anomalies
anomaly_df = parsed_df.mapInPandas(predict_anomaly, schema=output_schema)

# Add a user-friendly status column based on the integer predictions
final_df = anomaly_df.withColumn("anomaly_status", 
    when(col("anomaly") == 1, "Normal") \
    .when(col("anomaly") == -1, "Anomaly") \
    .otherwise("Unknown")
)

# Select the final columns to display in the console
console_output_df = final_df.select("timestamp", "feature1", "feature2", "anomaly_status")

# Start the streaming query
query = console_output_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()