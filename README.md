# **STEDI Human Balance Analytics – README.md** 🚀  

## **📌 Introduction**  
STEDI is developing a **human balance training platform** using **IoT sensors and Machine Learning**.  
This project aims to collect, transform, and analyze data from the **STEDI Step Trainer**, a device that monitors user movements.  

This **AWS-based ETL pipeline** allows STEDI to:  
✅ **Extract** IoT sensor data and store it in an **AWS S3 Data Lake**.  
✅ **Transform** and clean the data using **AWS Glue**.  
✅ **Load** the data into a **Curated Zone optimized for Machine Learning**.  
✅ **Analyze the data** using AWS Athena to detect patterns in balance training.  

📌 **Technologies used:**  
🔹 AWS Glue (ETL)  
🔹 AWS S3 (Data Lake)  
🔹 AWS Athena (Query engine)  
🔹 AWS IAM (Security)  
🔹 Apache Spark (Big Data processing)  

---

## **📌 Data Lakehouse Architecture**
The project follows a **Lakehouse Architecture**, combining the flexibility of a **Data Lake** with the performance of a **Data Warehouse**.

📍 **Pipeline Stages:**
1. **Landing Zone** 🏗️ – Raw IoT data ingestion.  
2. **Trusted Zone** 🔎 – Filtered and validated data.  
3. **Curated Zone** 📊 – Optimized data ready for Machine Learning.  

---

## **📌 Database Schema**
The dataset consists of three main tables, structured into different **processing zones**:

### **1️⃣ Landing Zone (Raw Data)**
This data is **ingested from IoT devices** and stored in JSON format on S3.  
| Table | Description |
|---------|------------|
| `customer_landing` | User data (registration, permissions, contact details) |
| `accelerometer_landing` | Mobile app sensor data (X, Y, Z) |
| `step_trainer_landing` | Step Trainer device movement data |

---

### **2️⃣ Trusted Zone (Filtered Data)**
Data is **cleaned and filtered**, keeping only users who have **agreed to share their data for research**.  
| Table | Description |
|---------|------------|
| `customer_trusted` | Users with research consent |
| `accelerometer_trusted` | Sensor data from authorized users |
| `step_trainer_trusted` | Validated Step Trainer data |

---

### **3️⃣ Curated Zone (Optimized for ML)**
Data is **aggregated and prepared** for advanced analytics.  
| Table | Description |
|---------|------------|
| `customer_curated` | Only users with accelerometer data |
| `machine_learning_curated` | Merged Step Trainer and Accelerometer data for ML |

---

## **📌 ETL Pipeline**
📌 **AWS Glue ETL Process Steps:**

1️⃣ **Extract (Landing Zone)**
   - Data is ingested from **IoT devices** and stored in **S3 as JSON**.  
   - AWS Glue **crawlers create Athena tables** from raw files.  

2️⃣ **Transform (Trusted Zone)**
   - **Filtering**: Keep only users who have research consent.  
   - **Joining**: Link users with their sensor data.  

3️⃣ **Load (Curated Zone)**
   - **Merge** Step Trainer & Accelerometer data.  
   - **Convert to Parquet** for optimized analytics.  

---

## **📌 Repository Structure**
📂 `stedi_project/`  
├── 📜 `README.md` (This file 📄)  
├── 📂 `sql/` (SQL scripts for Athena tables)  
│   ├── `customer_landing.sql`  
│   ├── `accelerometer_landing.sql`  
│   ├── `step_trainer_landing.sql`  
│   ├── `customer_trusted.sql`  
│   ├── `machine_learning_curated.sql`  
│   └── `customer_curated.sql`  
├── 📂 `glue_jobs/` (AWS Glue ETL scripts)  
│   ├── `customer_landing_to_trusted.py`  
│   ├── `accelerometer_landing_to_trusted.py`  
│   ├── `step_trainer_landing_to_trusted.py`  
│   ├── `customer_trusted_to_curated.py`  
│   ├── `machine_learning_curated.py`  
│   └── `glue_helpers.py` (Helper functions)  
├── 📂 `screenshots/` (AWS Athena query results)  
│   ├── `customer_landing.png`  
│   ├── `customer_trusted.png`  
│   ├── `customer_curated.png`  
│   ├── `machine_learning_curated.png`  
│   └── `glue_jobs_execution.png`  
└── 📜 `report_stedi_project.pdf` (Final report 📊)  

---

## **📌 How to Run the Project**
### **🔹 1️⃣ AWS Setup**
1. **Upload raw data to S3**:  
   - `customer_landing/`  
   - `accelerometer_landing/`  
   - `step_trainer_landing/`  

2. **Create Athena tables** using SQL scripts.

3. **Configure AWS Glue**:
   - **Create IAM Role** (`AWSGlueServiceRole-STEDI`) with S3 & Glue permissions.
   - **Set up AWS Glue Crawlers**.
   - **Create and run AWS Glue Jobs**.

4. **Validate data in Athena** using SQL queries.

---

## **📌 Example AWS Athena Queries**
### 🔹 **1️⃣ Top Users with the Most Accelerometer Readings**
```sql
SELECT user, COUNT(*) AS num_readings
FROM stedi.machine_learning_curated
GROUP BY user
ORDER BY num_readings DESC
LIMIT 10;

📌 Insight: Identifies users with the highest activity levels.
🔹 2️⃣ Average Distance Measured by the Step Trainer

SELECT AVG(distanceFromObject) AS avg_distance
FROM stedi.machine_learning_curated;

📌 Insight: Helps analyze balance stability across users.
🔹 3️⃣ Users with the Most Extreme Acceleration Changes

SELECT user, MAX(x) - MIN(x) AS variation_x, 
              MAX(y) - MIN(y) AS variation_y, 
              MAX(z) - MIN(z) AS variation_z
FROM stedi.machine_learning_curated
GROUP BY user
ORDER BY variation_x DESC
LIMIT 5;

📌 Insight: Detects users with the highest movement variability.
