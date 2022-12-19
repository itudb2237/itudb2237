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
                            "10": "\"Eagle\"",
                            "12": "\"Ford\"",
                            "13": "\"Lincoln\"",
                            "14": "\"Mercury\"",
                            "18": "\"Buick\"",
                            "19": "\"Cadillac\"",
                            "20": "\"Chevrolet\"",
                            "21": "\"Oldsmobile\"",
                            "22": "\"Pontiac\"",
                            "23": "\"GMC\"",
                            "24": "\"Saturn\"",
                            "25": "\"Grumman\"",
                            "26": "\"Coda\"",
                            "29": "\"Other Domestic\"",
                            "30": "\"Volkswagen\"",
                            "31": "\"Alfa Romeo\"",
                            "32": "\"Audi\"",
                            "33": "\"Austin-Healey\"",
                            "34": "\"BMW\"",
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
                            "52": "\"Mitsubishi\"",
                            "53": "\"Suzuki\"",
                            "54": "\"Acura\"",
                            "55": "\"Hyundai\"",
                            "56": "\"Merkur\"",
                            "57": "\"Lexus\"",
                            "58": "\"Infiniti\"",
                            "59": "\"Other Imports\"",
                            "60": "\"BSA\"",
                            "61": "\"Ducati\"",
                            "62": "\"Harley-Davidson\"",
                            "63": "\"Kawasaki\"",
                            "64": "\"Moto Guzzi\"",
                            "65": "\"Norton\"",
                            "66": "\"Mahindra\"",
                            "67": "\"Yamaha\"",
                            "69": "\"Other Motor Cycle\"",
                            "70": "\"Moped\"",
                            "71": "\"Ducati\"",
                            "72": "\"Harley-Davidson\"",
                            "73": "\"Kawasaki\"",
                            "74": "\"Moto Guzzi\"",
                            "75": "\"Norton\"",
                            "76": "\"Yamaha\"",
                            "77": "\"Victory\"",
                            "78": "\"Other Make Moped\"",
                            "79": "\"Other Make Motored Cycle\"",
                            "80": "\"Brockway\"",
                            "81": "\"Diamond Reo\"",
                            "82": "\"Freightliner\"",
                            "83": "\"FWD\"",
                            "84": "\"International Harvester\"",
                            "85": "\"Kenworth\"",
                            "86": "\"Mack\"",
                            "87": "\"Peterbilt\"",
                            "88": "\"White\"",
                            "89": "\"White/Autocar\"",
                            "90": "\"Bluebird\"",
                            "91": "\"Eagle Coach\"",
                            "92": "\"Gillig\"",
                            "93": "\"MCI\"",
                            "94": "\"Thomas Built\"",
                            "95": "\"Other Truck/Bus\"",
                            "97": "\"Not Reported\"",
                            "98": "\"Other Make\"",
                            "99": "\"Unknown Make\""
                        }
                        }

def createAndFillVehicleTable():
    
    dbpath = "database.db"
    connection = sqlite3.connect(dbpath)
    cursor = connection.cursor()

    

    cursor.execute("""CREATE TABLE IF NOT EXISTS VEHICLE(
        CASE_NUMBER INTEGER NOT NULL,
        VEHICLE_NUMBER INTEGER NOT NULL,
        NUMBER_OF_OCCUPANTS INTEGER NOT NULL,
        HIT_RUN VARCHAR(10) NOT NULL,
        OWNER VARCHAR(100) NOT NULL,
        MAKE VARCHAR(50) NOT NULL,
        MODEL_YEAR INTEGER NOT NULL,

        PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER))
    """)

    
    vehicles = csv.DictReader(open("./TableConverters/vehicle.csv"))
    for vehicle in vehicles:
        cursor.execute(f"INSERT INTO VEHICLE (CASE_NUMBER, VEHICLE_NUMBER, NUMBER_OF_OCCUPANTS, HIT_RUN, OWNER, MAKE, MODEL_YEAR) VALUES ({int(vehicle['ST_CASE'])},{int(vehicle['VEH_NO'])},{int(vehicle['NUMOCCS'])},{ValueMappings['HIT_RUN'][vehicle['HIT_RUN']]},{ValueMappings['OWNER'][vehicle['OWNER']]},{ValueMappings['MAKE'][vehicle['MAKE']]},{int(vehicle['MOD_YEAR'])})")

    connection.commit()
    connection.close()
