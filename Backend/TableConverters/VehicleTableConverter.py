import csv
import sqlite3


ValueMappings = {"HIT_RUN" : {"0": "\"No\"",
                            "1": "\"Yes\"",
                            "9": "\"Unknown\""
                            },
                "OWNER" : {"0": "\"Not Applicable, Vehicle Not Registered\"",
                            "1": "\"Driver (in This Crash) Was Registered Owner\"",
                            "2": "\"Driver (in This Crash) Not Registered Owner (Other Private Owner)\"",
                            "3": "\"Vehicle Registered as Business/Company/Government Vehicle\"",
                            "4": "\"Vehicle Registered as Rental Vehicle\"",
                            "5": "\"Vehicle Was Stolen (Reported by Police)\"",
                            "6": "\"Driverless/Motor Vehicle Parked/Stopped off Roadway\"",
                            "9": "\"Unknown\""
                            },
                "MAKE" : {"1": "\"American Motors\"",
                            "2": "\"Jeep\"",
                            "3": "\"AM General\"",
                            "6": "\"Chrysler\"",
                            "7": "\"Dodge\"",
                            "8": "\"Imperial\"",
                            "9": "\"Plymouth\"",
                            "10": "\"Eagle (Since 1988)\"",
                            "12": "\"Ford\"",
                            "13": "\"Lincoln\"",
                            "14": "\"Mercury\"",
                            "18": "\"Buick\"",
                            "19": "\"Cadillac\"",
                            "20": "\"Chevrolet\"",
                            "21": "\"Oldsmobile\"",
                            "22": "\"Pontiac\"",
                            "23": "\"GMC\"",
                            "29": "\"Other Domestic\"",
                            "30": "\"Volkswagen\"",
                            "31": "\"Alfa Romeo\"",
                            "32": "\"Audi\"",
                            "33": "\"Austin-Healey\"",
                            "35": "\"Datsun\"",
                            "36": "\"Fiat\"",
                            "37": "\"Honda\"",
                            "38": "\"Isuzu\"",
                            "39": "\"Jaguar\"",
                            "40": "\"Lancia\"",
                            "41": "\"Mazda\"",
                            "42": "\"Mercedes-Benz\"",
                            "43": "\"MG\"",
                            "44": "\"Peugeot\"",
                            "45": "\"Porsche\"",
                            "46": "\"Renault\"",
                            "47": "\"Saab\"",
                            "48": "\"Subaru\"",
                            "49": "\"Toyota\"",
                            "50": "\"Triumph\"",
                            "51": "\"Volvo\"",
                            "52": "\"Mitsubishi (Since 1982)\"",
                            "53": "\"Suzuki (Since 1987)\"",
                            "57": "\"Lexus (Since 1988)\"",
                            "58": "\"Infiniti (Since 1988)\"",
                            "59": "\"Other Imports\"",
                            "60": "\"BSA\"",
                            "61": "\"Ducati\"",
                            "62": "\"Harley-Davidson\"",
                            "63": "\"Kawasaki\"",
                            "64": "\"Moto Guzzi\"",
                            "65": "\"Norton\"",
                            "67": "\"Yamaha\"",
                            "69": "\"Other Motor Cycle\"",
                            "70": "\"Moped\"",
                            "80": "\"Brockway\"",
                            "81": "\"Diamond Reo\"",
                            "82": "\"Freightliner\"",
                            "83": "\"FWD\"",
                            "84": "\"International Harvester\"",
                            "85": "\"Kenworth\"",
                            "86": "\"Mack\"",
                            "87": "\"Peterbilt\"",
                            "88": "\"White\"",
                            "95": "\"Other Truck/Bus\"",
                            "98": "\"Other Make\"",
                            "99": "\"Unknown Make\""
                        }
                        }

def createAndFillVehicleTable(dbpath):
    vehicles = csv.DictReader(open("./TableConverters/vehicle.csv"))

    connection = sqlite3.connect(dbpath)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOTE EXISTS VEHICLE(
        CASE_NUMBER INTEGER NOT NULL,
        VEHICLE_NO INTEGER NOT NULL,
        NUMBER_OF_OCCUPANTS INTEGER NOT NULL,
        HIT_RUN CHAR(10) NOT NULL,
        OWNER VARCHAR(100) NOT NULL,
        MAKE VARCHAR(50) NOT NULL,
        MODEL_YEAR INTEGER NOT NULL,

        PRIMARY KEY (CASE_NUMBER, VEHICLE_NO))
    """)

    for vehicle in vehicles:
        cursor.execute(f"INSERT INTO VEHICLE (CASE_NUMBER, VEHICLE_NO, NUMBER_OF_OCCUPANTS, HIT_RUN, OWNER, MAKE, MODEL_YEAR) VALUES ({vehicle["ST_CASE"]},{vehicle["VEH_NO"]},{vehicle["NUMOCCS"]},{ValueMappings["HIT_RUN"][vehicle["HIT_RUN"]]},{ValueMappings["OWNER"][vehicle["OWNER"]]},{ValueMappings["MAKE"][vehicle["MAKE"]]},{vehicle["MOD_YEAR"]})")


    connection.commit()
    connection.close()