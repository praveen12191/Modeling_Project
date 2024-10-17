import pandas as pd

file_path = r'C:\Users\pr38\Downloads\Snowflake_SRVCWH_STTM.xlsx'  
df = pd.read_excel(file_path)  
grouped = df.groupby('SRVC_WH TABLE').agg({'SRVC_WH COLUMN': list, 'VIEW': list}).reset_index()

output_file_path = r'c:\Users\pr38\Downloads\outp.txt'  
with open(output_file_path, 'a') as file:
    LIS = []
    for index, row in grouped.iterrows():
       
        ln = len(row['SRVC_WH COLUMN'])
      
        stm = r'CREATE VIEW {} AS  SELECT '.format(row['SRVC_WH TABLE'])
        for ind in range(ln):
            stm += '{} as {},'.format(row['SRVC_WH COLUMN'][ind], row['VIEW'][ind])
        stm = stm[0:len(stm)-1] + ' from  TBL_{}'.format(row['SRVC_WH TABLE'])
        file.write(stm+';'+'\n\n')

print(f"Output saved to {output_file_path}")
