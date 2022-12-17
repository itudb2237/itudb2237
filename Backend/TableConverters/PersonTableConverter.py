import csv
import sqlite3

ValueMappings = {"SEX": {"1": "\"MALE\"",
                             "2": "\"FEMALE\"",
                             "8": "NULL",
                             "9": "NULL"
                             },
                     "INJ_SEV": {
                         "0": "\"No Injury\"",
                         "1": "\"Possible Injury\"",
                         "2": "\"Suspected Minor Injury\"",
                         "3": "\"Suspected Serious Injury\"",
                         "4": "\"Fatal Injury\"",
                         "5": "\"Injured, Severity Unknown\"",
                         "6": "\"Died Prior to Crash\"",
                         "8": "NULL",
                         "9": "NULL"
                     },
                     "SEAT_POS": {
                         "0": "\"Not a Motor Vehicle Occupant\"",
                         "11": "\"Front Seat – Left Side (Driver’s Side)\"",
                         "12": "\"Front Seat – Middle\"",
                         "13": "\"Front Seat – Right Side\"",
                         "18": "\"Front Seat – Other\"",
                         "19": "\"Front Seat – Unknown\"",
                         "21": "\"Second Seat – Left Side\"",
                         "22": "\"Second Seat – Middle\"",
                         "23": "\"Second Seat – Right Side\"",
                         "28": "\"Second Seat – Other\"",
                         "29": "\"Second Seat – Unknown\"",
                         "31": "\"Third Seat – Left Side\"",
                         "32": "\"Third Seat – Middle\"",
                         "33": "\"Third Seat – Right Side\"",
                         "38": "\"Third Seat – Other\"",
                         "39": "\"Third Seat – Unknown\"",
                         "41": "\"Fourth Seat – Left Side\"",
                         "42": "\"Fourth Seat – Middle\"",
                         "43": "\"Fourth Seat – Right Side\"",
                         "48": "\"Fourth Seat – Other\"",
                         "49": "\"Fourth Seat – Unknown\"",
                         "50": "\"Sleeper Section of Cab (Truck)\"",
                         "51": "\"Other Passenger in Enclosed Passenger or Cargo Area ",
                         "51": "\"Other Passenger in Enclosed Passenger or Cargo Area\"",
                         "52": "\"Other Passenger in Unenclosed Passenger or Cargo Area\"",
                         "53": "\"Other Passenger in Passenger or Cargo Area, Unknown Whether or Not Enclosed\"",
                         "54": "\"Trailing Unit\"",
                         "55": "\"Riding on Vehicle Exterior\"",
                         "56": "\"Appended to a Motor Vehicle for Motion\"",
                         "98": "NULL",
                         "99": "NULL"
                     },
                     "PER_TYP": {
                         "1": "\"Driver of a Motor Vehicle in Transport\"",
                         "2": "\"Passenger of a Motor Vehicle in Transport\"",
                         "3": "\"Occupant of a Motor Vehicle Not in Transport\"",
                         "4": "\"Occupant of a Non-Motor Vehicle Transport Device\"",
                         "5": "\"Pedestrian\"",
                         "6": "\"Bicyclist\"",
                         "7": "\"Other Cyclist\"",
                         "8": "\"Other Pedestrian (Includes Persons on Personal Conveyances)\"",
                         "8": "\"Person on Personal Conveyances\"",
                         "9": "\"Unknown Occupant Type in a Motor Vehicle in Transport\"",
                         "10": "\"Persons in/on Buildings\"",
                         "11": "\"Person on Motorized Personal Conveyance\"",
                         "12": "\"Person on Non-Motorized Personal Conveyance\"",
                         "13": "\"Person on Personal Conveyance, Unknown if Motorized or Non-Motorized\"",
                         "19": "\"Unknown Type of Non-Motorist\"",
                         "88": "NULL",
                         "99": "NULL"
                     }
                     }

def createAndFillPeopleTable(dbpath):
    person = csv.DictReader(open("./TableConverters/person.csv"))

    db = sqlite3.connect(dbpath)

    cursor = db.cursor()

    cursor.execute(("CREATE TABLE IF NOT EXISTS PERSON (\n"
                    "    CASE_NUMBER INTEGER NOT NULL,\n"
                    "    VEHICLE_NUMBER INTEGER NOT NULL,\n"
                    "    PERSON_NUMBER INTEGER NOT NULL,\n"
                    "    AGE INTEGER NULL,\n"
                    "    SEX CHAR(6) NULL,\n"
                    "    PERSON_TYPE CHAR(70) NULL,\n"
                    "    INJURY_SEVERITY CHAR(30) NULL,\n"
                    "    SEATING_POSITION CHAR(80) NULL,\n"
                    "\n"
                    "    PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER),\n"
                    "    CHECK ((AGE >= 0 AND AGE < 121) OR AGE == NULL),\n"
                    "    CHECK (SEX == \"FEMALE\" OR SEX == \"MALE\" OR SEX == NULL),\n")
                   + "CHECK (INJURY_SEVERITY == " + " OR INJURY_SEVERITY == ".join(
        [i for i in set(ValueMappings["INJ_SEV"].values())]) + "),\n"
                   + "CHECK (PERSON_TYPE == " + " OR PERSON_TYPE == ".join(
        [i for i in set(ValueMappings["PER_TYP"].values())]) + "),\n"
                   + "CHECK (SEATING_POSITION == " + " OR SEATING_POSITION == ".join(
        [i for i in set(ValueMappings["SEAT_POS"].values())]) + "))"
                   )

    for i in person:
        if i["AGE"] == "998" or i["AGE"] == "999":
            i["AGE"] = "NULL"
        for j, k in ValueMappings.items():
            i[j] = k[i[j]]
        cursor.execute(f"""INSERT INTO PERSON (CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER, AGE, SEX, PERSON_TYPE, INJURY_SEVERITY, SEATING_POSITION) VALUES
         ({i["ST_CASE"]}, {i["VEH_NO"]}, {i["PER_NO"]}, {i["AGE"]}, {i["SEX"]}, {i["PER_TYP"]}, {i["INJ_SEV"]}, {i["SEAT_POS"]})""")

    db.commit()

    db.close()

