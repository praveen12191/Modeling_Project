import pandas as pd

def GetDescription(df, table_name, column_names,file_name):
    results = []
    stm = f"CREATE VIEW {table_name} AS SELECT "
    for column_name in column_names:
        results = []
    columnCount = 0 
    type2 = "ACTIVE_FLAG,\nEFFECTIVE_START_DATE,\nEFFECTIVE_END_DATE\n"
    type2Audit = "AUDIT_CREATED_DATE,\nAUDIT_UPDATED_DATE,\nETL_BATCH_ID,\nHASH_KEY\n"
    for column_name in column_names:
        columnCount+=1
        filtered_df = df[(df['TABLE_NAME'] == table_name) & (df['COLUMN_NAME'] == column_name)]
        if not filtered_df.empty:
            desc = '; '.join(filtered_df['REQUIREMENT'].astype(str).tolist())  
        else:
            desc = 'NO RECORD'
        desc = desc.replace(" ", "_")
        if(columnCount==2):
            stm+=type2
        if(column_name=='SOR_CD'):
            desc = 'SOURCE_CODE'
        if(column_name =='SRC_EFF_DTTM'):
            desc = 'SOURCE_EFFECTIVE_DATEE'
        stm+= f'{column_name} AS {desc},\n'
        results.append({'COLUMN_NAME': column_name, 'DESC': desc})
    stm+=type2Audit
    stm = stm[0:len(stm)-1]+F' FROM TBL_{table_name}'
    with open(file_name, 'a') as file:
        file.write(stm+'\n\n')
    return pd.DataFrame(results)


def find_tbl_name(statement):
    tbl_name = statement.split()[-1]
    if(tbl_name[0:3].lower() == 'dbo'):
        return tbl_name[4:]
    return tbl_name

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

with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
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
            result_df = GetDescription(df, tbl_name, column_names,file_name=file_path)
            result_df.to_excel(writer, sheet_name=tbl_name, index=False)

print("Output saved to:", output_file)
