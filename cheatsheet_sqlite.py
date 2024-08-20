import sqlite3, os

# 1. Create a Database (creating a new or connecting to an existing database)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# 2. Create Two Tables (creating two tables employees and departments)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
)
''')

input("Tables created, lets add some data.")

# 3. Insert Data into Tables (inserting some data into created tables)
cursor.execute('''
INSERT INTO Departments (dept_name) VALUES ('IT Department')
''')

cursor.execute('''
INSERT INTO Departments (dept_name) VALUES ('HR Department')
''')

cursor.execute('''
INSERT INTO Employees (name, role, dept_id) VALUES ('John Doe', 'Python Teacher', 1)
''')

cursor.execute('''
INSERT INTO Employees (name, role, dept_id) VALUES ('Jane Smith', 'Java Teacher', 1)
''')

# Commit the inserts
conn.commit()

input("Data added, very nice. Lets see...")

# 4. Retrieving data from the database (get all there is from Employees)
print("All Employees:")
cursor.execute('SELECT * FROM Employees')
for row in cursor.fetchall():
    print(row)

input("Very nice. Okay lets see more...")

# 5. Retrieving specific and linked data from the database
print("\nIT Department and its Employees:")
cursor.execute('''
SELECT Departments.dept_name, Employees.name 
FROM Departments
JOIN Employees ON Departments.dept_id = Employees.dept_id
WHERE Departments.dept_name = 'IT Department'
''')
for row in cursor.fetchall():
    print(row)

input("nice. nice. lets do some changes")

# 6. Update data (update some data in both tables)
cursor.execute('''
UPDATE Employees
SET role = 'Senior Python Teacher'
WHERE name = 'John Doe'
''')

cursor.execute('''
UPDATE Departments
SET dept_name = 'Tech Department'
WHERE dept_name = 'IT Department'
''')

conn.commit()

input("changes done. now lets throw everything out the windows (or the ubuntus, badum tss)")

# 7. Deleting data (wiping both tables clean)
cursor.execute('DELETE FROM Employees')
cursor.execute('DELETE FROM Departments')

conn.commit()

input("tables wiped clean.")

# 8. Deleting tables (dropping both tables)
cursor.execute('DROP TABLE IF EXISTS Employees')
cursor.execute('DROP TABLE IF EXISTS Departments')

input("tables dropped/deleted")

# 9. Deleting the database (close connection and delete the database file)
conn.close()
input("press ENTER to remove database...") # you probably need more than this input() to actually see whats going on

os.remove('my_database.db')

print("DONE DONE DONE")
