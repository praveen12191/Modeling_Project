
// this are stg_file_format objects
CREATE OR REPLACE TABLE  ORDERS (
    ORDER_ID VARCHAR(30),
    AMOUNT VARCHAR(30),
    PROFIT INT,
    QUANTITY INT,
    CATEGORY VARCHAR(30),
    SUBCATEGORY VARCHAR(30));

// Prepare stage object
CREATE OR REPLACE STAGE aws_stage_copy
    url='s3://snowflakebucket-copyoption/size/';
  
LIST @aws_stage_copy;

desc stage aws_stage_copy;
  
    
 //Load data using copy command no data will be loaded in validation mode
COPY INTO ORDERS
    FROM @aws_stage_copy
    file_format= (type = csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
    VALIDATION_MODE = RETURN_ERRORS;
    
SELECT * FROM ORDERS;    
    
COPY INTO ORDERS
    FROM @aws_stage_copy
    file_format= (type = csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
   VALIDATION_MODE = RETURN_5_ROWS ;



--- Use files with errors ---

create or replace stage aws_stage_copy
    url ='s3://snowflakebucket-copyoption/returnfailed/';
    
list  @aws_stage_copy;

-- show all errors --
copy into orders
    from  @aws_stage_copy
    file_format = (type=csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
    validation_mode=return_errors;

-- validate first n rows --
copy into orders
    from  aws_stage_copy
    file_format = (type=csv field_delimiter=',' skip_header=1)
    pattern='.*error.*'
    validation_mode=return_1_rows;
    

    


    copy into orders
    from  @aws_stage_copy
    file_format = (type=csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
    validation_mode=return_errors;

// after run this code i can get the quert id else we can get via 

select * from table(result_scan(LAST_QUERY_ID()));


//HANDLING REJECTED RECOREDS 

CREATE OR REPLACE TABLE REJECTED AS
SELECT REJECTED_RECORD FROM table(result_scan('01b9ad39-0003-cae7-0002-712e03e829b6'));



SELECT * FROM REJECTED;


//if the record is rejected we need to process the record 


SELECT REJECTED_RECORD FROM rejected;

CREATE OR REPLACE TABLE rejected_values as
SELECT 
SPLIT_PART(rejected_record,',',1) as ORDER_ID, 
SPLIT_PART(rejected_record,',',2) as AMOUNT, 
SPLIT_PART(rejected_record,',',3) as PROFIT, 
SPLIT_PART(rejected_record,',',4) as QUATNTITY, 
SPLIT_PART(rejected_record,',',5) as CATEGORY, 
SPLIT_PART(rejected_record,',',6) as SUBCATEGORY
FROM rejected; 


SELECT * FROM rejected_values;


//also we have SIZE_LIMIT AND WE HAVE RETURN_FAILED_ONLY = TRUE/FALSE 




copy into orders
    from  @aws_stage_copy
    file_format = (type=csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
    ON_ERROR = CONTINUE
    RETURN_FAILED_ONLY = TRUE;

// WE CAN EASYLY FIND THE FILES WHICH ARE ERROR AND WE CAN LOOK ON IT


//TRUNCATECOLUMNS if we have column with data type varchar(10) if the data is grater than 10 it will truncat the data to length 10 


copy into orders
    from  @aws_stage_copy
    file_format = (type=csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*'
    truncatecolumns = true; 
