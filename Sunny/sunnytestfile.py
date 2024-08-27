import psycopg2
from psycopg2 import sql
import random
import datetime
import os

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

def connect_to_db(dbname, user, password, host, port):
    # Connect to your actual database
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

def create_db():
    user = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5432'
    dbname = 'crime_investigation'

    # Ensure the database exists
    create_database_if_not_exists(dbname, user, password, host, port)

    # Connect to the database
    conn = connect_to_db(dbname, user, password, host, port)
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS Crimes CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Evidence CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Officers CASCADE')
    cursor.execute('DROP TABLE IF EXISTS Suspects CASCADE')

    # Create tables
    cursor.execute('''
    CREATE TABLE Crimes (
        CrimeID SERIAL PRIMARY KEY,
        Type VARCHAR(255),
        Date DATE,
        Location VARCHAR(255)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Evidence (
        EvidenceID SERIAL PRIMARY KEY,
        Type VARCHAR(255),
        Description TEXT,
        CrimeID INTEGER REFERENCES Crimes(CrimeID) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE Officers (
        OfficerID SERIAL PRIMARY KEY,
        Name VARCHAR(255),
        Rank VARCHAR(255),
        Department VARCHAR(255),
        CrimeID INTEGER REFERENCES Crimes(CrimeID) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE Suspects (
        SuspectID SERIAL PRIMARY KEY,
        Name VARCHAR(255),
        Age INTEGER,
        Description TEXT,
        CrimeID INTEGER REFERENCES Crimes(CrimeID) ON DELETE CASCADE
    );
    ''')

    # Sample data
    crime_types = ['187 - Murder', '211 - Robbery', '459 - Burglary', '488 - Petty Theft', '245 - Assault']
    locations = ['Detroit', 'Los Angeles', 'New York', 'Chicago', 'Houston']
    evidence_types = ['Weapon', 'DNA', 'Fingerprint', 'Video Surveillance', 'Eyewitness']
    descriptions = ['Switchblade', 'Handgun', 'CCTV Footage', 'Blood Sample', 'Fingerprint on glass']
    officer_names = ['John Doe', 'Jane Doe', 'Alice Smith', 'Bob Johnson', 'Charlie Brown']
    officer_ranks = ['Lieutenant', 'Sergeant', 'Detective', 'Captain']
    officer_departments = ['Homicide', 'Robbery', 'Fraud', 'Vice']
    suspect_names = ['Jane Smith', 'John Brown', 'Emma Davis', 'Michael Miller', 'Olivia Wilson']
    suspect_descriptions = ['blonde, heavy smoker', 'tall, muscular', 'short, thin', 'medium height, athletic', 'scar on left cheek']

    def random_date(start, end):
        return start + datetime.timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )

    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime.today()

    # Insert random data
    for _ in range(1, 36):
        crime_type = random.choice(crime_types)
        location = random.choice(locations)
        crime_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        
        cursor.execute('''
        INSERT INTO Crimes (Type, Date, Location) 
        VALUES (%s, %s, %s) RETURNING CrimeID;
        ''', (crime_type, crime_date, location))
        crime_id = cursor.fetchone()[0]

        evidence_type = random.choice(evidence_types)
        evidence_description = random.choice(descriptions)
        
        cursor.execute('''
        INSERT INTO Evidence (Type, Description, CrimeID) 
        VALUES (%s, %s, %s);
        ''', (evidence_type, evidence_description, crime_id))
        
        officer_name = random.choice(officer_names)
        officer_rank = random.choice(officer_ranks)
        officer_department = random.choice(officer_departments)
        
        cursor.execute('''
        INSERT INTO Officers (Name, Rank, Department, CrimeID) 
        VALUES (%s, %s, %s, %s);
        ''', (officer_name, officer_rank, officer_department, crime_id))
        
        suspect_name = random.choice(suspect_names)
        suspect_age = random.randint(18, 65)
        suspect_description = random.choice(suspect_descriptions)
        
        cursor.execute('''
        INSERT INTO Suspects (Name, Age, Description, CrimeID) 
        VALUES (%s, %s, %s, %s);
        ''', (suspect_name, suspect_age, suspect_description, crime_id))

    # Commit the transactions
    conn.commit()

    # Close the connection
    conn.close()

def display_related_data(crime_id):
    conn = connect_to_db('crime_investigation', 'postgres', 'password', 'localhost', '5432')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Crimes WHERE CrimeID = %s', (crime_id,))
    crime = cursor.fetchone()
    print("\nCrime Details:")
    print(f"ID: {crime[0]}, Type: {crime[1]}, Date: {crime[2]}, Location: {crime[3]}")
    input("\nPress Enter to continue...")

    cursor.execute('SELECT * FROM Evidence WHERE CrimeID = %s', (crime_id,))
    evidence = cursor.fetchone()
    print("\nEvidence Details:")
    print(f"ID: {evidence[0]}, Type: {evidence[1]}, Description: {evidence[2]}")
    input("\nPress Enter to continue...")

    cursor.execute('SELECT * FROM Officers WHERE CrimeID = %s', (crime_id,))
    officer = cursor.fetchone()
    print("\nOfficer Details:")
    print(f"ID: {officer[0]}, Name: {officer[1]}, Rank: {officer[2]}, Department: {officer[3]}")
    input("\nPress Enter to continue...")

    cursor.execute('SELECT * FROM Suspects WHERE CrimeID = %s', (crime_id,))
    suspect = cursor.fetchone()
    print("\nSuspect Details:")
    print(f"ID: {suspect[0]}, Name: {suspect[1]}, Age: {suspect[2]}, Description: {suspect[3]}")
    input("\nPress Enter to continue...")

    conn.close()

def search_and_display(query, param=()):
    conn = connect_to_db('crime_investigation', 'postgres', 'password', 'localhost', '5432')
    cursor = conn.cursor()
    cursor.execute(query, param)
    results = cursor.fetchall()
    conn.close()
    return results


    if not results:
        print("No results found.")
        input("\nPress Enter to continue...")
        conn.close()
        return

    for i, result in enumerate(results, 1):
        print(f"{i}. {result}")

    choice = int(input("\nSelect the number of the entry to view more details: "))
    selected = results[choice - 1]

    display_related_data(selected[0])
    conn.close()

def show_unique_values_and_get_selection(query):
    conn = connect_to_db('crime_investigation', 'postgres', 'password', 'localhost', '5432')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    if not results:
        print("No data available.")
        input("\nPress Enter to continue...")
        conn.close()
        return None
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result[0]}")

    choice = int(input("\nSelect the number of your choice: "))
    selected_value = results[choice - 1][0]

    conn.close()
    return selected_value

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('''
        1. Search by Case ID
        2. Search by Crime
        3. Search by Date
        4. Search by Location
        5. Search by Evidence (Type)
        6. Search by Evidence (Description)
        7. Search by Officer (Name)
        8. Search by Suspect (Name)
        9. Exit
        ''')
        choice = input('Enter your choice: ')

        if choice == '1':
            case_id = input("Enter Case ID: ")
            search_and_display('SELECT * FROM Crimes WHERE CrimeID = %s', (case_id,))
        elif choice == '2':
            crime_type = show_unique_values_and_get_selection('SELECT DISTINCT Type FROM Crimes')
            if crime_type:
                search_and_display('SELECT * FROM Crimes WHERE Type = %s', (crime_type,))
        elif choice == '3':
            crime_date = show_unique_values_and_get_selection('SELECT DISTINCT Date FROM Crimes')
            if crime_date:
                search_and_display('SELECT * FROM Crimes WHERE Date = %s', (crime_date,))
        elif choice == '4':
            location = show_unique_values_and_get_selection('SELECT DISTINCT Location FROM Crimes')
            if location:
                search_and_display('SELECT * FROM Crimes WHERE Location = %s', (location,))
        elif choice == '5':
            evidence_type = show_unique_values_and_get_selection('SELECT DISTINCT Type FROM Evidence')
            if evidence_type:
                search_and_display('SELECT * FROM Evidence WHERE Type = %s', (evidence_type,))
        elif choice == '6':
            evidence_description = show_unique_values_and_get_selection('SELECT DISTINCT Description FROM Evidence')
            if evidence_description:
                search_and_display('SELECT * FROM Evidence WHERE Description = %s', (evidence_description,))
        elif choice == '7':
            officer_name = show_unique_values_and_get_selection('SELECT DISTINCT Name FROM Officers')
            if officer_name:
                search_and_display('SELECT * FROM Officers WHERE Name = %s', (officer_name,))
        elif choice == '8':
            suspect_name = show_unique_values_and_get_selection('SELECT DISTINCT Name FROM Suspects')
            if suspect_name:
                search_and_display('SELECT * FROM Suspects WHERE Name = %s', (suspect_name,))
        elif choice == '9':
            break
        else:
            print("Invalid choice, please try again.")
            input("\nPress Enter to continue...")

def main():
    create_db()
    menu()

if __name__ == '__main__':
    main()
