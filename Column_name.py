import os
import re
import pandas as pd

folder_path = r'C:\Users\pr38\\Project\\Modeling_Project\\scripts'
output_file = r'C:\Users\pr38\Downloads\output.xlsx'

table_column_list = []

server_name = input("SERVER NAME: ")
database = input("DATABASE: ")
schema = input("SCHEMA: ")
sf_schema_name = input("SF SCHEMA NAME: ")
sf_database = input("SF DATABASE: ")
load_type = input("LOAD TYPE: ")

for filename in os.listdir(folder_path):
    if filename.endswith(".sql"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r') as file:
            content = file.read()

        create_statements = re.findall(r'CREATE TABLE\s+([^\s(]+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)

    
        for table_name, columns in create_statements:
            columns = columns.strip().split('NULL,')
            for column in columns:
                try:
                    column_name = column.split()[0]
                except:
                    column_name = column.split()[0]

                if column_name.lower() == 'constraint':
                    break

            
                table_column_list.append({
                    'SERVER': server_name,
                    'DATABASE': database,
                    'SCHEMA' : schema,
                    'TABLE': table_name,
                    'COLUMN': column_name,
                    'SF_DB': sf_database,
                    'SF_SCHEMA': sf_schema_name,
                    'SF_TABLE': 'TBL_'+table_name,
                    'SF_COLUMN': column_name,
                    'LOAD_TYPE': load_type,
                    'VIEW': table_name
                })


df = pd.DataFrame(table_column_list)

df.to_excel(output_file, index=False)

print(f"Data successfully written to {output_file}")
