import pyodbc
import re

with open(r"C:\\Users\\pr38\\Project\\Modeling_Project\\dumpp.txt", 'r') as file:
    content = file.read()


ddl_statements = content.split(';\n')

modified_statements = []
for statement in ddl_statements:
    statement = statement.strip()
    if statement.startswith("CREATE TABLE"):
        start = statement.find('(') + 1
        end = statement.rfind(')')
        match1 = re.search(r'CREATE TABLE\s+([^\s(]+)', statement)    
        table_name = match1.group(1)  
        view_statement = f"CREATE VIEW {table_name} AS SELECT "
        columns_part = statement[start:end].strip()
        column_definitions = columns_part.split(',\n')
        for column in column_definitions:
            k = column.strip()
            if k:
                if(k[0]=='"'):
                    column_name = '"'+k.split('"')[1]+'"'
                else:
                    column_name = k.split()[0]
                if column_name.upper() == "CONSTRAINT":
                    break
                view_statement += column_name + ","
        view_statement = view_statement.rstrip(',')
        view_statement += f" FROM {table_name};"
        with open(r"C:\\Users\\pr38\\Project\\Modeling_Project\\mainTable.txt", 'a') as output_file:
            output_file.write(view_statement + '\n')

      