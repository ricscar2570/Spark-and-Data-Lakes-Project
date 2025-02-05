import sys
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("MachineLearningCurated").getOrCreate()

# S3 Paths
STEP_TRAINER_TRUSTED_PATH = "s3://stedi-trusted-data/step_trainer_trusted/"
ACCELEROMETER_TRUSTED_PATH = "s3://stedi-trusted-data/accelerometer_trusted/"
CURATED_ZONE_PATH = "s3://stedi-curated-data/machine_learning_curated/"

# Read Trusted Datasets
step_trainer_df = spark.read.parquet(STEP_TRAINER_TRUSTED_PATH)
accelerometer_df = spark.read.parquet(ACCELEROMETER_TRUSTED_PATH)

# Print columns for debugging
print("Step Trainer Columns: ", step_trainer_df.columns)
print("Accelerometer Columns: ", accelerometer_df.columns)

# Ensure correct timestamp column names
step_trainer_df = step_trainer_df.withColumnRenamed("sensorReadingTime", "timestamp_step")
accelerometer_df = accelerometer_df.withColumnRenamed("timeStamp", "timestamp_accel")

# Perform Join on corrected timestamp columns
machine_learning_df = step_trainer_df.join(accelerometer_df, step_trainer_df.timestamp_step == accelerometer_df.timestamp_accel, "inner")

# Drop duplicate timestamp column
machine_learning_df = machine_learning_df.drop("timestamp_accel")

# Write to Curated Zone
machine_learning_df.write.mode("overwrite").parquet(CURATED_ZONE_PATH)

# Stop Spark Session
spark.stop()
