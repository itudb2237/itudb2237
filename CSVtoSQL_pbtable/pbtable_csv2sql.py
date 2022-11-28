# Import required modules
import csv
import pandas as pd
import sqlite3 as dbapi2
import os

class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def add_pbdata(self, data):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PBTYPE (crash_id, veichle_no, person_no, person_typ, pbcwalk, pbswalk, pbszone, motman) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            
            # since all attributes are integer
            tup = tuple(int(col) for col in data)
            cursor.execute(query, tup)
            connection.commit()
            movie_key = cursor.lastrowid
        return movie_key


file = 'pbtable.db'
try:
    os.remove(file)
except OSError:
    pass
# Connecting to the geeks database
db = Database(file)

# Connecting to the geeks database
connection = dbapi2.connect(file)
 
# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()
 
# Table Definition
create_table = '''CREATE TABLE PBTYPE(
                crash_id INTEGER NOT NULL,
                veichle_no INTEGER NOT NULL,
                person_no INTEGER NOT NULL,
                person_typ INTEGER,
                pbcwalk INTEGER,
                pbswalk INTEGER,
                pbszone INTEGER,
                motman INTEGER
                );
                '''
# create sql table
cursor.execute(create_table)

# csv file content to pandas data frame
df = pd.read_csv("FARS2015NationalCSV_pbtype.csv")
content = df[['ST_CASE', 'VEH_NO', 'PER_NO', 'PBPTYPE', 'PBCWALK', 'PBSWALK', 'PBSZONE', 'MOTMAN']]
attribute_number = len(content.columns)
tuple_number = len(content) 

# add table rows of data frame
for i in range(tuple_number):
    db.add_pbdata(content.iloc[i, :])

# selection query
select_all = "SELECT * FROM PBTYPE"
rows = cursor.execute(select_all).fetchall()
 
# Output to the console screen
for r in rows:
    print(r)
 
# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()