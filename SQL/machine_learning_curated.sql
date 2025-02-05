CREATE EXTERNAL TABLE IF NOT EXISTS stedi.machine_learning_curated (
    sensorReadingTime TIMESTAMP,
    serialNumber STRING,
    distanceFromObject FLOAT,
    timeStamp TIMESTAMP,
    user STRING,
    x FLOAT,
    y FLOAT,
    z FLOAT
)
STORED AS PARQUET
LOCATION 's3://stedi-curated-data/machine_learning_curated/';
