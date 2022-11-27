-- Patrick McDermott MYSQLTUTORIAL.ORG INSERT STATEMENT
-- 2022-10-29
-- CIS 205 Database Management

-- First we will create the database
CREATE DATABASE SampleDB;

-- Switch to the created database
USE SampleDB;

-- Drop the table 'tasks' if it exists
DROP TABLE IF EXISTS tasks;

-- Create the new table with the attributes from the tutorial
CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT, -- Primary key =
    title VARCHAR(255) NOT NULL, -- Cannot be null
    start_date DATE, -- Can be null
    due_date DATE, -- Can be null
    priority TINYINT NOT NULL DEFAULT 3, -- Cannot be null
    description TEXT, -- Can be null
    PRIMARY KEY (task_id)
);

-- We will enter a row into the 'tasks' table letting the DB use nulls for the missing data
INSERT INTO tasks(title, priority)
VALUES("Learn MySql Insert Statement", 1);
SELECT * FROM tasks;

-- Next enter data into the 'tasks' table using the DEFAULT keyword
INSERT INTO tasks(title,priority)
VALUES('Understanding DEFAULT keyword in INSERT statement', DEFAULT);
SELECT * FROM tasks;

-- Now we enter date formats into the table
INSERT INTO tasks(title, start_date, due_date)
VALUES("Insert Date into Table", "2022-10-29", "2022-10-29");
SELECT * FROM tasks;

-- This is the same data formats entered but using functions to get the current date
INSERT INTO tasks(title,start_date,due_date)
VALUES('Use current date for the task',CURRENT_DATE(),CURRENT_DATE());
SELECT * FROM tasks;

-- This is an example of a multi row insert
INSERT INTO tasks(title, priority)
VALUES
	('My first task', 1),
	('It is the second task',2),
	('This is the third task of the week',3);
SELECT * FROM tasks;