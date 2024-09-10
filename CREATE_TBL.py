import pyodbc


conns = 'Driver={SQL Server};Server=CRSDWSQLUAT/;Database=CDF_MART;Trusted_Connection=yes'
conn = pyodbc.connect(conns)
cursor = conn.cursor()


def execute_sql(sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed SQL:--------------------------------------------------------------------------------------------------")
    except Exception as e:
        print(f"Error executing SQL:*******************************************************************************************{sql}\n{e}")



with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()
ddl_statements = content.split(';')
for statement in ddl_statements:
    statement = statement.strip()
    print(statement)
    # execute_sql(statement)
#     if statement.startswith("DROP TABLE DBO."):
#         with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'a') as output_file:
#             output_file.write(statement + ';\n')

for statement in ddl_statements:
    statement = statement.strip('\n')
    if statement.startswith("CREATE TABLE"):
        print(statement)

    # if statement.startswith("CREATE OR REPLACE VIEW"):
    #     with open(r"C:\\Users\\pr38\\Desktop\\sample.txt", 'w') as output_file:
    #         output_file.write(statement + ';')
    # if statement.startswith("ALTER"):
    #     execute_sql(statement)
    
    
cursor.close()
conn.close()
