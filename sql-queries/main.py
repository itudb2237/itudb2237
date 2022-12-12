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
    
    def update_pbdata(self, st_case, eventnum,):
        with dbapi2.connect(self.dbfile) as connection:
            pass
