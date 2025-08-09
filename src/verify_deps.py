import sys
import os
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("VerificationJob") \
    .getOrCreate()

print("--- Spark Context initialized ---")

# This function will run on a Spark worker
def verify_paths(x):
    return (list(sys.path), os.listdir('.'))

# Create a small RDD to trigger a Spark job
data = [1, 2]
rdd = spark.sparkContext.parallelize(data)

# Map the function to the RDD and collect the results
result = rdd.map(verify_paths).collect()

print("\n--- Verification Output ---")
print(f"Python path (sys.path) on worker: \n {result[0][0]}")
print(f"Files in worker directory: \n {result[0][1]}")
print("---------------------------\n")

spark.stop()