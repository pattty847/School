DROP DATABASE IF EXISTS  house;
CREATE DATABASE house;
USE house;

CREATE TABLE house
(
    ID VARCHAR(6), 
    STREET VARCHAR(40), 
    CITY VARCHAR(20), 
    STATE CHAR(2), 
    ZIP CHAR(5),
    BEDROOMS NUMERIC (2,1),
    BATHROOMS NUMERIC (2,1),
    VALUE NUMERIC,
    FIRST VARCHAR(20),
    LAST VARCHAR(20),
    SOLD BOOLEAN,
    CONSTRAINT PKHOUSE PRIMARY KEY(ID)
);

INSERT INTO house
VALUES(
        '10002' ,
        '207 BALDWIN ST' ,
        'PHILADELPHIA' ,
        'PA' ,
        '19127' ,
        '3' ,
        '1.5' ,
        '585000' ,
        'ELIJAH' ,
        'CHANDLER' ,
        '1' );

INSERT INTO house
VALUES(
        '10001' ,
        '200 GREEN LN ' ,
        'PHILADELPHIA' ,
        'PA' ,
        '19127' ,
        '3' ,
        '1.5' ,
        '572000' ,
        'COLIN' ,
        'MCKINNEY' ,
        '0' );

INSERT INTO house
VALUES(
    '10003',
    '4000 Gypsy Lane',
    'PHIADELPHIA',
    'PA',
    '19129',
    '3',
    '2',
    '178000',
    'PAT',
    'THOMAS',
    '0');