SELECT lastname FROM employees;

SELECT lastname, firstname, jobtitle FROM employees;

SELECT * FROM employees;

SELECT lastname, firstname, jobtitle FROM employees WHERE jobtitle='Sales Rep';

SELECT lastname, firstname, jobtitle FROM employees WHERE jobtitle='Sales Rep' AND officeCode=1;

SELECT lastname, firstname, reportsTo FROM employees WHERE reportsTo IS NULL;

SELECT lastname, firstname, jobtitle FROM employees WHERE jobtitle <> 'Sales Rep';

SELECT lastname, firstname, officecode FROM employees WHERE officecode > 5;

SELECT lastname, firstname, officecode FROM employees WHERE officecode <= 4;