SELECT 1 = 1 OR 1 / 0;

SELECT true OR false AND false;

SELECT (true OR false) AND false; 

SELECT customername, country FROM customers WHERE country='USA' OR country='France';

SELECT customername, country, creditlimit FROM customers WHERE (country='USA' or country='France') AND creditlimit > 100000;

SELECT customername, country, creditlimit FROM customers WHERE country='USA' or country='France' AND creditlimit > 10000;
