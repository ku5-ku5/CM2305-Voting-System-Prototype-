#Before using this on your personal system run the below command
#   pip install Faker
#   pip install mysql-connector-python

from faker import Faker
import mysql.connector
import random

#add your username and password to your own local account below
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="INSERT_PASSWORD",
  database="votedb"
)
mycursor = mydb.cursor()

#adds the instance of the Faker module
fake = Faker()

sql = "INSERT INTO `votedb`.`users` (`UserUId`,`EligibleToVote`,`Email`,`PwdHash`,`IsOfficial`,`HasVoted`)VALUES (UUID(), 0, %s, %s, 0, 0);"

i=0
while i <= 100:
    i += 1

    hash = random.getrandbits(128)
    val = (fake.email(), hash)
    mycursor.execute(sql, val)

    mydb.commit()
    print(str(i) + " record inserted, Email and Hash:" + str(val))
