// First step: Load Raw JSON

CREATE OR REPLACE stage JSONSTAGE
     url='s3://bucketsnowflake-jsondemo';
CREATE OR REPLACE stage JSONSTAGE_ASS
     url='s3://snowflake-assignments-mc/unstructureddata';


LIST @JSONSTAGE;
LIST @JSONSTAGE_ASS;
CREATE OR REPLACE file format JSONFORMAT
    TYPE = JSON;
    
    
CREATE OR REPLACE table JSON_RAW (
    raw_file variant);
    
COPY INTO JSON_RAW
    FROM @JSONSTAGE
    file_format= JSONFORMAT
    files = ('HR_data.json');
    


   
SELECT * FROM JSON_RAW;


SELECT RAW_FILE:city FROM JSON_RAW;

//CHANGE THE DATA TYPE
SELECT RAW_FILE:city::STRING FROM JSON_RAW;

// HANDELING THE NESTED DATA
SELECT RAW_FILE:job:salary as SALARY, RAW_FILE:job:title AS TITLE FROM JSON_RAW;

SELECT RAW_FILE:prev_company[0] FROM JSON_RAW;


/*{"spoken_languages":[{"language":"Haitian Creole","level":"Advanced"},{"language":"Quechua","level":"Basic"},{"language":"Thai","level":"Expert"}]}

i need the data like 

language level 

i can do like 

SELECT RAW_FILE:spoken_languages[0].language,spoken_languages[0].level FROM JSON_RAW;
union all 
SELECT RAW_FILE:spoken_languages[1].language,spoken_languages[1].level FROM JSON_RAW;

it is not a correct way

*/

// FLATTEN 


CREATE TABLE LANGUAGES AS 
SELECT RAW_FILE:first_name as FIRST_NAME,
        f.value:language::string as LANGUAGE,
        f.value:level::string as LEVEL

FROM JSON_RAW , TABLE(FLATTEN(RAW_FILE:spoken_languages)) f ;


SELECT * FROM LANGUAGES;


SELECT CURRENT_TIMESTAMP;
