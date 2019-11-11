import mysql.connector
import random
import datetime
import time

#add your username and password to your own local account below
votedb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="INSERT_PASSWORD",
  database="votedb"
)
mycursor = votedb.cursor()

sql = "INSERT INTO `votedb`.`vote` (`VoteId`,`PoliticalPartyID`,`VoteTimestamp`)VALUES (UUID(), %s, %s);"

party_array = ['c5a60d73-ffe0-11e9-8f05-1831bf97a796', 'c5a7721d-ffe0-11e9-8f05-1831bf97a796', 'c5a8f70d-ffe0-11e9-8f05-1831bf97a796', 'c5aae837-ffe0-11e9-8f05-1831bf97a796', '294980dc-0489-11ea-be81-1831bf97a796', '2948f383-0489-11ea-be81-1831bf97a796', '29478d29-0489-11ea-be81-1831bf97a796' ]


i=0
while i < 100:
    i += 1

    date = datetime.datetime.now()

    val = (random.choice(party_array), date)
    mycursor.execute(sql, val)

    votedb.commit()
    if i == 1:
        print(str(i) + " record inserted, PartyUId and date:" + str(val))
    else:
        print(str(i) + " records inserted, PartyUId and date:" + str(val))
    #script will sleep for 5 seconds so that all the data isnt at the same time however can be commented out
    time.sleep(5)
