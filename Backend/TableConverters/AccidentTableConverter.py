import csv
import pandas as pd
import sqlite3 as dbapi2
import os
from TableConverters.valueMapsAccident import ValueMappings, HeadMappings

class CSVtoDb:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def accessMap(self, column, data):
        return ValueMappings[HeadMappings[column]][data[column]]
        
    def getGeoData(self, val):
        if int(val) > 360:
            return "NULL"
        return int(val)
    def add_accidentData_fromCSV(self, data):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO ACCIDENT (STATE, CASE_NUMBER, N_PEOPLE_IN_VEHICLES, YEAR, USED_LAND, LATITUDE, LONGITUDE) VALUES(?,?,?,?,?,?,?)"""
            values = (self.accessMap("STATE", data), int(data["ST_CASE"]), int(data["PERMVIT"]), int(data["YEAR"]), self.accessMap("RUR_URB", data), self.getGeoData(data["LATITUDE"]), self.getGeoData(data["LONGITUD"]))
            cursor.execute(query, values)
            connection.commit()
            pbkey = cursor.lastrowid

        return pbkey

def createAndFillAccidentTable():
    
    file = 'database.db'
    
    db = CSVtoDb(file)

    connection = dbapi2.connect(file)
    
    # Creating a cursor object to execute
    # SQL queries on a database table
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS ACCIDENT")
    
    create_table = """CREATE TABLE ACCIDENT(
    STATE CHAR(70) NULL,
    CASE_NUMBER INTEGER NOT NULL,
    N_PEOPLE_IN_VEHICLES INTEGER NULL,
    YEAR INTEGER NULL,
    USED_LAND CHAR(70) NULL,
    LATITUDE INTEGER NULL,
    LONGITUDE INTEGER NULL,

    PRIMARY KEY (CASE_NUMBER),\n"""

    create_table += "CHECK (STATE == \""+"\" OR STATE == \"".join([i for i in set(ValueMappings["STATE"].values())])+"\"),\n"
    create_table += "CHECK (USED_LAND == \""+"\" OR USED_LAND == \"".join([i for i in set(ValueMappings["USED_LAND"].values())])+"\"))"

    # print(create_table)
    # create sql table
    cursor.execute(create_table)

    # csv file content to pandas data frame
    df = pd.read_csv("./TableConverters/accident.csv")
    content = df[['STATE', 'ST_CASE', 'PERMVIT', 'YEAR', 'RUR_URB', 'LATITUDE', 'LONGITUD']]
    attribute_number = len(content.columns)
    tuple_number = len(content) 

    # add table rows of data frame
    for i in range(tuple_number):
        db.add_accidentData_fromCSV(content.iloc[i, :])

    # selection query
    # id = "\"Not a Pedestrian\" ORDER BY PERSON_NUMBER DESC"
    select_all = "SELECT * FROM ACCIDENT"
    rows = cursor.execute(select_all).fetchall()
    
    # Output to the console screen
    # for r in rows:
    #     print(r)
    
    # Committing the changes
    connection.commit()
    
    # closing the database connection
    connection.close()  
