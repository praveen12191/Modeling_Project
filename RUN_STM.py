import pyodbc


environments = {
    "QA": 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_QA;Database=CDF_MART;Trusted_Connection=yes',
    "DEV": 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_DEV;Database=CDF_MART;Trusted_Connection=yes',
    "UAT": 'Driver={SQL Server};Server=CRSDWSQLUAT;Database=CDF_MART;Trusted_Connection=yes'
}

def execute_sql(cursor, conn, sql):
    try:
        cursor.execute(sql)
        conn.commit()
        print(f"Executed SQL:----------------------------------------------------------------------------")
    except Exception as e:
        print(f"Error executing SQL: ***************************************************************************{sql}")

with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()

ddl_statements = content.split(';')


for env_name, conns in environments.items():
    print(f"Connecting to {env_name} environment...")
    try:
        conn = pyodbc.connect(conns)
        cursor = conn.cursor()
        
        for statement in ddl_statements:
            statement = statement.strip()
            execute_sql(cursor,conn,statement)
           
        cursor.close()
        conn.close()
        print(f"Finished executing statements in {env_name} environment.\n")

    except Exception as e:
        print(f"Failed to connect to {env_name} environment: {e}")
