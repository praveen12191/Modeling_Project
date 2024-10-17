import os
import re
import pandas as pd

folder_path = r'C:\Users\pr38\Desktop\fun'
output_file = r'C:\Users\pr38\Downloads\output.xlsx'

table_column_list = []

server_name = input("SERVER NAME: ")
database = input("DATABASE: ")
sf_schema_name = input("SF SCHEMA NAME: ")
sf_database = input("SF DATABASE: ")
load_type = input("LOAD TYPE: ")

# Loop through all SQL files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".sql"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r') as file:
            content = file.read()

        # Regex to find CREATE TABLE statements and extract columns
        create_statements = re.findall(r'CREATE TABLE\s+([^\s(]+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)

        # Process each table and its columns
        for table_name, columns in create_statements:
            columns = columns.strip().split('NULL,')
            for column in columns:
                try:
                    column_name = column.split()[0]
                except:
                    column_name = column.split()[0]

                if column_name.lower() == 'constraint':
                    break

                # Append data to list in a structured format
                table_column_list.append({
                    'SERVER': server_name,
                    'DATABASE': database,
                    'TABLE': table_name,
                    'COLUMN': column_name,
                    'SF_DB': sf_database,
                    'SF_SCHEMA': sf_schema_name,
                    'SF_TABLE': table_name,
                    'SF_COLUMN': column_name,
                    'LOAD_TYPE': load_type,
                    'VIEW': table_name
                })

# Create a DataFrame from the list
df = pd.DataFrame(table_column_list)

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False)

print(f"Data successfully written to {output_file}")
