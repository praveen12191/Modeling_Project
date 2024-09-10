import pandas as pd
import re



def getDataType(table):

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

    dlist = []
    for tablename, data_types in table_data_types.items():
        if(tablename==table):
            for dtype in data_types:
                if(dtype=='NULL'):
                    continue
                dlist.append(dtype)
    return dlist

def getViewName(table):
    file_path = r'C:\Users\pr38\Downloads\fun\fun\SRVC_WH_STG2.sql'
    with open(file_path, 'r') as file:
        content = file.read()
        
    create_statements = re.findall(r'CREATE\s+VIEW\s+([^\s]+)\s+AS\s+SELECT\s+(.*?)\s+FROM\s+[^\s;]+', content, re.DOTALL | re.IGNORECASE)
    #create_statements = re.findall(r'CREATE VIEW\s+([^\s(]+)\s*\((.*?)\);', content, re.DOTALL | re.IGNORECASE)
    
    for table_name, columns in create_statements:
        if(table_name==table):
            table_column_list = []
            columns = columns.strip().split(',')
            for column in columns:
                try:
                    column_name = column.split()[2]
                except:
                    column_name = column.split()[0]
                table_column_list.append(column_name)
            return table_column_list
    else:
        return 'non'
def GetDescription(df, table_name, column_names, file_name):
    results = []
    stm = f"CREATE VIEW {table_name} AS SELECT "
    type2 = "ACTIVE_FLAG,\nEFFECTIVE_START_DATE,\nEFFECTIVE_END_DATE\n"
    type2Audit = "AUDIT_CREATED_DATE,\nAUDIT_UPDATED_DATE,\nETL_BATCH_ID,\nHASH_KEY\n"
    columnCount = 0 
    count = 0
    viewName = getViewName(table_name)
    datatypelist = getDataType(table_name)
    for column_name in column_names:
        columnCount += 1
        data_type = ''
        filtered_df = df[(df['TABLE_NAME'] == table_name) & (df['COLUMN_NAME'] == column_name)]
        if not filtered_df.empty:
            desc = filtered_df['REQUIREMENT'].astype(str).iloc[0]
            data_type = filtered_df['DATA_TYPES'].astype(str).iloc[0]
        else:
            desc = ''
            data_type = ''
        desc = desc.replace(" ", "_")

        if columnCount == 2:
            stm += type2
        if column_name == 'SOR_CD':
            desc = 'SOURCE_CODE'
        if column_name == 'SRC_EFF_DTTM':
            desc = 'SOURCE_EFFECTIVE_DATE'
        
        stm += f'{column_name} AS {desc},\n'
        try:
            results.append({'TABLE_NAME': table_name, 'COLUMN_NAME': column_name,'data_type':datatypelist[count], 'DESC': desc,'view':viewName[count]})
        except:
            results.append({'TABLE_NAME': table_name, 'COLUMN_NAME': column_name,'data_type':data_type, 'DESC': desc})
        count+=1

    
    stm += type2Audit
    stm = stm[:-1] + f' FROM TBL_{table_name}'

    # Append SQL statement to the output file
    with open(file_name, 'a') as file:
        file.write(stm + '\n\n')
    
    return pd.DataFrame(results)

def find_tbl_name(statement):
    tbl_name = statement.split()[-1]
    if tbl_name.lower().startswith('dbo.'):
        return tbl_name[4:]
    return tbl_name

# Paths
file_path = r'C:\Users\pr38\Documents\DG\STTM\PROD_Servicing_Data_Warehouse_STTM_MASTER 9.xlsx'
lsams_path = r'C:\Users\pr38\Downloads\LSAMS Data Dictionary ALL Files 03-05-2019_latest 1.xlsx'
sheet_name = 'SRVC_WH'  
output_file = r'C:\Users\pr38\Documents\DG\STTM\output_results.xlsx' 

df = pd.read_excel(file_path, sheet_name=sheet_name)
df.columns = df.columns.str.strip().str.upper()

with open(r"C:\\Users\\pr38\\Desktop\\dumpp.txt", 'r') as file:
    content = file.read()

ddl_statements = content.split(';')
file_path = r'C:\Users\pr38\Downloads\outputs.txt'

# DataFrame to hold all results
all_results_df = pd.DataFrame()

for statement in ddl_statements:
    statement = statement.strip()
    if not statement:
        continue
    start = statement.find('(') + 1
    end = statement.rfind(')')
    tbl_name = find_tbl_name(statement[:start-1])
    if not tbl_name:
        continue
    columns_part = statement[start:end].strip()
    column_definitions = columns_part.split(',\n')
    column_names = []
    
    for column in column_definitions:
        k = column.strip()
        try:
        
            column_name = k.split()[0]
            if column_name.upper() == "CONSTRAINT":
                break
            column_names.append(column_name)
        except:
            pass
    if column_names:
        result_df = GetDescription(df,tbl_name, column_names, file_name=file_path)
        all_results_df = pd.concat([all_results_df, result_df], ignore_index=True)
# Save all results to a single Excel sheet
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    all_results_df.to_excel(writer, sheet_name='All_Tables', index=False)

print("Output saved to:", output_file)
