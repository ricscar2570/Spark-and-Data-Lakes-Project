CREATE TABLE stedi.accelerometer_filtered AS 
SELECT 
    a.* 
FROM stedi.accelerometer_trusted a
JOIN stedi.customer_trusted c 
ON a.user = c.serialnumber
WHERE a.timeStamp >= c.sharewithresearchasofdate;