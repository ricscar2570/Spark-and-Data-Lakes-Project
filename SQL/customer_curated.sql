CREATE EXTERNAL TABLE IF NOT EXISTS stedi.customer_curated (
    birthDay STRING,
    customerName STRING,
    email STRING,
    lastUpdateDate STRING, 
    phone STRING,
    registrationDate STRING, 
    serialNumber STRING,
    shareWithFriendsAsOfDate STRING,
    shareWithPublicAsOfDate STRING,
    shareWithResearchAsOfDate TIMESTAMP
)
STORED AS PARQUET
LOCATION 's3://stedi-curated-data/customer_curated/';
