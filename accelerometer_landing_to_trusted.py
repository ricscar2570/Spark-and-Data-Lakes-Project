from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ✅ Initialize Spark Session
spark = SparkSession.builder \
    .appName("AccelerometerLandingToTrusted") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# ✅ S3 Paths
LANDING_ZONE_PATH = "s3://stedi-raw-data/accelerometer/landing/"
TRUSTED_ZONE_PATH = "s3://stedi-trusted-data/accelerometer_trusted/"

# ✅ Read JSON data dynamically
accelerometer_df = spark.read \
    .option("inferSchema", "true") \
    .json(LANDING_ZONE_PATH)

# ✅ Enable dynamic partitioning and schema updates
spark.sql("SET hive.exec.dynamic.partition = true")
spark.sql("SET hive.exec.dynamic.partition.mode = nonstrict")

# ✅ Load Customer Trusted Data
customer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/customer_trusted/")

# ✅ Ensure Correct Data Types
accelerometer_df = accelerometer_df.withColumn("timeStamp", col("timeStamp").cast("timestamp"))
customer_trusted_df = customer_trusted_df.withColumn("shareWithResearchAsOfDate", col("shareWithResearchAsOfDate").cast("timestamp"))

# ✅ Filter out records where consent date is missing
accelerometer_trusted_df = accelerometer_df.alias("a").join(
    customer_trusted_df.alias("c"),
    col("a.user") == col("c.email"),
    "inner"
).filter(
    col("a.timeStamp") >= col("c.shareWithResearchAsOfDate")  # ✅ Apply Consent Date Filter
).select("a.*")  # ✅ Keep Only Accelerometer Columns

# 🚀 Debugging: Print Final Row Count
print(f"✅ Accelerometer Readings in Trusted Zone: {accelerometer_trusted_df.count()}")

# ✅ Save to Trusted Zone
accelerometer_trusted_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .option("path", TRUSTED_ZONE_PATH) \
    .option("mergeSchema", "true") \
    .saveAsTable("stedi.accelerometer_trusted")

print("🚀 Accelerometer Trusted Data Successfully Written!")

# ✅ Stop Spark Session
spark.stop()
