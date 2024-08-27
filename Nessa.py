import sqlite3
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk




# Database setup
db_file = 'crime_cases.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CrimeTypes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Open'
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Locations (
        LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT
    )''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS EvidenceType (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        description TEXT,
        FOREIGN KEY(case_id) REFERENCES CrimeCase(id)
    )
''')
    
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suspect (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        name TEXT,
        description TEXT,
        FOREIGN KEY(case_id) REFERENCES CrimeCase(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Officer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        name TEXT,
        rank TEXT,
        FOREIGN KEY(case_id) REFERENCES CrimeCase(id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Crimes (
        CrimeID INTEGER PRIMARY KEY AUTOINCREMENT,
        CrimeTypeID INTEGER,
        LocationID INTEGER,
        SuspectID INTEGER,
        OfficerID INTEGER,
        Date DATE,
        Time TIME,
        Status TEXT,
        FOREIGN KEY (CrimeTypeID) REFERENCES CrimeTypes(CrimeTypeID),
        FOREIGN KEY (LocationID) REFERENCES Locations(LocationID),
        FOREIGN KEY (SuspectID) REFERENCES Suspects(SuspectID),
        FOREIGN KEY (OfficerID) REFERENCES Officers(OfficerID)
    )''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS CrimeEvidence (
        EvidenceID INTEGER PRIMARY KEY AUTOINCREMENT,
        CrimeID INTEGER,
        EvidenceTypeID INTEGER,
        Description TEXT,
        FOREIGN KEY (CrimeID) REFERENCES Crimes(CrimeID),
        FOREIGN KEY (EvidenceTypeID) REFERENCES EvidenceTypes(EvidenceTypeID)
    )''')


conn.commit()

# Log file helper
def log_case_action(case_id, action):
    log_dir = f'logs/case_{case_id}'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'log.txt')
    
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {action}\n")

# CRUD functions
def add_crime_case():
    title = input("Enter case title: ")
    description = input("Enter case description: ")
    
    cursor.execute("INSERT INTO CrimeCase (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    case_id = cursor.lastrowid
    log_case_action(case_id, f"Case '{title}' added.")
    
    print(f"Case '{title}' added with ID {case_id}.")

def view_crime_cases():
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    
    if not cases:
        print("No cases found.")
        return
    
    for case in cases:
        print(f"ID: {case[0]}, Title: {case[1]}, Description: {case[2]}, Status: {case[3]}")
        view_related_data(case[0])

def view_related_data(case_id):
    cursor.execute("SELECT description FROM Evidence WHERE case_id=?", (case_id,))
    evidences = cursor.fetchall()
    cursor.execute("SELECT name, description FROM Suspect WHERE case_id=?", (case_id,))
    suspects = cursor.fetchall()
    cursor.execute("SELECT name, rank FROM Officer WHERE case_id=?", (case_id,))
    officers = cursor.fetchall()
    
#Main Menu
def main_menu():
    while True:
        print("\nCrime Case Management System")
        print("1. Add Crime Case")
        print("2. View Crime Cases")
        print("3. Update Crime Case")
        print("4. Delete Crime Case")
        print("5. Add Related Data (Evidence/Suspect/Officer)")    
        print("6. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_crime_case()
        elif choice == '2':
            view_crime_cases()
        elif choice == '3':
            update_crime_case()
        elif choice == '4':
            delete_crime_case()
        elif choice == '5':
            add_related_data()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
            
            
    print("  Evidence:")
    for evidence in evidences:
        print(f"    - {evidence[0]}")
    
    print("  Suspects:")
    for suspect in suspects:
        print(f"    - {suspect[0]}: {suspect[1]}")
    
    print("  Officers:")
    for officer in officers:
        print(f"    - {officer[0]} ({officer[1]})")

def update_crime_case():
    case_id = input("Enter case ID to update: ")
    cursor.execute("SELECT * FROM CrimeCase WHERE id=?", (case_id,))
    case = cursor.fetchone()
    
    if not case:
        print("Case not found.")
        return
    
    new_title = input(f"Enter new title (current: {case[1]}): ") or case[1]
    new_description = input(f"Enter new description (current: {case[2]}): ") or case[2]
    new_status = input(f"Enter new status (current: {case[3]}): ") or case[3]
    
    cursor.execute("UPDATE CrimeCase SET title=?, description=?, status=? WHERE id=?", (new_title, new_description, new_status, case_id))
    conn.commit()
    log_case_action(case_id, f"Case '{new_title}' updated.")
    
    print(f"Case '{new_title}' updated.")

def delete_crime_case():
    case_id = input("Enter case ID to delete: ")
    cursor.execute("DELETE FROM CrimeCase WHERE id=?", (case_id,))
    cursor.execute("DELETE FROM Evidence WHERE case_id=?", (case_id,))
    cursor.execute("DELETE FROM Suspect WHERE case_id=?", (case_id,))
    cursor.execute("DELETE FROM Officer WHERE case_id=?", (case_id,))
    conn.commit()
    log_case_action(case_id, "Case deleted.")
    
    print(f"Case ID {case_id} deleted.")

def add_related_data():
    case_id = input("Enter case ID to add related data: ")
    cursor.execute("SELECT * FROM CrimeCase WHERE id=?", (case_id,))
    case = cursor.fetchone()
    
    if not case:
        print("Case not found.")
        return
    
    data_type = input("What do you want to add? (evidence/suspect/officer): ").strip().lower()
    
    if data_type == "evidence":
        description = input("Enter evidence description: ")
        cursor.execute("INSERT INTO Evidence (case_id, description) VALUES (?, ?)", (case_id, description))
        conn.commit()
        log_case_action(case_id, f"Evidence added: {description}.")
        print("Evidence added.")
    
    elif data_type == "suspect":
        name = input("Enter suspect name: ")
        description = input("Enter suspect description: ")
        cursor.execute("INSERT INTO Suspect (case_id, name, description) VALUES (?, ?, ?)", (case_id, name, description))
        conn.commit()
        log_case_action(case_id, f"Suspect added: {name}.")
        print("Suspect added.")
    
    elif data_type == "officer":
        name = input("Enter officer name: ")
        rank = input("Enter officer rank: ")
        cursor.execute("INSERT INTO Officer (case_id, name, rank) VALUES (?, ?, ?)", (case_id, name, rank))
        conn.commit()
        log_case_action(case_id, f"Officer added: {name}.")
        print("Officer added.")
    
    else:
        print("Invalid option.")
"""
#Main Menu
def main_menu():
    while True:
        print("\nCrime Case Management System")
        print("1. Add Crime Case")
        print("2. View Crime Cases")
        print("3. Update Crime Case")
        print("4. Delete Crime Case")
        print("5. Add Related Data (Evidence/Suspect/Officer)")
        print("6. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_crime_case()
        elif choice == '2':
            view_crime_cases()
        elif choice == '3':
            update_crime_case()
        elif choice == '4':
            delete_crime_case()
        elif choice == '5':
            add_related_data()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
            
            """
            
            
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Add Crime Case")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Tittle", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    #tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    
    
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("View Crime Case")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Title", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("view_Evidence")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Title", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Update Crime Case")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Title", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Delete Crime Case")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Title", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    
def Crime_Cases():
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title("Add related data")
    new_window.geometry("800x400")
    new_window.configure(bg='gold')
    # Configure the grid for the new window
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_rowconfigure(0, weight=1)
    # Create a Treeview to display the cases
    tree = ttk.Treeview(new_window, columns=("ID", "Title", "Description", "Status"), show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Description", text="Description")
    tree.heading("Status", text="Status")
    tree.grid(row=0, column=0, sticky="nsew")
    # Fetch cases from the database
    cursor.execute("SELECT * FROM CrimeCase")
    cases = cursor.fetchall()
    if not cases:
        print("No cases found.")
    for case in cases:
        tree.insert("", "end", values=case)
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    
    
    #creating a gui
def main_TTK_menu():
    root=tk.Tk()
    root.title("Crime Data Viewer")
    root.geometry("500x400")
    root.configure(bg="#FFD54F")
    crime =tk.Button(root, text="View Crime Case",command=Crime_Cases)
    crime.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    view_crime =tk.Button(root, text="Add Crime Case",command=Crime_Cases)
    view_crime.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    Update_crime =tk.Button(root, text="Update Crime Case",command=Crime_Cases)
    Update_crime.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    Del_crime =tk.Button(root, text="Delete Crime Case",command=Crime_Cases)
    Del_crime.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    Rel_data =tk.Button(root, text="Add related data",command=Crime_Cases)
    Rel_data.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
    
    
    
    root.mainloop()
if __name__ == '__main__':
    main_TTK_menu()
    conn.close()



