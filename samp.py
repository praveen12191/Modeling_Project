import pyodbc
import re


with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()


# content = re.sub(r'\bbit\b', 'boolean', content, flags=re.IGNORECASE)
# content = re.sub(r'\bnvarchar\b', 'varchar(50)', content, flags=re.IGNORECASE)

ddl_statements = content.split(';\n')

n = int(input("Enter the Type: "))
if n == 1:
    AUDIT = """
            AUDIT_CREATED_DATETIME TIMESTAMP_NTZ(9) NOT NULL,
            AUDIT_UPDATED_DATETIME TIMESTAMP_NTZ(9),
            AUDIT_CREATED_BY VARCHAR(50) NOT NULL,
	        AUDIT_UPDATED_BY VARCHAR(50),
            ETL_BATCH_ID NUMBER(38,0) NOT NULL,
            HASH_KEY NUMBER(38,0),
            """
else:
    AUDIT = """
            AUDIT_CREATED_DATETIME TIMESTAMP_NTZ(9) NOT NULL,
            AUDIT_CREATED_BY VARCHAR(50) NOT NULL,
            ETL_BATCH_ID NUMBER(38,0) NOT NULL,
            """

STG_AUDIT = """
            AUDIT_CREATED_DATETIME TIMESTAMP_NTZ(9) NOT NULL,
            AUDIT_CREATED_BY VARCHAR(50) NOT NULL,
            ETL_BATCH_ID NUMBER(38,0) NOT NULL);
            """

TYPE_2 = """
        ACTIVE_FLAG VARCHAR(1) NOT NULL,
        EFFECTIVE_START_DATE TIMESTAMP_NTZ(9) NOT NULL,
        EFFECTIVE_END_DATE TIMESTAMP_NTZ(9),
        """

modified_statements = []
for statement in ddl_statements:
    statement = statement.strip()
    statement2 = statement.strip()
    if statement.startswith("CREATE TABLE"):

        first_comma_pos = statement.find(',')
        statement = statement[:first_comma_pos + 1] + statement[first_comma_pos + 1:]
        match = re.search(r'CONSTRAINT\s+([^\s(]+)', statement, re.IGNORECASE)
        if match:
            insert_pos = match.start()
            statement = statement[:insert_pos].rstrip(',\n') + '\n' + AUDIT.strip() + '\n' + statement[insert_pos:]
            match1 = re.search(r'CREATE TABLE\s+([^\s(]+)', statement)
            if match1:
                table_name = match1.group(1)
                new_table_name = f"TBL_{table_name}"
                statement = statement.replace(table_name, new_table_name, 1)
                new_table_name = f"TBL_{table_name}"
                statement2 = statement2.replace(table_name, new_table_name, 1)
                closing_index = statement2.rfind('CONSTRAINT')
                insert_pos = match.start()
                statement2 = statement2[:closing_index-1] + STG_AUDIT
                with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'a') as output_file:
                    # output_file.write(statement+';'+ '\n')
                    output_file.write(statement2 + '\n')
                start = statement.find('(') + 1
                end = statement.rfind(')')
                tbl_name = table_name
                view_statement = f"CREATE VIEW {tbl_name} AS SELECT "
                columns_part = statement[start:end].strip()
                column_definitions = columns_part.split(',\n')
                for column in column_definitions:
                    k = column.strip()
                    if k:
                        column_name = k.split()[0]
                        if column_name.upper() == "CONSTRAINT":
                            break
                        view_statement += column_name + ","
                view_statement = view_statement.rstrip(',')
                view_statement += f" FROM TBL_{tbl_name};"
                
                # with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'a') as output_file:
                #     output_file.write(view_statement + '\n')

        else:
            match1 = re.search(r'CREATE TABLE\s+([^\s(]+)', statement)
            if match1:
                table_name = match1.group(1)
                new_table_name = f"TBL_{table_name}"
                statement = statement.replace(table_name, new_table_name, 1)
                statement = statement.rstrip(' \t\n\r);')
                statement += ',\n' + AUDIT.strip() + '\n'
                new_table_name = f"TBL_STG_{table_name}"
                statement2 = statement2.replace(table_name, new_table_name, 1)
                closing_index = statement2.rfind(');')
                statement2 = statement2[:closing_index - 1] + STG_AUDIT
                with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'a') as output_file:
                    output_file.write(statement + '\n')
                    output_file.write(statement2 + '\n')
        
                start = statement.find('(') + 1
                end = statement.rfind(')')
                tbl_name = table_name
                view_statement = f"CREATE VIEW {tbl_name} AS SELECT "
                columns_part = statement[start:end].strip()
                column_definitions = columns_part.split(',\n')
                for column in column_definitions:
                    k = column.strip()
                    if k:
                        column_name = k.split()[0]
                        if column_name.upper() == "CONSTRAINT":
                            break
                        view_statement += column_name + ","
                view_statement = view_statement.rstrip(',')
                view_statement += f" FROM TBL_{tbl_name};"
                with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'a') as output_file:
                    output_file.write(view_statement + '\n')
