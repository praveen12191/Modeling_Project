import re

ddl_file_path = r'C:\Users\pr38\Downloads\fun\fun\SRVC_WH_STG.sql' 

with open(ddl_file_path, 'r') as file:
    ddl_content = file.read()


ddl_statements = re.split(r'CREATE TABLE\b', ddl_content, flags=re.IGNORECASE)[1:]


table_data_types = {}

for ddl in ddl_statements:

    table_name_match = re.search(r'^\s*([\w\.]+)', ddl)
    if table_name_match:
        table_name = table_name_match.group(1).strip()
        table_data_types[table_name] = []

        column_definitions = re.findall(r'\b([\w_]+)\s+([a-zA-Z_]+(?:\(\d+(?:,\s*\d+)?\))?)', ddl)

    
        for _, data_type in column_definitions:
            table_data_types[table_name].append(data_type)

for table, data_types in table_data_types.items():
    print(f"Table: {table}")
    for dtype in data_types:
        if(dtype=='NULL'):
            continue
        print(dtype)
    print("\n")
