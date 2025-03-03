import os
import re
import pandas as pd
from collections import defaultdict

def columnDeatils(server_name, database, sf_database, sf_schema_name, load_type, secure_view_db, secure_view_schema):
    file_path = r'C:\Users\pr38\Project\Modeling_Project\dumpp.txt'
    output_file = r'C:\Users\pr38\Project\Modeling_Project\scriptsoutput.xlsx'
    table_hash = defaultdict(list)
    

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    create_statements = re.findall(r'CREATE TABLE\s+([^\s(]+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
    count = 0
    for table_name, columns in create_statements:
        columns = columns.strip().split('NULL,')
        count2 = 0 
        for column_name in columns:
            column_name = column_name.split()[0]
            table_hash[count].append({
                'SERVER': server_name,
                'DATABASE': database,
                'SCHEMA': 'schema',
                'TABLE': 'table_name',
                'COLUMN': 'column',
                'SF_DB': sf_database,
                'SF_SCHEMA': sf_schema_name,
                'SF_TABLE': 'TBL_' + table_name,
                'SF_COLUMN': column_name,
                'LOAD_TYPE': load_type,
                'VIEW': table_name,
                'SECURE_VIEW_DB': secure_view_db,
                'SECURE_VIEW_SCHEMA': secure_view_schema
            })
            count2+=1
        count+=1
    file_path = r'C:\Users\pr38\Project\Modeling_Project\scripts\ddl.sql'
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    create_statements = re.findall(r'CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)

    count = 0

    for schema_name, table_name, columns in create_statements:
        column_matches = re.findall(r'\[(.*?)\]\s+\[.*?\]', columns)
        count2 = 0 
        for column_name in column_matches:
            table_hash[count][count2]['SCHEMA'] = schema_name
            table_hash[count][count2]['TABLE'] = table_name
            table_hash[count][count2]['COLUMN'] = column_name
            count2+=1
        count+=1

    columnDetails = []
    for i in table_hash.values():
        for j in i:
            columnDetails.append(j)
    df = pd.DataFrame(columnDetails)
    df.to_excel(output_file, index=False)
    print(f"Data successfully written to {output_file}")
