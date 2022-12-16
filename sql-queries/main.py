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

    
    def update_pbdata(self, st_case, eventnum,):
        with dbapi2.connect(self.dbfile) as connection:
            pass


mydb = Database('pbtable.db')
# mydb.getByPrimKey(430219,0,1)
print(mydb.getPedestrians())