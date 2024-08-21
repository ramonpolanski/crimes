import sqlite3
import random
import datetime
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

def create_db():
    conn = sqlite3.connect('crime_investigation.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS Crimes')
    cursor.execute('DROP TABLE IF EXISTS Evidence')
    cursor.execute('DROP TABLE IF EXISTS Officers')
    cursor.execute('DROP TABLE IF EXISTS Suspects')

    cursor.execute('''
    CREATE TABLE Crimes (
        CrimeID INTEGER PRIMARY KEY,
        Type TEXT,
        Date TEXT,
        Location TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE Evidence (
        EvidenceID INTEGER PRIMARY KEY,
        Type TEXT,
        Description TEXT,
        CrimeID INTEGER,
        FOREIGN KEY(CrimeID) REFERENCES Crimes(CrimeID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Officers (
        OfficerID INTEGER PRIMARY KEY,
        Name TEXT,
        Rank TEXT,
        Department TEXT,
        CrimeID INTEGER,
        FOREIGN KEY(CrimeID) REFERENCES Crimes(CrimeID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE Suspects (
        SuspectID INTEGER PRIMARY KEY,
        Name TEXT,
        Age INTEGER,
        Description TEXT,
        CrimeID INTEGER,
        FOREIGN KEY(CrimeID) REFERENCES Crimes(CrimeID)
    );
    ''')

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
        
        cursor.execute('''
        INSERT INTO Crimes (CrimeID, Type, Date, Location) 
        VALUES (?, ?, ?, ?);
        ''', (crime_id, crime_type, crime_date, location))
        
        evidence_id = crime_id
        evidence_type = random.choice(evidence_types)
        evidence_description = random.choice(descriptions)
        
        cursor.execute('''
        INSERT INTO Evidence (EvidenceID, Type, Description, CrimeID) 
        VALUES (?, ?, ?, ?);
        ''', (evidence_id, evidence_type, evidence_description, crime_id))
        
        officer_id = crime_id
        officer_name = random.choice(officer_names)
        officer_rank = random.choice(officer_ranks)
        officer_department = random.choice(officer_departments)
        
        cursor.execute('''
        INSERT INTO Officers (OfficerID, Name, Rank, Department, CrimeID) 
        VALUES (?, ?, ?, ?, ?);
        ''', (officer_id, officer_name, officer_rank, officer_department, crime_id))
        
        suspect_id = crime_id
        suspect_name = random.choice(suspect_names)
        suspect_age = random.randint(18, 65)
        suspect_description = random.choice(suspect_descriptions)
        
        cursor.execute('''
        INSERT INTO Suspects (SuspectID, Name, Age, Description, CrimeID) 
        VALUES (?, ?, ?, ?, ?);
        ''', (suspect_id, suspect_name, suspect_age, suspect_description, crime_id))

    conn.commit()
    conn.close()

def fetch_data(query, param=()):
    conn = sqlite3.connect('crime_investigation.db')
    cursor = conn.cursor()
    cursor.execute(query, param)
    result = cursor.fetchall()
    conn.close()
    return result

def show_crime_details(crime_id):
    crime = fetch_data('SELECT * FROM Crimes WHERE CrimeID = ?', (crime_id,))
    evidence = fetch_data('SELECT * FROM Evidence WHERE CrimeID = ?', (crime_id,))
    officer = fetch_data('SELECT * FROM Officers WHERE CrimeID = ?', (crime_id,))
    suspect = fetch_data('SELECT * FROM Suspects WHERE CrimeID = ?', (crime_id,))

    details = f'''
    Crime Details:
    ID: {crime[0][0]}, Type: {crime[0][1]}, Date: {crime[0][2]}, Location: {crime[0][3]}

    Evidence Details:
    ID: {evidence[0][0]}, Type: {evidence[0][1]}, Description: {evidence[0][2]}

    Officer Details:
    ID: {officer[0][0]}, Name: {officer[0][1]}, Rank: {officer[0][2]}, Department: {officer[0][3]}

    Suspect Details:
    ID: {suspect[0][0]}, Name: {suspect[0][1]}, Age: {suspect[0][2]}, Description: {suspect[0][3]}
    '''
    messagebox.showinfo("Crime Details", details)

def on_crime_select(event):
    selected = crime_tree.selection()
    if selected:
        crime_id = crime_tree.item(selected[0], 'values')[0]
        show_crime_details(crime_id)

def populate_treeview():
    for row in fetch_data('SELECT * FROM Crimes'):
        crime_tree.insert('', 'end', values=row)

def main():
    create_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("Crime Investigation Database")
    root.geometry("800x600")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#2e2e2e",
                    foreground="white",
                    rowheight=25,
                    fieldbackground="#2e2e2e")
    style.map('Treeview', background=[('selected', '#1f538d')])

    global crime_tree
    crime_tree = ttk.Treeview(root, columns=("CrimeID", "Type", "Date", "Location"), show="headings")
    crime_tree.heading("CrimeID", text="Crime ID")
    crime_tree.heading("Type", text="Type")
    crime_tree.heading("Date", text="Date")
    crime_tree.heading("Location", text="Location")
    crime_tree.bind('<<TreeviewSelect>>', on_crime_select)
    crime_tree.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    populate_treeview()

    root.mainloop()

if __name__ == '__main__':
    main()

