import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

# Initialize Spark Session
spark = SparkSession.builder.appName("AccelerometerLandingToTrusted").getOrCreate()

# S3 Paths
LANDING_ZONE_PATH = "s3://stedi-raw-data/accelerometer/landing/"
TRUSTED_ZONE_PATH = "s3://stedi-trusted-data/accelerometer_trusted/"
CUSTOMER_TRUSTED_PATH = "s3://stedi-trusted-data/customer_trusted/"

# Read Accelerometer Data
accelerometer_df = spark.read.json(LANDING_ZONE_PATH)

# Read Customer Trusted Data
customer_trusted_df = spark.read.parquet(CUSTOMER_TRUSTED_PATH).select("email", "shareWithResearchAsOfDate")

# Convert shareWithResearchAsOfDate to timestamp format
customer_trusted_df = customer_trusted_df.withColumn("shareWithResearchAsOfDate", to_timestamp(col("shareWithResearchAsOfDate")))

# Read Accelerometer data and convert timestamp
accelerometer_df = accelerometer_df.withColumn("timeStamp", to_timestamp(col("timeStamp")))

# Join and filter out readings before research consent date
accelerometer_trusted_df = accelerometer_df.join(customer_trusted_df, accelerometer_df.user == customer_trusted_df.email, "inner") \
    .filter(col("timeStamp") >= col("shareWithResearchAsOfDate")) \
    .drop("email", "shareWithResearchAsOfDate")

# Write the filtered data to the Trusted Zone
accelerometer_trusted_df.write.mode("overwrite").parquet(TRUSTED_ZONE_PATH)

# Stop Spark Session
spark.stop()
