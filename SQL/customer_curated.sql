CREATE EXTERNAL TABLE IF NOT EXISTS stedi.customer_curated (
    serialnumber STRING,
    birthday STRING,
    registrationdate STRING,
    sharewithresearchasofdate STRING,
    lastupdatedate STRING,
    sharewithfriendsasofdate STRING
)
STORED AS PARQUET
LOCATION 's3://stedi-curated-data/customer_curated/';
