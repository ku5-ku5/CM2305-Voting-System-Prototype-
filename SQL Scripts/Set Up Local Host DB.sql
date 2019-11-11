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
  VoteStatus TINYINT(1) DEFAULT 0,
  VoteTimestamp DATETIME NOT NULL,
  PRIMARY KEY (VoteId),
  FOREIGN KEY (PoliticalPartyID) REFERENCES PoliticalParty(UId)
);
users

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
(UUID(),
'Labour');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
(UUID(),
'Conservative');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
(UUID(),
'UKIP');
INSERT INTO `votedb`.`politicalparty`
(`UId`,
`Name`)
VALUES
(UUID(),
'Green Party');
