import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("CustomerLandingToTrusted") \
    .config("spark.sql.catalogImplementation", "hive") \
    .getOrCreate()

# S3 Paths
LANDING_ZONE_PATH = "s3://stedi-raw-data/customer/landing/"
TRUSTED_ZONE_PATH = "s3://stedi-trusted-data/customer_trusted/"

# Read JSON data dynamically
customer_df = spark.read \
    .option("inferSchema", "true") \
    .json(LANDING_ZONE_PATH)

# Enable dynamic partitioning and schema updates
spark.sql("SET hive.exec.dynamic.partition = true")
spark.sql("SET hive.exec.dynamic.partition.mode = nonstrict")

# Filter customers who shared data for research
customer_trusted_df = customer_df.filter(col("shareWithResearchAsOfDate").isNotNull())

# Write data to Glue Data Catalog with schema evolution enabled
customer_trusted_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .option("path", TRUSTED_ZONE_PATH) \
    .saveAsTable("stedi.customer_trusted")

# Stop Spark Session
spark.stop()
