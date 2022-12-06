import sqlite3
import pandas as pd


column_names = ["ST_CASE", "VEH_NO", "NUMOCCS", "HIT_RUN", "OWNER", "MAKE", "MOD_YEAR"]
df = pd.read_csv('FARS2015NationalCSV_vehicle.csv', encoding='windows-1252').loc[:,column_names]

connection = sqlite3.connect('Vehicle.sql')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Vehicle(
	st_case INTEGER NOT NULL,
	veh_no INTEGER NOT NULL,
	numoccs INTEGER NOT NULL,
	hit_run INTEGER NOT NULL,
	owner INTEGER NOT NULL,
	make INTEGER NOT NULL,
	mod_year INTEGER NOT NULL,

	PRIMARY KEY(st_case, veh_no)
)""")

for i in range(len(df)):
	row = [int(df.iloc[i][0]), int(df.iloc[i][1]), int(df.iloc[i][2]), int(df.iloc[i][3]), int(df.iloc[i][4]), int(df.iloc[i][5]), int(df.iloc[i][6])]
	cursor.execute("""INSERT INTO Vehicle VALUES (?,?,?,?,?,?,?)""", row)

connection.commit()
connection.close()




