CREATE TABLE Users(
  UserUId CHAR(38),
  EligibleToVote TINYINT(1) DEFAULT 0,
  Email VARCHAR(255) NOT NULL,
  PwdHash VARCHAR(255),
  HasVoted TINYINT(1) DEFAULT 0,
  otp_secret varchar(16),
  PRIMARY KEY (UserUId)
);
