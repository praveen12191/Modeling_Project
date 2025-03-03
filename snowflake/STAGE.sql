CREATE OR REPLACE SCHEMA EXTERNAL_STAGE;


//creating the external stage


//'s3://bucketsnowflakes3'

CREATE OR REPLACE STAGE AWS_STAGE
URL = 's3://bucketsnowflakes3';


LIST @AWS_STAGE;




CREATE OR REPLACE STAGE AWS_STAGE_ASS
URL = 's3://snowflake-assignments-mc/';

desc STAGE AWS_STAGE;

LIST @AWS_STAGE;

LIST @AWS_STAGE_ASS;


// CREATING THE FILE FORMAT 
CREATE OR REPLACE FILE FORMAT CSV_STAGE_FILE_CHECK
TYPE = 'CSV'
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"';

DESC FILE FORMAT CSV_STAGE_FILE_CHECK;

// TYPE CAN'T BE CHNAGED 

ALTER FILE FORMAT CSV_STAGE_FILE_CHECK
SET TYPE='JSON';

SELECT $1 AS column1, $2 AS column2, $3 AS column3
FROM @AWS_STAGE/Loan_payments_data.csv
(FILE_FORMAT => CSV_STAGE_FILE_CHECK)
LIMIT 10;


CREATE or replace TABLE SAMPLES
(
ID INT,

first_name varchar,

last_name varchar,

email varchar,

age int,

city varchar);


COPY INTO SAMPLES
FROM @AWS_STAGE_ASS/loadingdata
FILE_FORMAT = (type=CSV field_delimiter = ';' skip_header=1)
pattern ='.*customer.*';


SELECT * FROM SAMPLES;

// coping specific column from external stage
COPY INTO SAMPLES (ID,email)
FROM ( SELECT $1 , $4  FROM @AWS_STAGE_ASS/loadingdata)
FILE_FORMAT = (type=CSV field_delimiter = ';' skip_header=1)
pattern ='.*customer.*';


// ON_ERROR if we have some error in file in age field we have name etc 

COPY INTO SAMPLES (ID,email)
FROM ( SELECT $1 , $4  FROM @AWS_STAGE_ASS/loadingdata)
FILE_FORMAT = (type=CSV field_delimiter = ';' skip_header=1)
pattern ='.*customer.*'
on_error = 'ABORT_STATEMENT';//THIS IS DEFAULT
//WE have SKIP_FILE  and CONTINUE -> which is not load the error data 
// in SKIP_FILE we can give the limit SKIP_FILE_2


//VALIDATION_MODE 



