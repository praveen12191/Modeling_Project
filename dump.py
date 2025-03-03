import pandas as pd

# Load Excel A (all sheets)
excel_a_path = "C:\\Users\\pr38\\Downloads\\NON_TKAMS Mapping (3).xlsx"
sheets = pd.read_excel(excel_a_path, sheet_name=None)

# Extract unique table names from Excel A
tables_in_a = set()
missing_table_rows = []  # List to store first rows of missing tables

# Iterate through sheets and collect table names
for sheet_name, df in sheets.items():
    if "SF_TABLE" in df.columns and sheet_name not in ["BKFS", "SS", "DIL", "REO", "OperationalReporting","SRVC_WH"]:
        for table in df["SF_TABLE"].dropna().unique():
            tables_in_a.add(table)
            # Store first row of each table
            first_row = df[df["SF_TABLE"] == table].iloc[:1]  # Get the first row
            first_row.insert(0, "Missing_Table", table)  # Add column for table name
            missing_table_rows.append(first_row)

# Load Excel B
excel_b_path = "C:\\Users\\pr38\\Downloads\\Table_Assignment_Status_Tracker (1).xlsx"
df_b = pd.read_excel(excel_b_path)

# Extract table names from Excel B
tables_in_b = set(df_b["Source table name"].dropna().unique())

# Find missing tables (tables in A but not in B)
missing_tables = tables_in_a - tables_in_b

# Filter only missing tables' first rows
filtered_rows = pd.concat(missing_table_rows) if missing_table_rows else pd.DataFrame()

# Save to Excel if there are missing tables
output_file = "C:\\Users\\pr38\\Downloads\\Missing_Tables_First_Row.xlsx"

if not filtered_rows.empty:
    filtered_rows.to_excel(output_file, sheet_name="Missing_Tables", index=False)
    print(f"First rows of missing tables saved to {output_file} in one sheet.")
else:
    print("All tables in Excel A are present in Excel B.")
