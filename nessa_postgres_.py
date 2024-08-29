import psycopg2
import datetime
import customtkinter as ctk
from tkinter import ttk
from tkinter import Toplevel, Scrollbar, Canvas, Text

# Database Functions
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='crime_investigation',
            user='postgres',
            password='password',
            host='localhost',
            port='5432'
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Database Connection Error", f"An error occurred: {e}")
        return None

def create_db():
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Crimes (
        CrimeID SERIAL PRIMARY KEY,
        Type TEXT,
        Date DATE,
        Location TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Evidence (
        EvidenceID SERIAL PRIMARY KEY,
        Type TEXT,
        Description TEXT,
        CrimeID INTEGER REFERENCES Crimes(CrimeID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Officers (
        OfficerID SERIAL PRIMARY KEY,
        Name TEXT,
        Rank TEXT,
        Department TEXT,
        CrimeID INTEGER REFERENCES Crimes(CrimeID)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suspects (
        SuspectID SERIAL PRIMARY KEY,
        Name TEXT,
        Age INTEGER,
        Description TEXT,
        CrimeID INTEGER REFERENCES Crimes(CrimeID)
    );
    ''')

    conn.commit()
    conn.close()

def fetch_data(query, param=()):
    conn = connect_to_db()
    if not conn:
        return []

    cursor = conn.cursor()
    cursor.execute(query, param)
    result = cursor.fetchall()
    conn.close()
    return result

def execute_query(query, param=()):
    conn = connect_to_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, param)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

# GUI Functions
def populate_treeview():
    crime_tree.delete(*crime_tree.get_children())
    for row in fetch_data('SELECT * FROM Crimes'):
        crime_tree.insert('', 'end', values=row)

def add_crime():
    type = type_entry.get()
    date = date_entry.get()
    location = location_entry.get()

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
        return

    if type and date and location:
        execute_query('INSERT INTO Crimes (Type, Date, Location) VALUES (%s, %s, %s)', (type, date, location))
        populate_treeview()
        messagebox.showinfo("Success", "Crime added successfully.")
    else:
        messagebox.showerror("Input Error", "All fields must be filled out.")

def update_crime():
    selected = crime_tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a record to update.")
        return

    crime_id = crime_tree.item(selected[0], 'values')[0]
    type = type_entry.get()
    date = date_entry.get()
    location = location_entry.get()

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
        return

    if type and date and location:
        execute_query('UPDATE Crimes SET Type = %s, Date = %s, Location = %s WHERE CrimeID = %s', 
                      (type, date, location, crime_id))
        populate_treeview()
        messagebox.showinfo("Success", "Crime updated successfully.")
    else:
        messagebox.showerror("Input Error", "All fields must be filled out.")

def delete_crime():
    selected = crime_tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a record to delete.")
        return

    crime_id = crime_tree.item(selected[0], 'values')[0]
    execute_query('DELETE FROM Crimes WHERE CrimeID = %s', (crime_id,))
    populate_treeview()
    messagebox.showinfo("Success", "Crime deleted successfully.")

def on_crime_select(event):
    selected = crime_tree.selection()
    if selected:
        selected_record = crime_tree.item(selected[0], 'values')
        type_entry.delete(0, ctk.END)
        type_entry.insert(0, selected_record[1])
        date_entry.delete(0, ctk.END)
        date_entry.insert(0, selected_record[2])
        location_entry.delete(0, ctk.END)
        location_entry.insert(0, selected_record[3])

def view_case_details():
    selected = crime_tree.selection()
    if not selected:
        messagebox.showerror("Selection Error", "Please select a record to view details.")
        return

    crime_id = crime_tree.item(selected[0], 'values')[0]

    # Fetch details from the database
    officers = fetch_data('SELECT Name, Rank FROM Officers WHERE CrimeID = %s', (crime_id,))
    suspects = fetch_data('SELECT Name FROM Suspects WHERE CrimeID = %s', (crime_id,))
    evidence = fetch_data('SELECT Type, Description FROM Evidence WHERE CrimeID = %s', (crime_id,))

    # Create the details string
    details = f"Crime ID: {crime_id}\n\nOfficers:\n"
    for officer in officers:
        details += f"Name: {officer[0]}, Rank: {officer[1]}\n"

    details += "\nSuspects:\n"
    for suspect in suspects:
        details += f"Name: {suspect[0]}\n"

    details += "\nEvidence:\n"
    for ev in evidence:
        details += f"Type: {ev[0]}, Description: {ev[1]}\n"

    # Show the details in a custom dialog
    show_custom_dialog("Crime Case Details", details)


from tkinter import Toplevel, Canvas, Scrollbar, Text

def show_custom_dialog(title, message):
    # Create a new top-level window
    dialog = Toplevel(root)
    dialog.title(title)
    dialog.geometry("500x400")
    dialog.configure(bg="black")

    # Add a canvas and scrollbar to handle long messages
    canvas = Canvas(dialog, bg="black", highlightthickness=0)
    scrollbar = Scrollbar(dialog, orient="vertical", command=canvas.yview)
    text = Text(canvas, bg="black", fg="white", wrap="word", padx=10, pady=10, bd=0, highlightthickness=0)

    # Add text to the Text widget
    text.insert("1.0", message)
    text.configure(state="disabled")

    # Layout widgets
    canvas.create_window((0, 0), window=text, anchor="nw")
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    scrollbar.config(command=canvas.yview)
    
    dialog.mainloop()

# Main Application
def main():
    create_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    global root, crime_tree, type_entry, date_entry, location_entry

    root = ctk.CTk()
    root.title("Crime Investigation Database")
    root.geometry("800x600")

    # Layout Configuration
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)

    # Treeview Styles
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#2e2e2e", foreground="White", rowheight=25, fieldbackground="#2e2e2e")
    style.map('Treeview', background=[('selected', '#1f538d')])

    # Treeview
    crime_tree = ttk.Treeview(root, columns=("CrimeID", "Type", "Date", "Location"), show="headings")
    crime_tree.heading("CrimeID", text="Crime ID")
    crime_tree.heading("Type", text="Type")
    crime_tree.heading("Date", text="Date")
    crime_tree.heading("Location", text="Location")
    crime_tree.bind('<<TreeviewSelect>>', on_crime_select)
    crime_tree.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

    # Buttons on the left side
    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=0, column=0, rowspan=3, sticky="ns", padx=10, pady=10)

    add_button = ctk.CTkButton(button_frame, text="Add Crime", command=add_crime)
    add_button.pack(pady=5)

    update_button = ctk.CTkButton(button_frame, text="Update Crime", command=update_crime)
    update_button.pack(pady=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete Crime", command=delete_crime)
    delete_button.pack(pady=5)

    view_details_button = ctk.CTkButton(button_frame, text="View Details", command=view_case_details)
    view_details_button.pack(pady=5)

    # Input Fields below the table
    input_frame = ctk.CTkFrame(root)
    input_frame.grid(row=2, column=1, sticky="ew", padx=10, pady=10)

    ctk.CTkLabel(input_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
    type_entry = ctk.CTkEntry(input_frame)
    type_entry.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(input_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5)
    date_entry = ctk.CTkEntry(input_frame)
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    ctk.CTkLabel(input_frame, text="Location:").grid(row=2, column=0, padx=5, pady=5)
    location_entry = ctk.CTkEntry(input_frame)
    location_entry.grid(row=2, column=1, padx=5, pady=5)

    populate_treeview()
    root.mainloop()

if __name__ == '__main__':
    main()
