 DROP DATABASE IF EXISTS  StudentTableTest;
 CREATE DATABASE StudentTableTest; 
 USE StudentTableTest;

CREATE TABLE Student
(
snum CHAR (6),

firstname VARCHAR (15), 

lastname VARCHAR (25), 

street VARCHAR (25),

city VARCHAR (15), 

st CHAR (2),

zip CHAR (5), 

phone CHAR (10), 

major VARCHAR (20),

gpa DOUBLE,

gender ENUM ('F','M'),

scholarship BOOLEAN, 

CONSTRAINT STUDENT_PK PRIMARY KEY (snum) );

 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship) VALUES ('100000', 'Joe', 'Cooper', '01 Main', 'Phila', 'PA',
'19122', '2154445555', 'Comp Science', '3.6', 'M', False);

INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship) 
VALUES ('J11233', 'Mauris', 'Cholaro', '63 Woodland', 'Phila', 'PA', '19142', '2671295460', 'Accounting', '2.9', 'M', TRUE);

INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('J85147', 'Michael', 'Bentt', '22 Le Bronx', 'New York', 'NY', '19801', '6105290071', 'Business Admin', '4.0', 'M', TRUE);

INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('A78126', 'Jasmine', 'Davenport', '50 Olney', 'Phila', 'PA', '19101', '2670297300', 'Art', '3.0', 'F', False);

 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z61403', 'Kwame', 'Traylor', '37 Have Hill', 'Conshohoken', 'PA', '19341', '2157308912', 'Biology', '3.3', 'F', TRUE);

 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z45503', 'Stephanie', 'Cowdery', '45 Bule Lane', 'Newark', 'DE', '18677', '3025678944', 'Law', '3.3', 'F', TRUE);

 INSERT INTO Student (snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64551', 'Peter', 'Congo', '501 Washington Lane', 'Newark', 'DE', '18677', '3025677844', 'Construction', '3.7', 'M', False);

 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64589', 'Celestein', 'Dawson', '456 Flatbush Ave', 'New York', 'NY', '56789', '2125677711', 'Computer Science', '3.4', 'F', False);

 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64584', 'Bruce', 'Wiley', '4334 N. 16 Steet', 'Phila', 'PA', '19020', '2156572134', 'Computer Science', '2.4', 'M', False);

 INSERT INTO Student (snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64595', 'Keith', 'Johnson', '5712 Commerce Street', 'Camden', 'NJ', '34567', '6092344567', 'Liberal Arts', '1.4', 'M', False);

 INSERT INTO Student (snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64585', 'Jennifer', 'Thompson', '202 Park Avenue', 'New Castle', 'DE',
'87933', '6092344567', 'CIS', '3.5', 'F', True);
 
 INSERT INTO Student
(snum, firstname, lastname, street, city, st, zip,  phone, major, gpa, gender, scholarship)
 VALUES ('Z64590', 'James', 'Smith', '1721 JFK Bulivard', 'Phila', 'PA', '19120', '2157553478', 'CIS', '3.0', 'M', False);

 