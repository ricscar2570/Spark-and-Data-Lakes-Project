CREATE EXTERNAL TABLE IF NOT EXISTS stedi.step_trainer_trusted (
    sensorReadingTime TIMESTAMP,
    serialNumber STRING,
    distanceFromObject FLOAT
)
STORED AS PARQUET
LOCATION 's3://stedi-trusted-data/step_trainer_trusted/';
