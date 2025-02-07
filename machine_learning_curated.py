from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# ✅ Initialize Spark Session
spark = SparkSession.builder.appName("MachineLearningCurated").getOrCreate()

# ✅ Load Step Trainer Trusted Data
step_trainer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/step_trainer_trusted/")

# ✅ Load Accelerometer Trusted Data
accelerometer_trusted_df = spark.read.parquet("s3://stedi-trusted-data/accelerometer_trusted/")

# 🚀 Debugging: Print Initial Row Counts and Schema
print(f"✅ Total Step Trainer Trusted Rows: {step_trainer_trusted_df.count()}")
print(f"✅ Total Accelerometer Trusted Rows: {accelerometer_trusted_df.count()}")

print("📌 Step Trainer Trusted Schema:")
step_trainer_trusted_df.printSchema()

print("📌 Accelerometer Trusted Schema:")
accelerometer_trusted_df.printSchema()

# ✅ Ensure Correct Data Types
step_trainer_trusted_df = step_trainer_trusted_df.withColumn("sensorReadingTime", col("sensorReadingTime").cast("timestamp"))
accelerometer_trusted_df = accelerometer_trusted_df.withColumn("timeStamp", col("timeStamp").cast("timestamp"))

# 🚀 Verify Min/Max Timestamps Before Joining
print("📊 Min/Max Timestamps in Step Trainer Trusted:")
step_trainer_trusted_df.selectExpr("MIN(sensorReadingTime)", "MAX(sensorReadingTime)").show()

print("📊 Min/Max Timestamps in Accelerometer Trusted:")
accelerometer_trusted_df.selectExpr("MIN(timeStamp)", "MAX(timeStamp)").show()

# ✅ Perform the INNER JOIN on Sensor Reading Time
machine_learning_curated_df = step_trainer_trusted_df.alias("s").join(
    accelerometer_trusted_df.alias("a"),
    col("s.sensorReadingTime") == col("a.timeStamp"),
    "inner"
).select(
    col("s.sensorReadingTime"),
    col("s.serialNumber"),
    col("s.distanceFromObject"),
    col("a.x"),
    col("a.y"),
    col("a.z")
)  # ✅ Selecting Only Relevant Fields

# 🚀 Debugging: Print Final Row Count After Join
print(f"✅ Machine Learning Curated Rows: {machine_learning_curated_df.count()}")

# ✅ Save to Curated Zone
machine_learning_curated_df.write.mode("overwrite").parquet("s3://stedi-curated-data/machine_learning_curated/")

print("🚀 Machine Learning Curated Data Successfully Written!")
