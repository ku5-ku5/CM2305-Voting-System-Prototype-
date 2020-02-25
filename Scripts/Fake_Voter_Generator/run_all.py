from faker import Faker
import mysql.connector
import random
import datetime
import time

pwd = 'PASSWORD'

votedb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port=3306,
    auth_plugin='mysql_native_password',
    passwd=pwd
)


def create_database():

    cursor = votedb.cursor()
    try:
        cursor.execute("CREATE DATABASE votedb")
        print("VoteDB created")
    except mysql.connector.Error as er:
        print(er)

    cursor.close()

def create_tables():
    dbcursor = votedb.cursor()

    dbcursor.execute("SHOW DATABASES")
    dbs = []
    for i in dbcursor:
        str = ""
        for char in i:
            if char.isalpha():
                str += char

        dbs.append(str)

    if 'votedb' in dbs:

        table_cursor = votedb.cursor()

        table_cursor.execute("USE votedb;")

        try:
            table_cursor.execute("CREATE TABLE `Political_Party` ( UId CHAR(38) NOT NULL UNIQUE,Name VARCHAR(255) NOT NULL,PRIMARY KEY (UId));")
            print("PoliticalParty table created")
        except mysql.connector.Error as err:
            print("Failed to create the PoliticalParty table")
            print(err)

        try:
            table_cursor.execute("CREATE TABLE `Vote` (VoteId CHAR(38) NOT NULL UNIQUE,PoliticalPartyID CHAR(38) NOT NULL,/**VoteStatus TINYINT(1) DEFAULT 0,**/VoteTimestamp DATETIME NOT NULL,PRIMARY KEY (VoteId),FOREIGN KEY (PoliticalPartyID) REFERENCES Political_Party(UId));")
            print("Vote table created")
        except mysql.connector.Error as err:
            print("Failed to create the Vote table")
            print(err)

        try:
            table_cursor.execute("CREATE TABLE `Users` (UserUId CHAR(38) NOT NULL UNIQUE,EligibleToVote TINYINT(1) DEFAULT 0,Email VARCHAR(255) NOT NULL UNIQUE,PwdHash VARCHAR(255),HasVoted TINYINT(1) DEFAULT 0,PRIMARY KEY (UserUId));")
            print("Users table created")
        except mysql.connector.Error as err:
            print("Failed to create users table")
            print(err)

        try:
            table_cursor.execute("CREATE TABLE `Officials` (OfficialUId CHAR(38) NOT NULL UNIQUE,FirstName VARCHAR(50) NOT NULL, Surname VARCHAR(50) NOT NULL,Email VARCHAR(255) NOT NULL UNIQUE,PwdHash VARCHAR(255),IsAdmin TINYINT(1) DEFAULT 0,PRIMARY KEY (OfficialUId));")
        except mysql.connector.Error as err:
            print("Failed to create officials table")
            print(err)

        table_cursor.close()
    else:
        print("Database not created :/ Script stopped")

    dbcursor.close()

def parties():
    party_cursor = votedb.cursor()

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('c5a60d73-ffe0-11e9-8f05-1831bf97a796','Labour');")
        print("Labour party added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('c5a7721d-ffe0-11e9-8f05-1831bf97a796','Conservative');")
        print("Conservatives added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('29478d29-0489-11ea-be81-1831bf97a796','DUP');")
        print("DUP added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('2948f383-0489-11ea-be81-1831bf97a796','SNP');")
        print("SNP added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('294980dc-0489-11ea-be81-1831bf97a796','Plaid Cymru');")
        print("Plaid Cymru added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('c5aae837-ffe0-11e9-8f05-1831bf97a796','Green Party');")
        print("Green Party added")
    except mysql.connector.Error as err:
        print(err)

    try:
        party_cursor.execute("INSERT INTO `votedb`.`political_party`(`UId`,`Name`)VALUES('c5a8f70d-ffe0-11e9-8f05-1831bf97a796','UKIP');")
        print("UKIP added")
    except mysql.connector.Error as err:
        print(err)

    party_cursor.close()

def remove_duplicates(x):
    return list(dict.fromkeys(x))

def fake_voters():
    mycursor = votedb.cursor()

    #adds the instance of the Faker module
    fake = Faker()

    sql = "INSERT INTO `votedb`.`users` (`UserUId`,`EligibleToVote`,`Email`,`PwdHash`,`HasVoted`)VALUES (UUID(), 0, %s, %s, 0);"

    emails_raw = []

    while len(emails_raw) < 100:

        emails_raw.append(fake.email())

    emails = remove_duplicates(emails_raw)

    d = 0
    for i in emails:

        hash = random.getrandbits(128)
        val = (emails[d], hash)
        mycursor.execute(sql, val)

        d+=1

        votedb.commit()
        if d == 1:
            print(str(d) + " record inserted, Email and Hash:" + str(val))
        else:
            print(str(d) + " records inserted, Email and Hash:" + str(val))

    mycursor.close()

def fake_vote():
    cursor = votedb.cursor()

    sql = "INSERT INTO `votedb`.`vote` (`VoteId`,`PoliticalPartyID`,`VoteTimestamp`)VALUES (UUID(), %s, %s);"

    party_array = ['c5a60d73-ffe0-11e9-8f05-1831bf97a796', 'c5a7721d-ffe0-11e9-8f05-1831bf97a796', 'c5a8f70d-ffe0-11e9-8f05-1831bf97a796', 'c5aae837-ffe0-11e9-8f05-1831bf97a796', '294980dc-0489-11ea-be81-1831bf97a796', '2948f383-0489-11ea-be81-1831bf97a796', '29478d29-0489-11ea-be81-1831bf97a796' ]


    i=0
    while i < 100:
        i += 1

        date = datetime.datetime.now()

        val = (random.choice(party_array), date)
        cursor.execute(sql, val)

        votedb.commit()
        if i == 1:
            print(str(i) + " record inserted, PartyUId and date:" + str(val))
        else:
            print(str(i) + " records inserted, PartyUId and date:" + str(val))
        #script will sleep for 5 seconds so that all the data isnt at the same time however can be commented out
        #time.sleep(5)
    cursor.close()

def add_admin():
    cursor = votedb.cursor()

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Rhys', 'Connor', 'rhys@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Rhys admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Jake', 'Casey', 'jakec@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Jake C admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Martha', 'Heron', 'martha@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Martha admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Sophie', 'Hunt', 'sophie@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Sophie admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Markus', 'Hutchby', 'markus@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Markus admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Tomos', 'Williams', 'tomos@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Tomos admin added')
    except mysql.connector.Error as err:
        print(err)

    try:
        cursor.execute("INSERT INTO `votedb`.`officials` (`OfficialUId`,`FirstName`,`Surname`, `email`, `PwdHash`)VALUES (UUID(), 'Jake', 'Ziegler', 'jakez@mail.net', 'e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a');")
        print('Jake Z admin added')
    except mysql.connector.Error as err:
        print(err)

    cursor.close()

#The below will run the functions

#Create statements
#create_database()
create_tables()
#Insert statements that populate the data
parties()
fake_voters()
fake_vote()
add_admin()

votedb.close()
