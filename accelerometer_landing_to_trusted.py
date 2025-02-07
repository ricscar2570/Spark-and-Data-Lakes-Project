from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ✅ Initialize Spark Session
spark = SparkSession.builder.appName("AccelerometerTrusted").getOrCreate()

# ✅ Load Accelerometer Landing Data
accelerometer_landing_df = spark.read.option("inferSchema", "true").json("s3://stedi-raw-data/accelerometer/landing/")

# ✅ Load Customer Trusted Data
customer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/customer_trusted/")

# ✅ Ensure Correct Data Types
accelerometer_landing_df = accelerometer_landing_df.withColumn("timeStamp", col("timeStamp").cast("timestamp"))
customer_trusted_df = customer_trusted_df.withColumn("shareWithResearchAsOfDate", col("shareWithResearchAsOfDate").cast("timestamp"))

# 🚀 Debugging: Print Initial Row Counts
print(f"✅ Total Accelerometer Readings in Landing: {accelerometer_landing_df.count()}")
print(f"✅ Customers in Trusted Zone: {customer_trusted_df.count()}")

# ✅ Join Accelerometer with Customer Trusted Data
accelerometer_trusted_df = accelerometer_landing_df.alias("a").join(
    customer_trusted_df.alias("c"),
    col("a.user") == col("c.email"),
    "inner"
).filter(
    col("a.timeStamp") >= col("c.shareWithResearchAsOfDate")  # ✅ Apply Consent Date Filter
).select("a.*")  # Keep only Accelerometer Data

# 🚀 Debugging: Print Final Row Count After Filtering
print(f"✅ Total Accelerometer Readings in Trusted Zone (After Consent Filtering): {accelerometer_trusted_df.count()}")

# ✅ Save to Trusted Zone
accelerometer_trusted_df.write.mode("overwrite").parquet("s3://stedi-trusted-data/accelerometer_trusted/")

print("🚀 Accelerometer Trusted Data Successfully Written!")

spark.stop()
