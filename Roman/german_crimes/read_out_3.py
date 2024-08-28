import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read the Excel file, skip rows before the data
file_path = 'BU-F-01-T01-Faelle_xls.xlsx'
df = pd.read_excel(file_path, skiprows=7)  # Skipping the first 7 rows (0-indexed)

# Step 2: Extract and combine headers from rows 4, 5, and 6
headers = pd.read_excel(file_path, nrows=6, header=None)
headers_combined = headers.iloc[3:6].apply(lambda x: ' '.join(x.dropna().astype(str)).strip(), axis=0)

# Step 3: Ensure all column names are unique and non-empty
def make_unique(column_names):
    seen = {}
    result = []
    for col in column_names:
        if col == '':
            col = 'Unnamed'  # Replace empty names with 'Unnamed'
        if col in seen:
            seen[col] += 1
            result.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            result.append(col)
    return result

df.columns = make_unique(headers_combined)

# Optional: Check if the DataFrame looks correct
print(df.head())

# Step 4: Insert the DataFrame into the SQL table
# Ensure you have PostgreSQL running and accessible
# Modify 'password' and 'your_database' with actual values
engine = create_engine('postgresql://postgres:password@localhost:5432/your_database')

# Ensure the table name 'read_out_2' does not conflict with any folder names
df.to_sql('read_out_2', engine, if_exists='replace', index=False)
