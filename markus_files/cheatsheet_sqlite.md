# SQLITE CHEAT SHEET (CLI)
##########################
1. Create a Database
(creating a new or connecting to an existing database)

```bash
sqlite3 my_database.db
```

BUT if started only with:

```bash
sqlite3
```

then you need to do
```bash
.open my_database.db
```

Otherwise a in-memory database will be used which
is stored in RAM - all will be lost on session end.

##########################
2. Create Two Tables
(creating two tables employees and departments)

```bash
CREATE TABLE Employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    dept_id INTEGER,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL
);

```
Here we created two tables which are linked via a foreign key in Employees. 
Every employee is connected to a department. 

You could fetch a department and all its linked employees.

##########################
3. Insert Data into Tables
(inserting some data into created tables)

```bash
INSERT INTO Departments (dept_name) VALUES ('IT Department');
INSERT INTO Departments (dept_name) VALUES ('HR Department');

INSERT INTO Employees (name, role, dept_id) VALUES ('John Doe', 'Python Teacher', 1);
INSERT INTO Employees (name, role, dept_id) VALUES ('Jane Smith', 'Java Teacher', 1);
```

Populating the database.

##########################
4. Retrieving data from the database
(get all there is from Employees)

```bash
SELECT * FROM Employees;
```

##########################
5.  Retrieving specific and linked data from the database
(get info about one department and all its linked employees)

```bash
SELECT Departments.dept_name, Employees.name 
FROM Departments
JOIN Employees ON Departments.dept_id = Employees.dept_id
WHERE Departments.dept_name = 'IT Department';
```
The WHERE statement is optional.

##########################
6. Update data
(update some data in both tables)

```bash
UPDATE Employees
SET role = 'Senior Python Teacher'
WHERE name = 'John Doe';

UPDATE Departments
SET dept_name = 'Tech Department'
WHERE dept_name = 'IT Department';
```
##########################
7. Deleting data
(wiping both tables clean)

```bash
DELETE FROM Departments;

DELETE FROM Employees;
```

##########################
8. Deleting tables
(dropping both tables)

```bash
DROP TABLE Departments;

DROP TABLE Employees;
```

##########################
9. Deleting the database

```bash
.quit

rm my_database.db
```

As Sqlite works with a local database file - you need to remove that for deletion.

Thats good for small apps that don't have much data. You can move the file wherever you need it or just delete it as shown.

# DONE DONE DONE