import csv
import sqlite3

connection = sqlite3.connect('blg317e.db')
cursor = connection.cursor()

statement0 = '''DROP TABLE Cevent'''
cursor.execute(statement0)

statement = '''CREATE TABLE Cevent(
                state INTEGER,
				st_case INTEGER,    
				eventnum INTEGER,
				vnumber1 INTEGER,
                aoi1 INTEGER,
                soe INTEGER,
                vnumber2 INTEGER,
                aoi2 INTEGER,
                CONSTRAINT PK_Cevent PRIMARY KEY (st_case, eventnum)
                );
				'''  

# later st_case should be foreign key referencing Accident table

cursor.execute(statement)

file = open('Cevent.csv')
spreadsheet = csv.reader(file)
insert_records = "INSERT INTO Cevent VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

cursor.executemany(insert_records, spreadsheet)

statement2 = '''ALTER TABLE Cevent DROP COLUMN state'''
cursor.execute(statement2)

tuples = cursor.execute("SELECT * FROM Cevent").fetchall()

for i in tuples:
	print(i)

connection.commit()
connection.close()
