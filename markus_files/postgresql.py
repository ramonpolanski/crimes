import psycopg2
import os

# 1. Create a Database Connection 
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="password",
    host="localhost",
    port="5432")
conn.autocommit = True # this one is False by default

cursor = conn.cursor()

# 2. Create Two Tables (creating two tables employees and departments)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL
)
''')  # commit not needed, CREATE TABLE gets executed directly

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
)
''')  # commit not needed, CREATE TABLE gets executed directly

input("Tables created, let's add some data.")

# 3. Insert Data into Tables (inserting some data into created tables)
cursor.execute('''
INSERT INTO Departments (dept_name) VALUES ('IT Department')
''')  # commit not needed, INSERT gets executed directly

cursor.execute('''
INSERT INTO Departments (dept_name) VALUES ('HR Department')
''')  # commit not needed, INSERT gets executed directly

cursor.execute('''
INSERT INTO Employees (name, role, dept_id) VALUES ('John Doe', 'Python Teacher', 1)
''')  # commit not needed, INSERT gets executed directly

cursor.execute('''
INSERT INTO Employees (name, role, dept_id) VALUES ('Jane Smith', 'Java Teacher', 1)
''')  # commit not needed, INSERT gets executed directly

# Commit the inserts
# conn.commit()  # Commented out due to autocommit

input("Data added, very nice. Let's see...")

# 4. Retrieving data from the database (get all there is from Employees)
print("All Employees:")
cursor.execute('SELECT * FROM Employees')  # commit not needed, SELECT gets executed directly
for row in cursor.fetchall():
    print(row)

input("Very nice. Okay, let's see more...")

# 5. Retrieving specific and linked data from the database
print("\nIT Department and its Employees:")
cursor.execute('''
SELECT Departments.dept_name, Employees.name 
FROM Departments
JOIN Employees ON Departments.dept_id = Employees.dept_id
WHERE Departments.dept_name = 'IT Department'
''')  # commit not needed, SELECT JOIN gets executed directly
for row in cursor.fetchall():
    print(row)

input("Nice, nice. Let's do some changes")

# 6. Update data (update some data in both tables)
cursor.execute('''
UPDATE Employees
SET role = 'Senior Python Teacher'
WHERE name = 'John Doe'
''')  # commit not needed, UPDATE gets executed directly

cursor.execute('''
UPDATE Departments
SET dept_name = 'Tech Department'
WHERE dept_name = 'IT Department'
''')  # commit not needed, UPDATE gets executed directly

# conn.commit()  # Commented out due to autocommit

input("Changes done. Now let's throw everything out...")

# 7. Deleting data (wiping both tables clean)
cursor.execute('DELETE FROM Employees')  # commit not needed, DELETE gets executed directly
cursor.execute('DELETE FROM Departments')  # commit not needed, DELETE gets executed directly

# conn.commit()  # Commented out due to autocommit

input("Tables wiped clean.")

# 8. Deleting tables (dropping both tables)
cursor.execute('DROP TABLE IF EXISTS Employees')  # commit not needed, DROP TABLE gets executed directly
cursor.execute('DROP TABLE IF EXISTS Departments')  # commit not needed, DROP TABLE gets executed directly

input("Tables dropped/deleted")

# 9. Closing the connection (no need to delete the database file for PostgreSQL)
conn.close()

print("DONE DONE DONE")
