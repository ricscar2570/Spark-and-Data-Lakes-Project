import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("AccelerometerLandingToTrusted") \
    .config("spark.sql.catalogImplementation", "hive") \
    .getOrCreate()

# S3 Paths
LANDING_ZONE_PATH = "s3://stedi-raw-data/accelerometer/landing/"
TRUSTED_ZONE_PATH = "s3://stedi-trusted-data/accelerometer_trusted/"
CUSTOMER_TRUSTED_PATH = "s3://stedi-trusted-data/customer_trusted/"

# Read JSON dynamically
accelerometer_df = spark.read.option("inferSchema", "true").json(LANDING_ZONE_PATH)
customer_trusted_df = spark.read.parquet(CUSTOMER_TRUSTED_PATH).select("email", "shareWithResearchAsOfDate")

# Convert timestamps
customer_trusted_df = customer_trusted_df.withColumn("shareWithResearchAsOfDate", to_timestamp(col("shareWithResearchAsOfDate")))
accelerometer_df = accelerometer_df.withColumn("timeStamp", to_timestamp(col("timeStamp")))

# Join with customer data and filter old timestamps
accelerometer_trusted_df = accelerometer_df.join(customer_trusted_df, accelerometer_df.user == customer_trusted_df.email, "inner") \
    .filter(col("timeStamp") >= col("shareWithResearchAsOfDate")) \
    .drop("email", "shareWithResearchAsOfDate")

# Save as Parquet with Schema Evolution
accelerometer_trusted_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .option("path", TRUSTED_ZONE_PATH) \
    .saveAsTable("stedi.accelerometer_trusted")

spark.stop()
