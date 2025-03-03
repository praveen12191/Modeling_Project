create or replace table sales_raw_staging(
  id varchar,
  product varchar,
  price varchar,
  amount varchar,
  store_id varchar);
  

create or replace stream sales_stream on table sales_raw_staging;

-- insert values 
insert into sales_raw_staging 
    values
        (1,'Banana',1.99,1,1),
        (2,'Lemon',0.99,1,1),
        (3,'Apple',1.79,1,2),
        (4,'Orange Juice',1.89,1,2),
        (5,'Cereals',5.98,2,1);  


SELECT * FROM sales_raw_staging;

select * from sales_stream;

SELECT * FROM sales_final_table;
delete from sales_raw_staging
where id = 1;


CREATE TASK all_data_changes
WAREHOUSE = MRCSBWH
SCHEDULE = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('SALES_STREAM');


merge into sales_final_table s 
using sales_stream sa
on s.id = sa.id
when NOT matched and sa.metadata$action = 'INSERT'
THEN INSERT 
(id,product,price,store_id,amount)
VALUES (sa.id,sa.product,sa.price,sa.store_id,sa.amount);



