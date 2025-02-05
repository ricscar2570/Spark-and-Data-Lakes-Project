CREATE EXTERNAL TABLE IF NOT EXISTS stedi.customer_trusted (
    serialnumber STRING,
    sharewithpublicasofdate STRING,
    birthday STRING,
    registrationdate STRING,
    sharewithresearchasofdate STRING,
    customername STRING,
    lastupdatedate STRING,
    sharewithfriendsasofdate STRING
)
STORED AS PARQUET
LOCATION 's3://stedi-trusted-data/customer_trusted/';
