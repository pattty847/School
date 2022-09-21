DROP DATABASE IF EXISTS  HouseTableTest;
CREATE DATABASE HouseTableTest;
USE HouseTableTest;
CREATE TABLE House
(
	ID VARCHAR(
	6)
	,
	STREET VARCHAR(
	40)
	,
	CITY VARCHAR(
	20)
	,
	STATE CHAR(
	2)
	,
	ZIP CHAR(
	5)
	,
	BEDROOMS NUMERIC (
	2,
	1)
	,
	BATHROOMS NUMERIC (
	2,
	1)
	,
	VALUE NUMERIC ,

	FIRST VARCHAR(
	20)
	,
	LAST VARCHAR(
	20)
	,
	SOLD BOOLEAN,
	CONSTRAINT PKHOUSE PRIMARY KEY(
	ID)
)
;
INSERT INTO House
VALUES(
		'10002' ,
		'207 BALDWIN ST' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19127' ,
		'3' ,
		'1.5' ,
		'585000' ,
		'ELIJAH' ,
		'CHANDLER' ,
		'1' )
;
INSERT INTO House
VALUES(
		'10001' ,
		'200 GREEN LN ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19127' ,
		'3' ,
		'1.5' ,
		'572000' ,
		'COLIN' ,
		'MCKINNEY' ,
		'0' )
;
INSERT INTO House
VALUES(
		'10009' ,
		'406 LEVERINGTON AVE ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'3' ,
		'1.5' ,
		'572000' ,
		'NEVADA' ,
		'MCCORMICK' ,
		'0' )
;
INSERT INTO House
VALUES(
		'10003' ,
		'207 DUPONT ST' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19154' ,
		'4' ,
		'2' ,
		'507000' ,
		'CLEMENTINE' ,
		'HOLLOWAY' ,
		'1' )
;
INSERT INTO House
VALUES(
		'10005' ,
		'236 PARKER AVE' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'4' ,
		'2' ,
		'491400' ,
		'EMMANUEL' ,
		'SHARPE' ,
		'1' )
;
INSERT INTO House
VALUES(
		'10004' ,
		'217 N 11TH ST ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'2' ,
		'1' ,
		'390000' ,
		'SUSAN' ,
		'TERRY' ,
		'0' )
;
INSERT INTO House
VALUES(
		'10006' ,
		'246 N 3RD ST ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19106' ,
		'1' ,
		'1.5' ,
		'390000' ,
		'JULIET' ,
		'ONEAL' ,
		'0' )
;
INSERT INTO House
VALUES(
		'10008' ,
		'365 HERMITAGE ST' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'2' ,
		'1' ,
		'362700' ,
		'MONA' ,
		'FRANK' ,
		'0' )
;
INSERT INTO House
VALUES(
		'10000' ,
		'121 NANDINA ST' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19116' ,
		'2' ,
		'1.5' ,
		'227500' ,
		'VINCENT' ,
		'COMPTON' ,
		'1' )
;
INSERT INTO House
VALUES(
		'10007' ,
		'346 GREEN LN ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'2' ,
		'2' ,
		'146640' ,
		'MIRANDA' ,
		'MCINTOSH' ,
		'1' )
;



INSERT INTO House
VALUES(
		'10015' ,
		'1914 Fairmount Avenue ' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19139' ,
		'3' ,
		'3' ,
		'300640' ,
		'Mark' ,
		'Jones' ,
		'1' )
;


INSERT INTO House
VALUES(
		'10016' ,
		'2022 Spring Garden' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19139' ,
		'3' ,
		'2' ,
		'251000' ,
		'Mark' ,
		'Jones' ,
		'1' )
;



INSERT INTO House
VALUES(
		'10044' ,
		'1503 Green Street' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19139' ,
		'2' ,
		'2' ,
		'249000' ,
		'Mark' ,
		'Jones' ,
		'0' )
;


INSERT INTO House
VALUES(
		'10055' ,
		'5720 Bell Street' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19140' ,
		'4' ,
		'2' ,
		'207000' ,
		'CLEMENTINE' ,
		'HOLLOWAY' ,
		'1' )
;

INSERT INTO House
VALUES(
		'10075' ,
		'1755 Miller Avenue' ,
		' PHILADELPHIA' ,
		'PA' ,
		'19128' ,
		'4' ,
		'2' ,
		'491400' ,
		'EMMANUEL' ,
		'SHARPE' ,
		'0' )
	;
	
	