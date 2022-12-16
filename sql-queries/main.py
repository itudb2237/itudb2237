import csv
import pandas as pd
import sqlite3 as dbapi2
import os


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def add_pbdata(self, data):
        with dbapi2.connect(self.dbfile) as connection:
            pass

    def getByPrimKey(self, caseNum, perNum, vehNum):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            s = (caseNum,perNum,vehNum)

            return cursor.execute("SELECT * FROM PBTYPE WHERE CASE_NUMBER = ? AND VEHICLE_NUMBER = ? AND PERSON_NUMBER = ?", s).fetchall()[0]

    
    def getPedestrians(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT * FROM PBTYPE WHERE PERSON_TYPE = \"Pedestrian\"").fetchall()


    def getBikers(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            return cursor.execute("SELECT * FROM PBTYPE WHERE PERSON_TYPE = \"Bicyclist\"").fetchall()

    def getFilteredTable(self, formInput): # formInput is a dictionary, keys are columns, values are lists
        statement = "SELECT "
        
        prevKey = ""
        for key in formInput.keys():
            if prevKey != "":
                statement += prevKey + ", "
            prevKey = key
        statement += prevKey + " FROM PBTYPE WHERE "

        last_key = list(formInput)[-1]
        for key in formInput.keys():
            if formInput[key] == None or len(formInput[key]) == 0:
                statement += "( " + key + " IS NULL)" 
            
            else:
                last_value = formInput[key][-1]
                statement += "("
                prevValue = ""
                for value in formInput[key]:
                    statement += key + " == \"" + value + "\""
                    if value != last_value:
                        statement += " OR "
                statement += ")"
            if key != last_key:
                statement += " AND "
        
        print(statement)
        return statement

    def update_pbdata(self, st_case, eventnum,):
        with dbapi2.connect(self.dbfile) as connection:
            pass


mydb = Database('pbtable.db')
# mydb.getByPrimKey(430219,0,1)
print(mydb.getPedestrians())
formInput = {
"CASE_NUMBER": [],
"VEHICLE_NUMBER": [],
"PERSON_NUMBER": [],
"PERSON_TYPE": ["Pedesterian"],
"CROSSWALK_PRESENT": ["Yes", "None"],
"SIDEWALK_PRESENT": ["None"],
"SCHOOLZONE_PRESENT": ["Yes", "None"],
"MOTOR_MANEUVER": ["Right"],
}
mydb.getFilteredTable(formInput)