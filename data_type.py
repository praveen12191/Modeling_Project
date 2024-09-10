import re

# Path to the file containing DDL statements
ddl_file_path = r'C:\Users\pr38\Downloads\fun\fun\SRVC_WH_STG.sql'  # Update this to your actual file path

# Read the content of the DDL file
with open(ddl_file_path, 'r') as file:
    ddl_content = file.read()

# Split DDL content by CREATE TABLE statements
ddl_statements = re.split(r'CREATE TABLE\b', ddl_content, flags=re.IGNORECASE)[1:]

# Prepare a dictionary to store table names and their data types
table_data_types = {}

# Process each DDL statement
for ddl in ddl_statements:
    # Extract the table name
    table_name_match = re.search(r'^\s*([\w\.]+)', ddl)
    if table_name_match:
        table_name = table_name_match.group(1).strip()
        table_data_types[table_name] = []

        # Extract column definitions with their data types
        column_definitions = re.findall(r'\b([\w_]+)\s+([a-zA-Z_]+(?:\(\d+(?:,\s*\d+)?\))?)', ddl)

        # Collect data types for the table
        for _, data_type in column_definitions:
            table_data_types[table_name].append(data_type)

# Output the data types for each table
for table, data_types in table_data_types.items():
    print(f"Table: {table}")
    for dtype in data_types:
        if(dtype=='NULL'):
            continue
        print(dtype)
    print("\n")
