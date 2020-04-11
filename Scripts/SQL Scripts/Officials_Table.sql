CREATE TABLE Officials(
  OfficialUId CHAR(38),
  FirstName CHAR(50),
  Surname CHAR(50),
  Email VARCHAR(255) NOT NULL,
  PwdHash VARCHAR(255),
  IsAdmin TINYINT(1) DEFAULT 0,
  PRIMARY KEY (OfficialUId)
);
