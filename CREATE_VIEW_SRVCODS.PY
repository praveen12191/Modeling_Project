import pandas as pd

file_path = r'C:\Users\pr38\Downloads\output_results.xlsx'  
# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)  

# Group the data by column 'A' and aggregate columns 'B' and 'C' as lists
grouped = df.groupby('SRVC_WH TABLE').agg({'SRVC_WH COLUMN': list, 'VIEW': list}).reset_index()

# Write the results to a text file
output_file_path = r'c:\Users\pr38\Downloads\outp.txt'  # Update this to your desired output file path
with open(output_file_path, 'a') as file:
    LIS = []
    for index, row in grouped.iterrows():
       
        ln = len(row['SRVC_WH COLUMN'])
      
        stm = r'CREATE VIEW AS {}  SELECT '.format(row['SRVC_WH TABLE'])
        for ind in range(ln):
            stm += '{} as {},'.format(row['SRVC_WH COLUMN'][ind], row['VIEW'][ind])
        file.write(stm+';'+'\n\n')

print(f"Output saved to {output_file_path}")
