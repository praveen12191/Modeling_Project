import os
import re

folder_path = r'C:\Users\pr38\Downloads\fun\fun'

output_file = r'C:\Users\pr38\Downloads\outp.txt'

table_column_list = []

for filename in os.listdir(folder_path):
    if filename.endswith(".sql"):
        file_path = os.path.join(folder_path, filename)
     
        with open(file_path, 'r') as file:
            content = file.read()
        
        # create_statements = re.findall(r'CREATE\s+VIEW\s+([^\s]+)\s+AS\s+SELECT\s+(.*?)\s+FROM\s+[^\s;]+', content, re.DOTALL | re.IGNORECASE)
        create_statements = re.findall(r'CREATE TABLE\s+([^\s(]+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
     
        for table_name, columns in create_statements:

            columns = columns.strip().split(',')
            for column in columns:
                try:
                    column_name = column.split()[0]
                except:
                    column_name = column.split()[0]
                if(column_name=='CONSTRAINT' or column_name=='constraint'):
                    break
                table_column_list.append(f'table:{table_name} column:{column_name}')


with open(output_file, 'w') as txt_file:
    for entry in table_column_list:
        txt_file.write(entry + '\n')

print(f"Text file created: {output_file}")
