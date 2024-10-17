lis = [
    'SMR010',
'CHKDIG',
'SMR011',
'SMA517',
'SPDATE',
'SMR080',
'SMA125',
'SMA280',
'SMA290',
'SMR081',
'SML530',
'SML030',
'SML150',
'SML300',
'SML320',
'SME320',
'SML500',
'SML510',
'SMM110',
'SMM080',
'SMM100',
'SMP070',
'SMP150',
'SMP180',
'SMP190',
'SMP210',
'SMP220',
'SMP206',
'SMP207',
'SMP230',
'SMP240',
'SMW010',
'SMW200',
'SMX070',
'SMX080',
'SMP060',
'SMX206',
'SMX207',
'SMM020',
'SMA515',
'SMA516',
'SMX270',
'SMFL4',
'FNMALOANNUMBER',
'FHA_VACASENBR',
'SMFL84',
'SMFL67',
'SMA150',
'SMX042',
'LOAN_DUE_DATE',
'SMS105',
'SME120',
'SMFL19',
'SMR180'
]

import pandas as pd
import re

# file_path = r'C:\Users\pr38\Documents\DG\STTM\Glossary_SWH_Business 3.csv'  
# output_file_path = r'C:\Users\pr38\Downloads\output_descriptions.txt'

# df = pd.read_excel(file_path)  
# df.columns = df.columns.str.strip().str.upper()

# def GetDescription(df, column_names, output_file):
#     results = []
#     for col_name in column_names:
#         res = ""
#         for x in col_name.split('_'):
#             filtered_df = df[df['ABBREVIATION'] == x]  
#             if not filtered_df.empty:
#                 desc = filtered_df['NAME'].astype(str).iloc[0]
#             else:
#                 desc = x
#             res += desc + '_'

#         res = res.rstrip('_')
#         results.append(res)


#     with open(output_file, 'a') as file:
#         for result in results:
#             file.write(result + '\n')

# GetDescription(df, lis, output_file_path)




file_path = r'C:\Users\pr38\Downloads\LSAMS Data Dictionary ALL Files 03-05-2019_latest 1.xlsx'  
output_file_path = r'C:\Users\pr38\Downloads\output_descriptions.txt'

df = pd.read_excel(file_path)  
df.columns = df.columns.str.strip().str.upper()
def GetDescription(df, column_names, output_file):
    results = []
    for col_name in column_names:
        print(col_name)
        filtered_df = df[(df['FILE'] == 'SRVDSR') & (df['FIELD_NAME'] == col_name)]
        if not filtered_df.empty:
            desc = filtered_df['COLUMN_HEADING'].astype(str).iloc[0]
        else:
            desc = col_name
        results.append(desc)
        

    with open(output_file, 'a') as file:
        for result in results:
            file.write(result + '\n')

GetDescription(df, lis, output_file_path)