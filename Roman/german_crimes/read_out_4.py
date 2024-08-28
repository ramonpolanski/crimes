import psycopg2
from psycopg2 import sql
import pandas as pd
from sqlalchemy import create_engine

# Function to create a database if it doesn't exist
def create_database_if_not_exists(dbname, user, password, host, port):
    # Connect to the default database (postgres) to create a new database
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.autocommit = True  # Allow creation of the database
    cursor = conn.cursor()

    # Check if the database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}';")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(dbname)
        ))
        print(f"Database '{dbname}' created.")
    else:
        print(f"Database '{dbname}' already exists.")

    # Close connection to the default database
    cursor.close()
    conn.close()

# Database connection details
user = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'
dbname = 'your_database'

# Create the database if it doesn't exist
create_database_if_not_exists(dbname, user, password, host, port)

# Connect to the newly created or existing database using SQLAlchemy
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')

# Load data from an Excel file, skipping the first 8 rows
file_path = 'BU-F-01-T01-Faelle_xls.xlsx'
df = pd.read_excel(file_path, skiprows=7)

# Print the first few rows to check the data
print("Data preview after skipping rows:")
print(df.head())

# Print the columns to determine how many columns are present
print("Columns in the DataFrame:")
print(df.columns)

# Optional: Inspect data types
print("Data types in the DataFrame:")
print(df.dtypes)

# Manually set column names (adjust these as needed)
column_names = [
    'Schlüssel', 'Straftat', 'Anzahl erfasste Fälle', '%-Anteil an allen Fällen', 'erfasste Fälle davon: \nVersuche: Anzahl', 
    'in %', 'Tatortverteilung bis unter 20.000 Einwohner', '20.000 bis unter 100.000', '100.000 bis unter 500.000', '500.000 und mehr',
    'unbekannt', 'mit Schusswaffe gedroht', 'mit Schusswaffe geschossen', 'Aufklärung Anzahl', 'Aufklärung %',
    'Tatverdächtige insgesamt', 'TV männlich', 'TV weiblich', 'Nichtdeutsche TV\nAnzahl', 'Anteil an TV insg.in %'
]

# Ensure the number of column names matches the number of columns in the DataFrame
if len(column_names) != len(df.columns):
    raise ValueError(f"Length mismatch: Expected {len(df.columns)} columns, but provided {len(column_names)} column names.")

# Assign combined headers to the DataFrame
df.columns = column_names

# Optional: Print the DataFrame to verify column names
print("Data preview with correct column names:")
print(df.head())

# Optional: Clean the data by removing or correcting erroneous entries
# Example: Remove any rows where critical values are NaN or incorrect
df = df.dropna()  # This is an example; adjust based on your needs

# Write the DataFrame to the SQL table
df.to_sql('your_table_name', engine, if_exists='replace', index=False)

print("Data has been loaded into the database.")
