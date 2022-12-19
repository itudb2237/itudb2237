import csv
import pandas as pd
import sqlite3 as dbapi2
import os
from valueMapsVehAux import ValueMappings, HeadMappings

columns_csv = ['ST_CASE', 'VEH_NO']+ [k for k in HeadMappings]
revMap = {v: k for k,v in HeadMappings.items()}

class CSVtoDb:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def accessMap(self, column, data):
        try:
            return data[revMap[column]]
        except:
            print(revMap[column], data[revMap[column]])
            print(ValueMappings[column][data[revMap[column]]])
            return "yo"
    def add_vehAuxData_fromCSV(self, data):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO VEHICLE_AUX (CASE_NUMBER, VEHICLE_NUMBER, VEHICLE_BODY_TYPE, MOTORCYCLE_LICENSE_STATUS, SCHOOL_BUS, SPEEDING_VEHICLE, ROLLOVER) VALUES(?,?,?,?,?,?,?)"""
            values = (int(data["ST_CASE"]), int(data["VEH_NO"]), self.accessMap("VEHICLE_BODY_TYPE", data), self.accessMap("MOTORCYCLE_LICENSE_STATUS", data), self.accessMap("SCHOOL_BUS", data), self.accessMap("SPEEDING_VEHICLE", data), self.accessMap("ROLLOVER", data))
            cursor.execute(query, values)
            connection.commit()
            pbkey = cursor.lastrowid

        return pbkey

def createAndFillVehicleAuxillaryTable():
    
    file = 'database.db'
    
    db = CSVtoDb(file)

    connection = dbapi2.connect(file)
    
    # Creating a cursor object to execute
    # SQL queries on a database table
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS VEHICLE_AUX")

    # Table Definition
    create_table = """CREATE TABLE VEHICLE_AUX(
    CASE_NUMBER INTEGER NOT NULL,
    VEHICLE_NUMBER INTEGER NOT NULL,
    VEHICLE_BODY_TYPE CHAR(70)  NULL,
    MOTORCYCLE_LICENSE_STATUS CHAR(70) NULL,
    SCHOOL_BUS CHAR(70) NULL,
    SPEEDING_VEHICLE CHAR(70) NULL,
    ROLLOVER CHAR(70) NULL,

    PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER),\n"""

    check_cols = []
    for col in check_cols:
        create_table += "CHECK ( "+col
        create_table += " == '" + f"' OR {col} == '".join([i for i in set(ValueMappings[col].values())])+"'),\n"
    
    create_table = create_table[:-2] + ")\n"
    # create sql table
    cursor.execute(create_table)

    # csv file content to pandas data frame
    df = pd.read_csv(".\TableConverters\VEH_AUX.csv")
    content = df[columns_csv]
    attribute_number = len(content.columns)
    tuple_number = len(content) 

    # add table rows of data frame
    for i in range(tuple_number):
        db.add_vehAuxData_fromCSV(content.iloc[i, :])

    # selection query
    select_all = "SELECT * FROM VEHICLE_AUX"
    rows = cursor.execute(select_all).fetchall()
    
    # Output to the console screen
    for r in rows:
        print(r)
    
    # Committing the changes
    connection.commit()
    
    # closing the database connection
    connection.close()  
