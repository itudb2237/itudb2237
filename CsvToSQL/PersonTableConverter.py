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
    SEX CHAR(6) NULL,
    PERSON_TYPE INTEGER NULL,
    INJURY_SEVERITY INTEGER NULL,
    SEATING_POSITION INTEGER NULL,

    PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER)
    CHECK (SEX == \"FEMALE\" OR SEX == \"MALE\" OR SEX == NULL)
)""")

for i in person:
    i["SEX"] = {"1": "\"MALE\"", "2": "\"FEMALE\"", "8": "\"NULL\"", "9": "NULL"}[i["SEX"]]

    # INJ_SEV
    # 0 No Injury (O)
    # 1 Possible Injury (C)
    # 2 Suspected Minor Injury (B)
    # 3 Suspected Serious Injury (A)
    # 4 Fatal Injury (K)
    # 5 Injured, Severity Unknown (U) (Since 1978)
    # 6 Died Prior to Crash
    # 8 Not Reported (2010 Only)
    # 9 Unknown
    #
    # SEAT_POS
    # 0 Not a Motor Vehicle Occupant (2005-Later)
    # 11 Front Seat – Left Side (Driver’s Side)
    # 12 Front Seat – Middle
    # 13 Front Seat – Right Side
    # 18 Front Seat – Other
    # 19 Front Seat – Unknown
    # 21 Second Seat – Left Side
    # 22 Second Seat – Middle
    # 23 Second Seat – Right Side
    # 28 Second Seat – Other
    # 29 Second Seat – Unknown
    # 31 Third Seat – Left Side
    # 32 Third Seat – Middle
    # 33 Third Seat – Right Side
    # 38 Third Seat – Other
    # 39 Third Seat – Unknown
    # 41 Fourth Seat – Left Side
    # 42 Fourth Seat – Middle
    # 43 Fourth Seat – Right Side
    # 48 Fourth Seat – Other
    # 49 Fourth Seat – Unknown
    # 50 Sleeper Section of Cab (Truck)
    # 51 Other Passenger in Enclosed Passenger or Cargo Area [Includes Passengers in 5th Row of 15-Seat, 5-Row Vans] [Includes Injured Full-Size-Bus Occupants] (2002-2008)
    # 51 Other Passenger in Enclosed Passenger or Cargo Area (Since 2009)
    # 52 Other Passenger in Unenclosed Passenger or Cargo Area
    # 53 Other Passenger in Passenger or Cargo Area, Unknown Whether or Not Enclosed
    # 54 Trailing Unit
    # 55 Riding on Vehicle Exterior
    # 56 Appended to a Motor Vehicle for Motion

    cursor.execute(f"""INSERT INTO PERSON (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER, AGE, SEX, PERSON_TYPE, INJURY_SEVERITY, SEATING_POSITION) VALUES
     ({i["ST_CASE"]}, {i["VEH_NO"]}, {i["PER_NO"]}, {i["AGE"]}, {i["SEX"]}, {i["PER_TYP"]}, {i["INJ_SEV"]}, {i["SEAT_POS"]})""")

db.commit()

db.close()