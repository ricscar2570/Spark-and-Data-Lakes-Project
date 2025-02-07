from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime

# ✅ Initialize Spark Session
spark = SparkSession.builder.appName("CustomerCuratedFix").getOrCreate()

# ✅ Load Data from S3
customer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/customer_trusted/")
accelerometer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/accelerometer_trusted/")

# ✅ Check Schema Before Processing
print("📌 Customer Trusted Schema BEFORE Processing:")
customer_trusted_df.printSchema()

print("📌 Accelerometer Trusted Schema BEFORE Processing:")
accelerometer_trusted_df.printSchema()

# ✅ Convert `shareWithResearchAsOfDate` to Timestamp if Needed
if dict(customer_trusted_df.dtypes)["shareWithResearchAsOfDate"] != "timestamp":
    customer_trusted_df = customer_trusted_df.withColumn(
        "shareWithResearchAsOfDate", col("shareWithResearchAsOfDate").cast("timestamp")
    )

# ✅ Convert `timeStamp` to Timestamp if Needed
if dict(accelerometer_trusted_df.dtypes)["timeStamp"] != "timestamp":
    accelerometer_trusted_df = accelerometer_trusted_df.withColumn(
        "timeStamp", col("timeStamp").cast("timestamp")
    )

# ✅ Check Schema After Processing
print("📌 Customer Trusted Schema AFTER Processing:")
customer_trusted_df.printSchema()

print("📌 Accelerometer Trusted Schema AFTER Processing:")
accelerometer_trusted_df.printSchema()

customer_curated_df = customer_trusted_df.alias("c").join(
    accelerometer_trusted_df.alias("a"),
    col("c.email") == col("a.user"),
    "inner"
).filter(
    (col("c.shareWithResearchAsOfDate").isNotNull()) &  
    (col("a.timeStamp").isNotNull()) &  
    (col("a.timeStamp") >= col("c.shareWithResearchAsOfDate"))  # ✅ Apply Consent Date Filter
).select("c.*").dropDuplicates(["email"])  # ✅ Ensure Unique Customers

# 🚀 Debugging: Print Final Row Count
print(f"✅ Customers in Trusted: {customer_trusted_df.count()}")
print(f"✅ Accelerometer Trusted Rows: {accelerometer_trusted_df.count()}")
print(f"✅ Customers in Curated Zone: {customer_curated_df.count()}")

# ✅ Save to S3 in CORRECT FORMAT
customer_curated_df.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .parquet("s3://stedi-curated-data/customer_curated/")

print("🚀 Customer Curated Data Successfully Written!")
