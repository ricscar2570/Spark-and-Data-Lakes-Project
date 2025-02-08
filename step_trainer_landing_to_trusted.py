from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ✅ Initialize Spark Session
spark = SparkSession.builder \
    .appName("StepTrainerTrusted") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# ✅ Load Step Trainer Landing Data
step_trainer_landing_df = spark.read \
    .option("inferSchema", "true") \
    .json("s3://stedi-raw-data/step_trainer/landing/")

# ✅ Load Customer Curated Data (Selecting Only `serialNumber`)
customer_curated_df = spark.read \
    .parquet("s3://stedi-curated-data/customer_curated/") \
    .select("serialNumber")

# ✅ Ensure Correct Data Types
step_trainer_landing_df = step_trainer_landing_df.withColumn("sensorReadingTime", col("sensorReadingTime").cast("timestamp"))

# 🚀 Debugging: Print Initial Row Counts and Schema
print(f"✅ Total Step Trainer Readings in Landing: {step_trainer_landing_df.count()}")
print(f"✅ Customers in Curated Zone: {customer_curated_df.count()}")

print("📌 Step Trainer Landing Schema:")
step_trainer_landing_df.printSchema()

print("📌 Customer Curated Schema:")
customer_curated_df.printSchema()

# ✅ Perform the Join (Fix Duplicate Column Issue)
step_trainer_trusted_df = step_trainer_landing_df.alias("s").join(
    customer_curated_df.alias("c"),
    col("s.serialNumber") == col("c.serialNumber"),
    "inner"
).select("s.*")  # ✅ Keep Only Step Trainer Columns

# 🚀 Debugging: Print Final Row Count After Join
print(f"✅ Step Trainer Readings AFTER Join with Customers: {step_trainer_trusted_df.count()}")

# ✅ Enable schema evolution in Glue Data Catalog
step_trainer_trusted_df.write \
    .mode("overwrite") \
    .format("parquet") \
    .option("path", "s3://stedi-trusted-data/step_trainer_trusted/") \
    .option("mergeSchema", "true") \
    .saveAsTable("stedi.step_trainer_trusted")

print("🚀 Step Trainer Trusted Data Successfully Written!")

# ✅ Stop Spark Session
spark.stop()
