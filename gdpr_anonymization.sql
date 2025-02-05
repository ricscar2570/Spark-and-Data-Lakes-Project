CREATE TABLE stedi.customer_anonymized AS 
SELECT 
    serialnumber, 
    birthday, 
    registrationdate, 
    sharewithresearchasofdate, 
    lastupdatedate, 
    sharewithfriendsasofdate 
FROM stedi.customer_curated;
