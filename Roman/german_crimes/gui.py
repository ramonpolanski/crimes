import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql

# Database connection details
user = 'postgres'
password = 'password'
host = 'localhost'
port = '5432'
dbname = 'your_database'
table_name = 'your_table_name'

# Connect to the database and load data
def load_data():
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
    df = pd.read_sql_table(table_name, engine)
    return df

def save_data(df):
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)

# Create main application window
class CRUDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CRUD Application")
        self.geometry("800x600")

        self.df = load_data()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Create and pack the widgets
        self.filter_label = tk.Label(self, text="Filter by:")
        self.filter_label.pack(pady=5)

        self.filter_entry = tk.Entry(self)
        self.filter_entry.pack(pady=5)

        self.filter_button = tk.Button(self, text="Apply Filter", command=self.apply_filter)
        self.filter_button.pack(pady=5)

        self.tree = ttk.Treeview(self, columns=self.df.columns.tolist(), show='headings')
        self.tree.pack(expand=True, fill=tk.BOTH, pady=5)

        # Scrollbars
        self.scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.scroll_x.pack(side='bottom', fill='x')

        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scroll_y.pack(side='right', fill='y')

        self.tree.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Add headings to the treeview
        for col in self.df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Buttons for CRUD operations
        self.add_button = tk.Button(self, text="Add", command=self.add_record)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self, text="Edit", command=self.edit_record)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_record)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.load_data_into_tree()

    def load_data_into_tree(self):
        # Clear the existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert data into the treeview
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def apply_filter(self):
        filter_text = self.filter_entry.get()
        if not filter_text:
            messagebox.showwarning("Input Error", "Please enter a filter text.")
            return

        filtered_df = self.df[self.df.apply(lambda row: row.astype(str).str.contains(filter_text, case=False).any(), axis=1)]
        
        if filtered_df.empty:
            messagebox.showinfo("No Results", "No records match the filter.")
        else:
            self.df = filtered_df
            self.load_data_into_tree()

    def add_record(self):
        AddEditDialog(self, "Add")

    def edit_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to edit.")
            return
        
        selected_values = self.tree.item(selected_item[0], 'values')
        selected_index = self.tree.index(selected_item[0])

        # Pass the selected values to the dialog
        AddEditDialog(self, "Edit", selected_values, selected_index)

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        
        selected_index = self.tree.index(selected_item[0])
        self.df = self.df.drop(self.df.index[selected_index])
        self.load_data_into_tree()
        save_data(self.df)
        messagebox.showinfo("Success", "Record deleted successfully.")

class AddEditDialog(tk.Toplevel):
    def __init__(self, parent, mode, values=None, index=None):
        super().__init__(parent)
        self.title(f"{mode} Record")
        self.geometry("400x300")
        self.parent = parent
        self.mode = mode
        self.values = values
        self.index = index
        
        self.entries = []
        
        # Create labels and entries for each column
        for col in parent.df.columns:
            tk.Label(self, text=col).pack(pady=5)
            entry = tk.Entry(self)
            entry.pack(pady=5)
            self.entries.append(entry)
            
            if values:
                entry.insert(0, values[parent.df.columns.get_loc(col)])
        
        self.save_button = tk.Button(self, text="Save", command=self.save)
        self.save_button.pack(pady=20)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(pady=5)

    def save(self):
        values = [entry.get() for entry in self.entries]
        
        if self.mode == "Add":
            new_row = pd.Series(values, index=self.parent.df.columns)
            self.parent.df = self.parent.df.append(new_row, ignore_index=True)
        
        elif self.mode == "Edit":
            self.parent.df.iloc[self.index] = values
        
        self.parent.load_data_into_tree()
        save_data(self.parent.df)
        self.destroy()
        messagebox.showinfo("Success", f"Record {self.mode.lower()}ed successfully.")

if __name__ == "__main__":
    app = CRUDApp()
    app.mainloop()
