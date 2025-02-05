import sys
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("StepTrainerLandingToTrusted") \
    .config("spark.sql.catalogImplementation", "hive") \
    .getOrCreate()

# S3 Paths
LANDING_ZONE_PATH = "s3://stedi-raw-data/step_trainer/landing/"
TRUSTED_ZONE_PATH = "s3://stedi-trusted-data/step_trainer_trusted/"
CUSTOMER_CURATED_PATH = "s3://stedi-curated-data/customer_curated/"

# Read JSON data
step_trainer_df = spark.read.option("inferSchema", "true").json(LANDING_ZONE_PATH)
customer_curated_df = spark.read.parquet(CUSTOMER_CURATED_PATH).select("serialNumber")

# Join & save
step_trainer_trusted_df = step_trainer_df.join(customer_curated_df, "serialNumber", "inner")
step_trainer_trusted_df.write.mode("overwrite").parquet(TRUSTED_ZONE_PATH)

spark.stop()
