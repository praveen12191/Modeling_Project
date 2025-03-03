import pandas as pd

# Load the Excel file
file_path = "C:\\Users\\pr38\\Downloads\\Book1.xlsx"  # Update with your actual file path
df = pd.read_excel(file_path)

# Filter rows where LOAD_TYPE is 'TYPE2' or 'TYPE 2'
filtered_df = df[df["LOAD_TYPE"].str.strip().str.upper().isin(["TYPE2", "TYPE 2"])].copy()

# Find unique tables that need the ACTIVE_FLAG column
tables_to_modify = filtered_df[["SERVER", "DATABASE", "SCHEMA", "TABLE", "SF_DATABASE", "SF_SCHEMA", "SF_TABLE"]].drop_duplicates()

# Create a new DataFrame for ACTIVE_FLAG rows
active_flag_rows = tables_to_modify.copy()
active_flag_rows["COLUMN"] = "ACTIVE_FLAG"
active_flag_rows["SF_COLUMN"] = "ACTIVE_FLAG"

# Fill other columns with default values or NaN
for col in df.columns:
    if col not in active_flag_rows.columns:
        active_flag_rows[col] = None  # Set missing values as None

# Append the new rows to the original DataFrame
final_df = pd.concat([df, active_flag_rows], ignore_index=True)

# Save the updated data back to Excel
output_file = "C:\\Users\\pr38\\Downloads\\Book2.xlsx"
final_df.to_excel(output_file, index=False)

print(f"Updated file saved as {output_file}")
