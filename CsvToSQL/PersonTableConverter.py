import csv
import sqlite3

db = sqlite3.connect("person.db")

person = csv.DictReader(open("person.csv"))

cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS PERSON (
    CASE_NUMBER INTEGER NOT NULL,
    VEHICLE_NUMBER INTEGER NOT NULL,
    PERSON_NUMBER INTEGER NOT NULL,
    AGE INTEGER NOT NULL,
    SEX INTEGER NULL,
    PERSON_TYPE INTEGER NULL,
    INJURY_SEVERITY INTEGER NULL,
    SEATING_POSITION INTEGER NULL,

    PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER)
)""")

#CHECK (SEX == \"FEMALE\" OR SEX == \"MALE\")

for i in person:
    cursor.execute(f"""INSERT INTO PERSON (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER, AGE, SEX, PERSON_TYPE, INJURY_SEVERITY, SEATING_POSITION) VALUES
     ({i["ST_CASE"]}, {i["VEH_NO"]}, {i["PER_NO"]}, {i["AGE"]}, {i["SEX"]}, {i["PER_TYP"]}, {i["INJ_SEV"]}, {i["SEAT_POS"]})""")

db.commit()

db.close()