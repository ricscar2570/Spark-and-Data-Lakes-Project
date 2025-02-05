CREATE EXTERNAL TABLE step_trainer_landing ( sensorReadingTime STRING, serialNumber STRING, distanceFromObject FLOAT
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://stedi-raw-data/step_trainer/landing/'
TBLPROPERTIES ("classification"="json")
