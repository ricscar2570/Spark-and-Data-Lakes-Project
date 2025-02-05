CREATE EXTERNAL TABLE customer_landing ( serialnumber STRING, sharewithpublicasofdate STRING, birthday STRING, registrationdate STRING, sharewithresearchasofdate STRING, customername STRING, email STRING, lastupdatedate STRING, phone STRING, sharewithfriendsasofdate STRING
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION 's3://steady-raw-data/customer/'
TBLPROPERTIES ("classification"="json")
