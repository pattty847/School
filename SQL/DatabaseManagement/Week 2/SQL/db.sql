DROP DATABASE IF EXISTS PhoneDB;
CREATE DATABASE PhoneDB;
USE PhoneDB;

DROP TABLE IF EXISTS PHONE;
CREATE TABLE Phone(
ID           VARCHAR(5)not null,
Manu         VARCHAR(40),
ModelNum     VARCHAR(20),
ModelName    VARCHAR(25), /* Metadata says size of 2, maybe meant 20/25? */
Description  VARCHAR(400),
Memory       VARCHAR(10),
Height       DOUBLE,
Width        DOUBLE,
Provider     VARCHAR(20),
Price        DOUBLE,
Rating       DOUBLE,
OperSys      VARCHAR(20),
SmartPhone   BOOLEAN,
CONSTRAINT Phone_PK PRIMARY KEY (ID)
) engine = innodb;
 
/*
Insert Statements
*/
INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00001","Apple","A1660","iPhone 7","4.7” LED-backlit widescreen, 1334x750, 326 ppi",256,5.44,2.64,"AT&T",849,4,"iOS",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00002","Apple","A1661","iPhone 7+","5.5” LED-backlit widescreen, 1920x1080, 401 ppi",256,6.23,3.07,"AT&T",969,4.5,"iOS",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00003","Samsung","SM-G950T","Galaxy S8","5.8” Quad HD+ Super AMOLED, 2960x1440, 570 ppi",64,5.86,2.68,"T-Mobile",750,4.5,"Android",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00004","Samsung","SM-G955T","Galaxy S8+","6.2” Quad HD+ Super AMOLED, 2960x1440, 529 ppi",64,6.28,2.89,"T-Mobile",850,4.5,"Android",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00005","Motorola","XT1685","Moto G5+","5.2” 2.0 GHz Qcta-Core, 1080x1920, 401 ppi",64,6.02,3.02,"Verizon",299,4,"Android",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00006","Motorola","MOTXT1650","Moto Z Droid","5.5” AMOLED, 1440p Quad HD, 2560x1440, 535 ppi",64,6.04,2.96,"Verizon",499,4,"Android",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00007","Nokia","RM-1018","Lumia 530","4” 1.2 GHz Qualcomm Snapdragon, 854x480, 246 ppi",4,4.7,2.45,"Cellular One",49.99,3.5,"Windows",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00008","Nokia","3310","Nokia 3310(2017)","2.4”, 240x320, 167 ppi",0.016,4.55,2.01,"Cellular One",52,3.4,"Nokia Series 30+",FALSE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00009","Blackberry","STV100-1","Blackberry Priv","5.4” Quad HD AMOLED, 2560x1440, 540 ppi",32,5.78,3.04,"Sprint",699,3.5,"Android",TRUE);

INSERT INTO Phone (ID, Manu, ModelNum, ModelName, Description, Memory, Height, Width, Provider, Price, Rating, OperSys, SmartPhone)
VALUES("00010","Alcatel","IDOL4SGOLD","Idol 4S","5.5” AMOLED, 1920x1080, 401 ppi",64,6.1,3,"Sprint",432,4,"Windows",TRUE);

