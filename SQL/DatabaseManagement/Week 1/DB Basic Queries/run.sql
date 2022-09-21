SELECT snum, firstname, lastname, phone, city, st FROM Student WHERE city='Newark' AND st='DE';

SELECT snum, firstname, lastname, gpa FROM Student WHERE gpa > 3.0;

SELECT snum, firstname, lastname, phone, st FROM Student WHERE st='NY' OR st='PA';

SELECT firstname, lastname, street, city, st, zip, gender, major FROM Student WHERE gender='F' AND major='CIS';

SELECT snum, firstname, lastname, phone, zip, scholarship FROM Student WHERE zip='19341' AND scholarship = TRUE;