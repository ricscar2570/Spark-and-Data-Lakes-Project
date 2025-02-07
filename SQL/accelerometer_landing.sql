CREATE EXTERNAL TABLE IF NOT EXISTS stedi.accelerometer_landing (
    timeStamp STRING,
    user STRING,
    x FLOAT,
    y FLOAT,
    z FLOAT
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('serialization.format' = '1')
LOCATION 's3://stedi-raw-data/accelerometer_landing/';
