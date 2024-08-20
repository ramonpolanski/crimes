import sqlite3, os

conn = sqlite3.connect('crime_investigation.db')
cursor = conn.cursor()

import random
import datetime
import sqlite3

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

for crime_id in range(1, 36):
    crime_type = random.choice(crime_types)
    location = random.choice(locations)
    crime_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
    
    cursor.execute(f'''
    INSERT INTO Crimes (CrimeID, Type, Date, Location) 
    VALUES ({crime_id}, '{crime_type}', '{crime_date}', '{location}');
    ''')
    
    evidence_id = crime_id
    evidence_type = random.choice(evidence_types)
    evidence_description = random.choice(descriptions)
    
    cursor.execute(f'''
    INSERT INTO Evidence (EvidenceID, Type, Description, CrimeID) 
    VALUES ({evidence_id}, '{evidence_type}', '{evidence_description}', {crime_id});
    ''')
    
    officer_id = crime_id
    officer_name = random.choice(officer_names)
    officer_rank = random.choice(officer_ranks)
    officer_department = random.choice(officer_departments)
    
    cursor.execute(f'''
    INSERT INTO Officers (OfficerID, Name, Rank, Department, CrimeID) 
    VALUES ({officer_id}, '{officer_name}', '{officer_rank}', '{officer_department}', {crime_id});
    ''')
    
    suspect_id = crime_id
    suspect_name = random.choice(suspect_names)
    suspect_age = random.randint(18, 65)
    suspect_description = random.choice(suspect_descriptions)
    
    cursor.execute(f'''
    INSERT INTO Suspects (SuspectID, Name, Age, Description, CrimeID) 
    VALUES ({suspect_id}, '{suspect_name}', {suspect_age}, '{suspect_description}', {crime_id});
    ''')

# Commit the transactions
conn.commit()

# Close the connection
conn.close()
