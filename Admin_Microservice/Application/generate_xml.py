import mysql.connector
from datetime import date

class Filename():
    def __init__(self):
        super().__init__()

    def make_filename(self):
        return "results-" + str(date.today()) + ".xml"

    def add_path(self):
        return "C:\\repos\\CM2305-Voting-System-Prototype-\\Results\\" + make_filename()

class Generate_xml():
    def __init__(self, file_name, pwd):
        self.file_name = file_name
        self.pwd = 'PASSWORD'
            
    def connect_to_database(self):

        votedb = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3306,
            auth_plugin='mysql_native_password',
            passwd=self.pwd
        )

        return votedb

    def check_if_contains(self):

        with open(file_name, 'r') as read_file:
            contains_item = read_file.read(1)
            
            #returns false if file is empty
            if not contains_item:
                return False
        return True


    def create_xml(self):

        if check_if_contains(file_name):
            open(file_name).close()

        else:
            try:
                f = open(file_name, 'r')
            except IOError:
                f = open(file_name, 'w')

        votedb = connect_to_database()
        
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
