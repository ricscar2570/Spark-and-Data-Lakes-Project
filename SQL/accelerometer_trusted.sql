CREATE EXTERNAL TABLE IF NOT EXISTS stedi.accelerometer_trusted (
    timeStamp TIMESTAMP,
    user STRING,
    x FLOAT,
    y FLOAT,
    z FLOAT
)
STORED AS PARQUET
LOCATION 's3://stedi-trusted-data/accelerometer_trusted/';
