
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk
from Sunny.sunnytestfile import create_db, search_and_display

def add_crime(tree):
    """
    Opens a window to add a new crime entry to the database.
    """
    def submit():
        crime_type = entry_type.get()
        crime_date = entry_date.get()
        crime_location = entry_location.get()

        if crime_type and crime_date and crime_location:
            query = '''
                INSERT INTO Crimes (Type, Date, Location) 
                VALUES (%s, %s, %s)
            '''
            search_and_display(query, (crime_type, crime_date, crime_location))
            populate_treeview(tree)
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")

    # Create a new window for adding a crime
    add_window = ctk.CTkToplevel()
    add_window.title("Add Crime")

    ctk.CTkLabel(add_window, text="Crime Type:").pack(pady=5)
    entry_type = ctk.CTkEntry(add_window)
    entry_type.pack(pady=5)

    ctk.CTkLabel(add_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    entry_date = ctk.CTkEntry(add_window)
    entry_date.pack(pady=5)

    ctk.CTkLabel(add_window, text="Location:").pack(pady=5)
    entry_location = ctk.CTkEntry(add_window)
    entry_location.pack(pady=5)

    submit_btn = ctk.CTkButton(add_window, text="Submit", command=submit)
    submit_btn.pack(pady=10)

def update_crime(tree):
    """
    Opens a window to update an existing crime entry.
    """
    selected = tree.focus()  # Get the selected item from the TreeView
    if not selected:
        messagebox.showerror("Error", "Please select a crime to update.")
        return

    values = tree.item(selected, 'values')  # Get the values of the selected item

    def submit():
        crime_id = values[0]
        crime_type = entry_type.get()
        crime_date = entry_date.get()
        crime_location = entry_location.get()

        if crime_type and crime_date and crime_location:
            query = '''
                UPDATE Crimes 
                SET Type = %s, Date = %s, Location = %s 
                WHERE CrimeID = %s
            '''
            search_and_display(query, (crime_type, crime_date, crime_location, crime_id))
            populate_treeview(tree)
            update_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")

    update_window = ctk.CTkToplevel()
    update_window.title("Update Crime")

    ctk.CTkLabel(update_window, text="Crime Type:").pack(pady=5)
    entry_type = ctk.CTkEntry(update_window)
    entry_type.insert(0, values[1])  # Insert current value into the entry field
    entry_type.pack(pady=5)

    ctk.CTkLabel(update_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    entry_date = ctk.CTkEntry(update_window)
    entry_date.insert(0, values[2])
    entry_date.pack(pady=5)

    ctk.CTkLabel(update_window, text="Location:").pack(pady=5)
    entry_location = ctk.CTkEntry(update_window)
    entry_location.insert(0, values[3])
    entry_location.pack(pady=5)

    submit_btn = ctk.CTkButton(update_window, text="Submit", command=submit)
    submit_btn.pack(pady=10)

def delete_crime(tree):
    """
    Deletes the selected crime entry from the database.
    """
    selected = tree.focus()  # Get the selected item from the TreeView
    if not selected:
        messagebox.showerror("Error", "Please select a crime to delete.")
        return

    values = tree.item(selected, 'values')  # Get the values of the selected item

    crime_id = values[0]

    query = 'DELETE FROM Crimes WHERE CrimeID = %s'
    search_and_display(query, (crime_id,))
    populate_treeview(tree)

def populate_treeview(tree):
    """
    Fetches and displays crime data in the TreeView widget.
    """
    for row in tree.get_children():
        tree.delete(row)

    query = 'SELECT * FROM Crimes'
    crimes = search_and_display(query, ())  # Pass empty tuple for no parameters

    for crime in crimes:
        tree.insert("", "end", values=crime)

def main():
    """
    Main entry point for the GUI application.
    """
    create_db()  # Ensure database is created and populated

    root = ctk.CTk()
    root.title("Crime Investigation Database")

    # Create a TreeView to display the crime data
    tree_frame = ctk.CTkFrame(root)
    tree_frame.pack(pady=10)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Type", "Date", "Location"), show="headings", height=8)
    tree.heading("ID", text="ID")
    tree.heading("Type", text="Type")
    tree.heading("Date", text="Date")
    tree.heading("Location", text="Location")
    tree.pack()

    # Populate the TreeView with data from the database
    populate_treeview(tree)

    # Create buttons for Add, Update, and Delete operations
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=10)

    add_btn = ctk.CTkButton(button_frame, text="Add Crime", command=lambda: add_crime(tree))
    add_btn.pack(side="left", padx=10)

    update_btn = ctk.CTkButton(button_frame, text="Update Crime", command=lambda: update_crime(tree))
    update_btn.pack(side="left", padx=10)

    delete_btn = ctk.CTkButton(button_frame, text="Delete Crime", command=lambda: delete_crime(tree))
    delete_btn.pack(side="left", padx=10)

    root.mainloop()

if __name__ == '__main__':
    main()
