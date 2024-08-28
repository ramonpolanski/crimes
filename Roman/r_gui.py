import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
import datetime

# Database Connection Function
def connect_to_db():
    return psycopg2.connect(dbname='crime_investigation', user='postgres', password='password', host='localhost', port='5432')

# Main Application Window
class CrimeInvestigationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crime Investigation Database")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Crime Investigation Database", font=("Arial", 18)).pack(pady=20)
        
        tk.Button(self, text="Add Entry", command=self.add_entry).pack(pady=10)
        tk.Button(self, text="Edit Entry", command=self.edit_entry).pack(pady=10)
        tk.Button(self, text="Delete Entry", command=self.delete_entry).pack(pady=10)
        tk.Button(self, text="Search Entry", command=self.search_entry).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=10)

    def add_entry(self):
        AddEntryWindow(self)

    def edit_entry(self):
        EditEntryWindow(self)

    def delete_entry(self):
        DeleteEntryWindow(self)

    def search_entry(self):
        SearchEntryWindow(self)

# Add Entry Window
class AddEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Entry")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Crime Type:").pack(pady=5)
        self.crime_type = tk.Entry(self)
        self.crime_type.pack(pady=5)

        tk.Label(self, text="Crime Date (YYYY-MM-DD):").pack(pady=5)
        self.crime_date = tk.Entry(self)
        self.crime_date.pack(pady=5)

        tk.Label(self, text="Location:").pack(pady=5)
        self.location = tk.Entry(self)
        self.location.pack(pady=5)

        tk.Label(self, text="Evidence Type:").pack(pady=5)
        self.evidence_type = tk.Entry(self)
        self.evidence_type.pack(pady=5)

        tk.Label(self, text="Evidence Description:").pack(pady=5)
        self.evidence_description = tk.Entry(self)
        self.evidence_description.pack(pady=5)

        tk.Label(self, text="Officer Name:").pack(pady=5)
        self.officer_name = tk.Entry(self)
        self.officer_name.pack(pady=5)

        tk.Label(self, text="Officer Rank:").pack(pady=5)
        self.officer_rank = tk.Entry(self)
        self.officer_rank.pack(pady=5)

        tk.Label(self, text="Officer Department:").pack(pady=5)
        self.officer_department = tk.Entry(self)
        self.officer_department.pack(pady=5)

        tk.Label(self, text="Suspect Name:").pack(pady=5)
        self.suspect_name = tk.Entry(self)
        self.suspect_name.pack(pady=5)

        tk.Label(self, text="Suspect Age:").pack(pady=5)
        self.suspect_age = tk.Entry(self)
        self.suspect_age.pack(pady=5)

        tk.Label(self, text="Suspect Description:").pack(pady=5)
        self.suspect_description = tk.Entry(self)
        self.suspect_description.pack(pady=5)

        tk.Button(self, text="Add", command=self.add_entry_to_db).pack(pady=20)

    def add_entry_to_db(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO Crimes (Type, Date, Location) 
        VALUES (%s, %s, %s) RETURNING CrimeID;
        ''', (self.crime_type.get(), self.crime_date.get(), self.location.get()))
        crime_id = cursor.fetchone()[0]

        cursor.execute('''
        INSERT INTO Evidence (Type, Description, CrimeID) 
        VALUES (%s, %s, %s);
        ''', (self.evidence_type.get(), self.evidence_description.get(), crime_id))

        cursor.execute('''
        INSERT INTO Officers (Name, Rank, Department, CrimeID) 
        VALUES (%s, %s, %s, %s);
        ''', (self.officer_name.get(), self.officer_rank.get(), self.officer_department.get(), crime_id))

        cursor.execute('''
        INSERT INTO Suspects (Name, Age, Description, CrimeID) 
        VALUES (%s, %s, %s, %s);
        ''', (self.suspect_name.get(), self.suspect_age.get(), self.suspect_description.get(), crime_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Entry added successfully")
        self.destroy()

# Edit Entry Window
class EditEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Edit Entry")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Crime ID to Edit:").pack(pady=5)
        self.crime_id = tk.Entry(self)
        self.crime_id.pack(pady=5)

        tk.Label(self, text="New Crime Type:").pack(pady=5)
        self.new_crime_type = tk.Entry(self)
        self.new_crime_type.pack(pady=5)

        tk.Label(self, text="New Crime Date (YYYY-MM-DD):").pack(pady=5)
        self.new_crime_date = tk.Entry(self)
        self.new_crime_date.pack(pady=5)

        tk.Label(self, text="New Location:").pack(pady=5)
        self.new_location = tk.Entry(self)
        self.new_location.pack(pady=5)

        tk.Button(self, text="Update", command=self.edit_entry_in_db).pack(pady=20)

    def edit_entry_in_db(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE Crimes 
        SET Type = %s, Date = %s, Location = %s 
        WHERE CrimeID = %s;
        ''', (self.new_crime_type.get(), self.new_crime_date.get(), self.new_location.get(), self.crime_id.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Entry updated successfully")
        self.destroy()

# Delete Entry Window
class DeleteEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Delete Entry")
        self.geometry("400x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Crime ID to Delete:").pack(pady=20)
        self.crime_id = tk.Entry(self)
        self.crime_id.pack(pady=20)

        tk.Button(self, text="Delete", command=self.delete_entry_in_db).pack(pady=20)

    def delete_entry_in_db(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Crimes WHERE CrimeID = %s', (self.crime_id.get(),))
        crime = cursor.fetchone()

        if not crime:
            messagebox.showerror("Error", "Crime not found")
            return

        cursor.execute('DELETE FROM Crimes WHERE CrimeID = %s;', (self.crime_id.get(),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Entry deleted successfully")
        self.destroy()

# Search Entry Window
class SearchEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Search Entry")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Search by Crime ID").pack(pady=5)
        self.case_id = tk.Entry(self)
        self.case_id.pack(pady=5)
        tk.Button(self, text="Search", command=self.search_by_case_id).pack(pady=5)

        tk.Label(self, text="Search by Crime Type").pack(pady=5)
        self.crime_type = tk.Entry(self)
        self.crime_type.pack(pady=5)
        tk.Button(self, text="Search", command=self.search_by_crime_type).pack(pady=5)

    def search_by_case_id(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Crimes WHERE CrimeID = %s', (self.case_id.get(),))
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Result", f"Crime ID: {result[0]}\nType: {result[1]}\nDate: {result[2]}\nLocation: {result[3]}")
        else:
            messagebox.showerror("Error", "No matching entry found")

    def search_by_crime_type(self):
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Crimes WHERE Type = %s', (self.crime_type.get(),))
        results = cursor.fetchall()
        conn.close()

        if results:
            result_text = "\n".join([f"Crime ID: {r[0]}, Type: {r[1]}, Date: {r[2]}, Location: {r[3]}" for r in results])
            messagebox.showinfo("Results", result_text)
        else:
            messagebox.showerror("Error", "No matching entries found")

# Running the Application
if __name__ == "__main__":
    app = CrimeInvestigationApp()
    app.mainloop()
