CREATE DATABASE VoteDB;

USE VoteDB;

CREATE TABLE PoliticalParty(
 UId CHAR(38) NOT NULL UNIQUE,
 Name VARCHAR(255) NOT NULL,
 PRIMARY KEY (UId)
);

CREATE TABLE Vote(
  VoteId CHAR(38) NOT NULL UNIQUE,
  PoliticalPartyID CHAR(38) NOT NULL,
  /**VoteStatus TINYINT(1) DEFAULT 0,**/
  VoteTimestamp DATETIME NOT NULL,
  PRIMARY KEY (VoteId),
  FOREIGN KEY (PoliticalPartyID) REFERENCES PoliticalParty(UId)
);


CREATE TABLE Users(
  UserUId CHAR(38) NOT NULL UNIQUE,
  EligibleToVote TINYINT(1) DEFAULT 0,
  Email VARCHAR(255) NOT NULL UNIQUE,
  PwdHash VARCHAR(255),
  HasVoted TINYINT(1) DEFAULT 0,
  IsOfficial TINYINT(1) DEFAULT 0,
  PRIMARY KEY (UserUId)
);


INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('c5a60d73-ffe0-11e9-8f05-1831bf97a796',
'Labour');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('c5a7721d-ffe0-11e9-8f05-1831bf97a796',
'Conservative');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('c5a8f70d-ffe0-11e9-8f05-1831bf97a796',
'UKIP');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('c5aae837-ffe0-11e9-8f05-1831bf97a796',
'Green Party');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('29478d29-0489-11ea-be81-1831bf97a796',
'DUP');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('2948f383-0489-11ea-be81-1831bf97a796',
'SNP');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
('294980dc-0489-11ea-be81-1831bf97a796',
'Plaid Cymru');
