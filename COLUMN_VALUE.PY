import os
import re
import pandas as pd

def columnDeatils(server_name, database, schema, sf_database, sf_schema_name, load_type, secure_view_db, secure_view_schema):
    folder_path = r'C:\Users\pr38\Project\Modeling_Project\scripts'
    output_file = r'C:\Users\pr38\Project\Modeling_Project\scriptsoutput.xlsx'
    table_column_list = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".sql"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            create_statements = re.findall(r'CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
            
            for schema_name, table_name, columns in create_statements:
                column_matches = re.findall(r'\[(.*?)\]\s+\[.*?\]', columns)
                
                for column_name in column_matches:
                    table_column_list.append({
                        'SERVER': server_name,
                        'DATABASE': database,
                        'SCHEMA': schema_name,
                        'TABLE': table_name,
                        'COLUMN': column_name,
                        'SF_DB': sf_database,
                        'SF_SCHEMA': sf_schema_name,
                        'SF_TABLE': 'TBL_' + table_name,
                        'SF_COLUMN': column_name,
                        'LOAD_TYPE': load_type,
                        'VIEW': table_name,
                        'SECURE_VIEW_DB': secure_view_db,
                        'SECURE_VIEW_SCHEMA': secure_view_schema
                    })
    
    df = pd.DataFrame(table_column_list)
    df.to_excel(output_file, index=False)
    print(f"Data successfully written to {output_file}")
