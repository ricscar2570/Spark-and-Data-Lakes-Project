import sys
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("CustomerTrustedToCurated").getOrCreate()

# S3 Paths
CUSTOMER_TRUSTED_PATH = "s3://stedi-trusted-data/customer_trusted/"
ACCELEROMETER_TRUSTED_PATH = "s3://stedi-trusted-data/accelerometer_trusted/"
CURATED_ZONE_PATH = "s3://stedi-curated-data/customer_curated/"

# Read Customer Trusted Data
customer_trusted_df = spark.read.parquet(CUSTOMER_TRUSTED_PATH)

# Read Accelerometer Trusted Data
accelerometer_trusted_df = spark.read.parquet(ACCELEROMETER_TRUSTED_PATH).select("user").distinct()

# Join with accelerometer users and remove PII
customer_curated_df = customer_trusted_df.join(accelerometer_trusted_df, customer_trusted_df.email == accelerometer_trusted_df.user, "inner") \
    .select("serialNumber", "registrationDate", "shareWithResearchAsOfDate")

# Write anonymized data to Curated Zone
customer_curated_df.write.mode("overwrite").parquet(CURATED_ZONE_PATH)

# Stop Spark Session
spark.stop()
