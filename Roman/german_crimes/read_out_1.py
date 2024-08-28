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

# Load data from an Excel file (modify the file name and path as needed)
df = pd.read_excel('BU-F-01-T01-Faelle_xls.xlsx')

# Write the DataFrame to the SQL table
df.to_sql('your_table_name', engine, if_exists='replace', index=False)

print("Data has been loaded into the database.")
