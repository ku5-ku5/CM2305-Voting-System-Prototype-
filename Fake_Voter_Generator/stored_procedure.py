import mysql.connector
import datetime


pwd = 'PASSWORD'

votedb = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    auth_plugin='mysql_native_password',
    passwd=pwd
)

fn = "results.xml"

try:
    f = open(fn, 'r')
except IOError:
    f = open(fn, 'w')

try:
    cursor = votedb.cursor()
    query = ("""
    SELECT count(pp.name), pp.Name FROM votedb.vote v 
    INNER JOIN votedb.political_party pp
    ON v.PoliticalPartyID = pp.UId
    GROUP BY pp.name;
    """)
    number_of_rows = cursor.execute(query)
    f.write("<?xml version=\"1.0\"?>\n")
    f.write("<dataset>\n")
    result = cursor.fetchall()
    for row in result:
        f.write("  <Party>\n")
        f.write("    <Party_Name>" + row[1] + "</Party_Name>\n")
        f.write("    <Votes>" + str(row[0]) + "</Votes>\n")
        f.write("  </Party>\n")
    f.write("</dataset>\n")
    

except mysql.connector.Error as er:
    print(er)
