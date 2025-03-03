import pyodbc
import re
from help import STG_AUDIT, TYPE_2, AUDIT_CONSTRAINT1, AUDIT_CONSTRAINT2, AUDIT1, AUDIT2
from Column_name import columnDeatils

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
def get_user_inputs():
    print("-----For Append and Truncate and load just type 3-------")
    n = int(input("Enter the Type: "))
    server_name = input("SERVER NAME: ")
    database = input("DATABASE: ")
    sf_database = input("SF DATABASE: ")
    sf_schema_name = input("SF SCHEMA NAME: ")
    load_type = input("LOAD TYPE: ")
    secure_view_db = input("SECURE_DB: ")
    secure_view_schema = input("SECURE_SCHEMA: ")
    return n, server_name, database, sf_database, sf_schema_name, load_type, secure_view_db, secure_view_schema

def process_statements(ddl_statements, n, sf_database, sf_schema_name, secure_view_db, secure_view_schema):
    modified_statements = []
    for statement in ddl_statements:
        statement = statement.strip()
        statement2 = statement.strip()
        if statement.startswith("CREATE TABLE"):
            flag = 0
            first_comma_pos = statement.find('NULL,')
            if n == 2:
                statement = statement[:first_comma_pos + 5] + TYPE_2 + statement[first_comma_pos + 5:]
            match = re.search(r'CONSTRAINT\s+([^\s(]+)', statement, re.IGNORECASE)
            if not match:
                flag = 1
                match = re.search(r'PRIMARY\s+([^\s(]+)', statement, re.IGNORECASE)
            if match:
                if n == 1 or n == 2:
                    AUDIT = AUDIT_CONSTRAINT1
                else:
                    AUDIT = AUDIT_CONSTRAINT2
                insert_pos = match.start()
                statement = statement[:insert_pos].rstrip('\n') + AUDIT + statement[insert_pos:]
                match1 = re.search(r'CREATE TABLE\s+([^\s(]+)', statement)
                if match1:
                    table_name = match1.group(1)
                    new_table_name = f"{sf_database}.{sf_schema_name}.TBL_{table_name}"
                    new_stg_table_name = f"{sf_database}.STG_{sf_schema_name}.TBL_{table_name}"
                    statement2 = statement2.replace(table_name, new_stg_table_name, 1)
                    statement = statement.replace(table_name, new_table_name, 1)
                    closing_index = statement.rfind('CONSTRAINT')
                    if flag:
                        closing_index = statement.rfind('PRIMARY')
                        stm = f"CONSTRAINT PK_{table_name} "
                        statement = statement[0:closing_index] + stm + statement[closing_index:]
                    if flag:
                        closing_index = statement2.rfind('PRIMARY')
                    else:
                        closing_index = statement2.rfind('CONSTRAINT')

                    statement2 = statement2[:closing_index] + STG_AUDIT
                    write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\mainTable.txt", statement + ';\n')
                    write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\stgTable.txt", statement2 + '\n')

                    create_view_statements(sf_database, sf_schema_name, secure_view_db, secure_view_schema, table_name, statement)
            else:
                process_without_constraint(statement, statement2, n, sf_database, sf_schema_name, secure_view_db, secure_view_schema)
    return modified_statements

def process_without_constraint(statement, statement2, n, sf_database, sf_schema_name, secure_view_db, secure_view_schema):
    match1 = re.search(r'CREATE TABLE\s+([^\s(]+)', statement)
    if match1:
        table_name = match1.group(1)
        new_table_name = f"{sf_database}.{sf_schema_name}.TBL_{table_name}"
        new_stg_table_name = f"{sf_database}.STG_{sf_schema_name}.TBL_{table_name}"
        statement = statement.replace(table_name, new_table_name, 1)
        statement = statement.rstrip(' \t\n\r);')
        if n == 1 or n == 2:
            AUDIT = AUDIT1
        else:
            AUDIT = AUDIT2
        statement2 = statement[:]
        statement += ',\n' + AUDIT.strip() + '\n'
        statement2 += ',\n' + STG_AUDIT.strip() + '\n'
        statement2 = statement2.replace(new_table_name, new_stg_table_name, 1)

        write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\mainTable.txt", statement + '\n')
        write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\stgTable.txt", statement2 + '\n')

        create_view_statements(sf_database, sf_schema_name, secure_view_db, secure_view_schema, table_name, statement)

def create_view_statements(sf_database, sf_schema_name, secure_view_db, secure_view_schema, table_name, statement):
    start = statement.find('(') + 1
    end = statement.rfind(')')
    tbl_name = table_name
    view_statement = f"CREATE VIEW {sf_database}.{sf_schema_name}.{tbl_name} AS SELECT "
    secure_view_statement = f"CREATE SECURE VIEW {secure_view_db}.{secure_view_schema}.{tbl_name} AS SELECT "
    columns_part = statement[start:end].strip()
    column_definitions = columns_part.split(',\n')
    for column in column_definitions:
        k = column.strip()
        if k:
            if k[0] == '"':
                column_name = '"' + k.split('"')[1] + '"'
            else:
                column_name = k.split()[0]
            if column_name.upper() == "CONSTRAINT":
                break
            view_statement += column_name + ","
            secure_view_statement += column_name + ","
    view_statement = view_statement.rstrip(',')
    secure_view_statement = secure_view_statement.rstrip(',')
    view_statement += f" FROM {sf_database}.{sf_schema_name}.TBL_{tbl_name};"
    secure_view_statement += f" FROM {sf_database}.{sf_schema_name}.TBL_{tbl_name};"
    write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\mainTable.txt", view_statement + '\n')
    write_to_file(r"C:\\Users\\pr38\\Project\\Modeling_Project\\DDL\\mainTable.txt", secure_view_statement + '\n')

def write_to_file(file_path, content):
    with open(file_path, 'a') as output_file:
        output_file.write(content)

def main():
    file_path = r"C:\\Users\\pr38\\Project\\Modeling_Project\\dumpp.txt"
    content = read_file(file_path)
    # content = re.sub(r'\bmoney\b', 'DECIMAL(18,4)', content, flags=re.IGNORECASE)
    # content = re.sub(r'\bbit\b', 'INT', content, flags=re.IGNORECASE)
    # content = re.sub(r'\bnvarchar\b', 'VARCHAR', content, flags=re.IGNORECASE)
    ddl_statements = content.split(';\n')
    
    n, server_name, database, sf_database, sf_schema_name, load_type, secure_view_db, secure_view_schema = get_user_inputs()
    
    columnDeatils(server_name, database, sf_database, sf_schema_name, load_type, secure_view_db, secure_view_schema)
    
    process_statements(ddl_statements, n, sf_database, sf_schema_name, secure_view_db, secure_view_schema)


main()