CREATE TABLE Vote(
  UId CHAR(38),
  ElectionID int NOT NULL,
  PoliticalPartyID CHAR(38) NOT NULL,
  VoteTimestamp DATETIME NOT NULL,
  PRIMARY KEY (UId),
  FOREIGN KEY (PoliticalPartyID) REFERENCES PoliticalParty(PartyID)
);
