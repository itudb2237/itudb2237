import csv
import pandas as pd
import sqlite3 as dbapi2
import os
from valueMaps import ValueMappings, HeadMappings
i = 0
class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def accessMap(self, column, data):
        return ValueMappings[HeadMappings[column]][data[column]]
        
    def add_pbdata_fromCSV(self, data):
        global i
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            # print(HeadMappings["PBPTYPE"])
            # print(ValueMappings[HeadMappings["PBPTYPE"]][data["PBPTYPE"]])
            query = """INSERT INTO PBTYPE (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER, PERSON_TYPE, CROSSWALK_PRESENT, SIDEWALK_PRESENT, SCHOOLZONE_PRESENT, MOTOR_MANEUVER) VALUES(?,?,?,?,?,?,?,?)"""
            values = (int(data["ST_CASE"]), int(data["VEH_NO"]), int(data["PER_NO"]), self.accessMap("PBPTYPE", data), self.accessMap("PBCWALK", data), self.accessMap("PBSWALK", data), self.accessMap("PBSZONE", data), self.accessMap("MOTMAN", data))
            cursor.execute(query, values)
            connection.commit()
            pbkey = cursor.lastrowid

            query = "SELECT"
        return pbkey


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

# bool types
boolConditions = ""
boolTypes = ["CROSSWALK_PRESENT","SIDEWALK_PRESENT","SCHOOLZONE_PRESENT"]
for btyp in boolTypes:
    boolConditions += "CHECK (" + btyp + " == \"None Noted\" OR "+ btyp +" == \"Yes\" OR "+ btyp +" == \"Unknown\"),\n"

# Table Definition
create_table = """CREATE TABLE IF NOT EXISTS PBTYPE(
CASE_NUMBER INTEGER NOT NULL,
VEHICLE_NUMBER INTEGER NOT NULL,
PERSON_NUMBER INTEGER NOT NULL,
PERSON_TYPE CHAR(70) NULL,
CROSSWALK_PRESENT CHAR(70) NULL,
SIDEWALK_PRESENT CHAR(70) NULL,
SCHOOLZONE_PRESENT CHAR(70) NULL,
MOTOR_MANEUVER CHAR(70) NULL,

PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER),\n"""
create_table += boolConditions
create_table += "CHECK (MOTOR_MANEUVER == \""+"\" OR MOTOR_MANEUVER == \"".join([i for i in set(ValueMappings["MOTOR_MANEUVER"].values())])+"\"))"
print(create_table)
# create sql table
cursor.execute(create_table)

# csv file content to pandas data frame
df = pd.read_csv("FARS2015PuertoRicoCSV_pbtype.csv")
content = df[['ST_CASE', 'VEH_NO', 'PER_NO', 'PBPTYPE', 'PBCWALK', 'PBSWALK', 'PBSZONE', 'MOTMAN']]
attribute_number = len(content.columns)
tuple_number = len(content) 

# add table rows of data frame
for i in range(tuple_number):
    db.add_pbdata_fromCSV(content.iloc[i, :])

# selection query
# id = "\"Not a Pedestrian\" ORDER BY PERSON_NUMBER DESC"
select_all = "SELECT * FROM PBTYPE"
rows = cursor.execute(select_all).fetchall()
 
# Output to the console screen
for r in rows:
    print(r)
 
# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()