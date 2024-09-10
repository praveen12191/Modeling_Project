import pyodbc,re


conns = 'Driver={SQL Server};Server=CRSDWSQLDEV02\SDW_DEV;Database=CDF_MART;Trusted_Connection=yes'
conn = pyodbc.connect(conns)
cursor = conn.cursor()



def find_tbl_name(ind,statement):
    tbl_name = ""
    for i in statement:
        if(i in "._"):
            return tbl_name[::-1]
        tbl_name+=i 


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
    start = statement.find('(') + 1
    end = statement.rfind(')')
    tbl_name = find_tbl_name(start,statement[:start-1][::-1])
    view_statement = "CREATE VIEW {} AS SELECT ".format(tbl_name)
    columns_part = statement[start:end].strip()
    column_definitions = columns_part.split(',\n')
    lis = []
    for column in column_definitions:
        k = column.strip()
        try:
            column_name = k.split()[0]
            lis.append(column_name)
            if(column_name.upper()=="CONSTRAINT"):
                break 
        except:
            pass
        
        view_statement+= column_name+","
    view_statement = view_statement.rstrip(',')
    view_statement += f" FROM {tbl_name};"




