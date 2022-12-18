import csv
import sqlite3

ValueMappings = {"AOI1": {"0": "\"Non-Collision\"",
                         "1": "\"1 o'clock\"",
                         "2": "\"2 o'clock\"",
                         "3": "\"3 o'clock\"",
                         "4": "\"4 o'clock\"",
                         "5": "\"5 o'clock\"",
                         "6": "\"6 o'clock\"",
                         "7": "\"7 o'clock\"",
                         "8": "\"8 o'clock\"",
                         "9": "\"9 o'clock\"",
                         "10": "\"10 o'clock\"",
                         "11": "\"11 o'clock\"",
                         "12": "\"12 o'clock\"",
                         "13": "\"Top\"",
                         "14": "\"Undercarriage\"",
                         "18": "\"Cargo/Vehicle Parts Set-in-Motion \"",
                         "19": "\"Other Objects or Person Set-in-Motion\"",
                         "20": "\"Object Set in Motion, Unknown if Cargo/VehicleParts or Other\"",
                         "55": "\"Non-Harmful Event\"",
                         "61": "\"Left\"",
                         "62": "\"Left-Front Side\"",
                         "63": "\"Left-Back Side\"",
                         "81": "\"Right\"",
                         "82": "\"Right-Front Side\"",
                         "83": "\"Right-Back Side\"",
                         "98": "\"Not Reported\"",
                         "99": "\"Reported as Unknown\""
                         },
                 "SOE": {
                     "1": "\"Rollover/Overturn\"",
                     "2": "\"Fire/Explosion\"",
                     "3": "\"Immersion or Partial Immersion\"",
                     "4": "\"Gas Inhalation\"",
                     "5": "\"Fell/Jumped From Vehicle\"",
                     "6": "\"Injured in Vehicle (Non-Collision)\"",
                     "7": "\"Other Non-Collision\"",
                     "8": "\"Pedestrian\"",
                     "9": "\"Pedalcyclist\"",
                     "10": "\"Railway Vehicle\"",
                     "11": "\"Live Animal\"",
                     "12": "\"Motor Vehicle in Transport\"",
                     "14": "\"Parked Motor Vehicle\"",
                     "15": "\"Non-Motorist on Personal Conveyance\"",
                     "16": "\"Thrown or Falling Object\"",
                     "17": "\"Boulder\"",
                     "18": "\"Other Object (Not Fixed)\"",
                     "19": "\"Building\"",
                     "20": "\"Impact Attenuator/Crash Cushion\"",
                     "21": "\"Bridge Pier or Support\"",
                     "23": "\"Bridge Rail (Includes Parapet)\"",
                     "24": "\"Guardrail Face\"",
                     "25": "\"Concrete Traffic Barrier\"",
                     "26": "\"Other Traffic Barrier\"",
                     "30": "\"Utility Pole/Light Support\"",
                     "31": "\"Post, Pole or Other Support\"",
                     "32": "\"Culvert\"",
                     "33": "\"Curb\"",
                     "34": "\"Ditch\"",
                     "35": "\"Embankment\"",
                     "38": "\"Fence\"",
                     "39": "\"Wall\"",
                     "40": "\"Fire Hydrant\"",
                     "41": "\"Shrubbery\"",
                     "42": "\"Tree (Standing Only)\"",
                     "43": "\"Other Fixed Object\"",
                     "44": "\"Pavement Surface Irregularity(Ruts, Potholes, Grates, etc.)\"",
                     "45": "\"Working Motor Vehicle\"",
                     "46": "\"Traffic Signal Support\"",
                     "48": "\"Snow Bank\"",
                     "49": "\"Ridden Animal or Animal-Drawn Conveyance\"",
                     "50": "\"Bridge Overhead Structure\"",
                     "51": "\"Jackknife (Harmful to This Vehicle)\"",
                     "52": "\"Guardrail End\"",
                     "53": "\"Mail Box\"",
                     "54": "\"Motor Vehicle in Transport Strikes or Is Struck by Cargo, Persons or Objects Set-in-Motion From/by Another Motor Vehicle in Transport\"",
                     "55": "\"Motor Vehicle in Motion Outside the Trafficway\"",
                     "57": "\"Cable Barrier\"",
                     "58": "\"Ground\"",
                     "59": "\"Traffic Sign Support\"",
                     "60": "\"Cargo/Equipment Loss or Shift (Non-Harmful)\"",
                     "61": "\"Equipment Failure (Blown Tire, Brake Failure, etc.)\"",
                     "62": "\"Separation of Units\"",
                     "63": "\"Ran off Road Right\"",
                     "64": "\"Ran off Road Left\"",
                     "65": "\"Cross Median\"",
                     "66": "\"Downhill Runaway\"",
                     "67": "\"Vehicle Went Airborne\"",
                     "68": "\"Cross Centerline\"",
                     "69": "\"Re-Entering Highway\"",
                     "70": "\"Jackknife (Non-Harmful)\"",
                     "71": "\"End Departure\"",
                     "72": "\"Cargo/Equipment Loss, Shift, or Damage(Harmful)\"",
                     "73": "\"Object That Had Fallen From Motor Vehicle in Transport\"",
                     "74": "\"Road Vehicle on Rails\"",
                     "79": "\"Ran off Roadway Direction Unknown\"",
                     "91": "\"Unknown Object Not Fixed\"",
                     "93": "\"Unknown Fixed Object\"",
                     "98": "\"Harmful Event, Details Not Reported\"",
                     "99": "\"Unknown/Reported as Unknown\""
                 },
                 "AOI2": {"0": "\"Non-Collision\"",
                         "1": "\"1 o'clock\"",
                         "2": "\"2 o'clock\"",
                         "3": "\"3 o'clock\"",
                         "4": "\"4 o'clock\"",
                         "5": "\"5 o'clock\"",
                         "6": "\"6 o'clock\"",
                         "7": "\"7 o'clock\"",
                         "8": "\"8 o'clock\"",
                         "9": "\"9 o'clock\"",
                         "10": "\"10 o'clock\"",
                         "11": "\"11 o'clock\"",
                         "12": "\"12 o'clock\"",
                         "13": "\"Top\"",
                         "14": "\"Undercarriage\"",
                         "18": "\"Cargo/Vehicle Parts Set-in-Motion \"",
                         "19": "\"Other Objects or Person Set-in-Motion\"",
                         "20": "\"Object Set in Motion, Unknown if Cargo/VehicleParts or Other\"",
                         "55": "\"Non-Harmful Event\"",
                         "61": "\"Left\"",
                         "62": "\"Left-Front Side\"",
                         "63": "\"Left-Back Side\"",
                         "77": "\"Not a Motor Vehicle\"",
                         "81": "\"Right\"",
                         "82": "\"Right-Front Side\"",
                         "83": "\"Right-Back Side\"",
                         "98": "\"Not Reported\"",
                         "99": "\"Reported as Unknown\""
                 }
                 }

def createAndFillCeventTable(database):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cevent = csv.DictReader(open("./TableConverters/cevent.csv"))

    statement0 = '''DROP TABLE IF EXISTS CEVENT'''
    cursor.execute(statement0)

    cursor.execute('''CREATE TABLE IF NOT EXISTS CEVENT (
        CASE_NUMBER INTEGER NOT NULL,
        EVENT_NUMBER INTEGER NOT NULL,
        VEHICLE_NUMBER_1 INTEGER NOT NULL,
        AREA_OF_IMPACT_1 VARCHAR(100),
        SEQUENCE_OF_EVENTS VARCHAR(200),
        VEHICLE_NUMBER_2 INTEGER NULL,
        AREA_OF_IMPACT_2 VARCHAR(100),
        CONSTRAINT PK_CEVENT PRIMARY KEY (CASE_NUMBER, EVENT_NUMBER));
        ''')

    # later CASE_NUMBER should be foreign key referencing CASE_NUMBER in Accident table
    # later (CASE_NUMBER AND VEHICLE_NUMBER_1) and (CASE_NUMBER AND VEHICLE_NUMBER_2) should be foreign key referencing CASE_NUMBER AND VEHICLE_NUMBER in Vehicle table

    for row in cevent:
        if row["VNUMBER2"] == '5555':
            row["VNUMBER2"] = "NULL"
        if row["VNUMBER2"] == '9999':
            row["VNUMBER2"] = "NULL"
        cursor.execute(f"INSERT INTO CEVENT VALUES ({row['ST_CASE']}, {row['EVENTNUM']}, {row['VNUMBER1']}, {ValueMappings['AOI1'][row['AOI1']]}, {ValueMappings['SOE'][row['SOE']]}, {row['VNUMBER2']}, {ValueMappings['AOI2'][row['AOI2']]})")

    connection.commit()
    connection.close()
