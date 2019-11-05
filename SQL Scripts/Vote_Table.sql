CREATE TABLE Vote(
  UId CHAR(38), 
  VoteID int IDENTITY(1,1), 
  PoliticalPartyID CHAR(38) NOT NULL, 
  VoteStatus BINARY(1) DEFAULT 0, 
  PRIMARY KEY (UId), 
  FOREIGN KEY (PoliticalPartyID) REFERENCES PoliticalParty(PartyID) 
); 