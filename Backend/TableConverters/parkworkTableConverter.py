import sqlite3 as dbapi2
import pandas as pd

ValueMappings = {"ST_CASE" : {},
                "VEH_NO" : {},
                "PHARM_EV": {
                     "1": "\"Rollover/Overturn\"",
                     "2": "\"Fire/Explosion\"",
                     "3": "\"Immersion\"",
                     "4": "\"Gas Inhalation\"",
                     "5": "\"Fell/Jumped From Vehicle\"",
                     "6": "\"Injured in Vehicle\"",
                     "7": "\"Other Non-Collision\"",
                     "8": "\"Pedestrian\"",
                     "9": "\"Pedalcyclist\"",
                     "10": "\"Railway Vehicle\"",
                     "11": "\"Live Animal\"",
                     "12": "\"Motor Vehicle in Transport\"",
                     "13": "\"Motor Vehicle in Transport on Other Roadway\"",
                     "14": "\"Parked Motor Vehicle\"",
                     "15": "\"Non-Motorist on Personal Conveyance\"",
                     "16": "\"Thrown or Falling Object\"",
                     "17": "\"Boulder\"",
                     "18": "\"Other Object (Not Fixed)\"",
                     "19": "\"Building\"",
                     "20": "\"Impact Attenuator/Crash Cushion\"",
                     "21": "\"Bridge Pier or Support\"",
                     "22": "\"Bridge Parapet End\"",
                     "23": "\"Bridge Rail\"",
                     "24": "\"Guardrail Face\"",
                     "25": "\"Concrete Traffic Barrier\"",
                     "26": "\"Other Traffic Barrier\"",
                     "27": "\"Highway/Traffic Sign Post\"",
                     "28": "\"Overhead Sign Support/Sign\"",
                     "29": "\"Luminary/Light Support\"",
                     "30": "\"Utility Pole/Light Support\"",
                     "31": "\"Post, Pole or Other Support\"",
                     "32": "\"Culvert\"",
                     "33": "\"Curb\"",
                     "34": "\"Ditch\"",
                     "35": "\"Embankment\"",
                     "36": "\"Embankment – Rock, Stone, or Concrete\"",
                     "37": "\"Embankment – Material Type Unknown\"",
                     "38": "\"Fence\"",
                     "39": "\"Wall\"",
                     "40": "\"Fire Hydrant\"",
                     "41": "\"Shrubbery\"",
                     "42": "\"Tree (Standing Only)\"",
                     "43": "\"Other Fixed Object\"",
                     "44": "\"Pavement Surface Irregularity\"",
                     "45": "\"Working Motor Vehicle\"",
                     "46": "\"Traffic Signal Support\"",
                     "47": "\"Vehicle Occupant Struck or Run Over by Own Vehicle\"",
                     "48": "\"Snow Bank\"",
                     "49": "\"Ridden Animal or Animal-Drawn Conveyance\"",
                     "50": "\"Bridge Overhead Structure\"",
                     "51": "\"Jackknife\"",
                     "52": "\"Guardrail End\"",
                     "53": "\"Mail Box\"",
                     "54": "\"Motor Vehicle in Transport Strikes or is Struck by Cargo, Persons or Objects Set-in-Motion From/By Another Motor Vehicle in Transport\"",
                     "55": "\"Motor Vehicle in Motion Outside the Trafficway\"",
                     "57": "\"Cable Barrier\"",
                     "58": "\"Ground\"",
                     "59": "\"Traffic Sign Support\"",
                     "72": "\"Cargo/Equipment Loss or Shift\"",
                     "73": "\"Object That Had Fallen From Motor Vehicle in Transport\"",
                     "74": "\"Road Vehicle on Rails\"",
                     "91": "\"Unknown Object Not Fixed\"",
                     "93": "\"Unknown Fixed Object\"",
                     "98": "\"Harmful Event, Details Not Reported\"",
                     "99": "\"Reported as Unknown\"",
                },
                 "PCARGTYP": {
                     "0": "\"Not Applicable\"",
                     "1": "\"Van/Enclosed Box\"",
                     "2": "\"Cargo Tank\"",
                     "3": "\"Flatbed\"",
                     "4": "\"Dump\"",
                     "5": "\"Concrete Mixer\"",
                     "6": "\"Auto Transporter\"",
                     "7": "\"Garbage/Refuse\"",
                     "8": "\"Grain, Chips, Gravel\"",
                     "9": "\"Pole-Trailer\"",
                     "10": "\"Log\"",
                     "11": "\"Intermodal Container Chassis\"",
                     "12": "\"Vehicle Towing Another Motor Vehicle\"",
                     "20": "\"Bus (Seats 9-15 People, Including Driver)\"",
                     "21": "\"Bus (Seats for 16 or More People, Including Driver)\"",
                     "22": "\"Bus\"",
                     "28": "\"Not Reported\"",
                     "96": "\"No Cargo Body Type\"",
                     "97": "\"Other\"",
                     "98": "\"Unknown Cargo Body Type\"",
                     "99": "\"Reported as Unknown\"",
                 },
                 "PSP_USE": {
                     "0": "\"No Special Use\"",
                     "1": "\"Taxi\"",
                     "2": "\"Vehicle Used as School Transport\"",
                     "3": "\"Vehicle Used as Other Bus\"",
                     "4": "\"Military\"",
                     "5": "\"Police\"",
                     "6": "\"Ambulance\"",
                     "7": "\"Fire Truck\"",
                     "8": "\"Non-Transport Emergency Services Vehicle\"",
                     "10": "\"Safety Service Patrols – Incident Response\"",
                     "11": "\"Other Incident Response \"",
                     "12": "\"Towing – Incident Response\"",
                     "13": "\"Incident Response\"",
                     "19": "\"Motor Vehicle Used for Vehicle Sharing Mobility\"",
                     "20": "\"Motor Vehicle Used for Electronic Ride-Hailing\"",
                     "21": "\"Mail Carrier\"",
                     "22": "\"Public Utility\"",
                     "23": "\"Rental Truck Over 10,000 lbs\"",
                     "24": "\"Truck Operating With Crash Attenuator Equipment\"",
                     "98": "\"Not Reported\"",
                     "99": "\"Reported as Unknown\"",
                 },
                 "PVEH_SEV": {
                    "0": "\"No Damage\"",
                    "2": "\"Minor Damage\"",
                    "4": "\"Functional Damage\"",
                    "6": "\"Disabling Damage\"",
                    "8": "\"Not Reported\"",
                    "9": "\"Reported as Unknown\"",
                 },
                 "PDEATHS": {}
                 }

def read_from_csv():
    file_name = './TableConverters/parkwork.csv'
    data_frame = pd.read_csv(file_name)

    header = ['ST_CASE', 'VEH_NO', 'PHARM_EV', 'PCARGTYP', 'PSP_USE', 'PVEH_SEV', 'PDEATHS']
    content = data_frame[header]

    return content


def write_to_csv(content):
    filename = 'parkwork.csv'
    df = pd.DataFrame(content)
    df.to_csv(filename, index=False, header=True)


def printContent(content):
    print("{:<10} {:<10} {:<35} {:<20} {:<30} {:<30} {:<20}".format('ST_CASE', 'VEH_NO', 'PHARM_EV', 'PCARGTYP', 'PSP_USE', 'PVEH_SEV', 'PDEATHS'))
    for i in range(200):
        print("{:<10} {:<10} {:<35} {:<20} {:<30} {:<30} {:<20}".format(content[i]['ST_CASE'], content[i]['VEH_NO'], content[i]['PHARM_EV'], content[i]['PCARGTYP'], content[i]['PSP_USE'], content[i]['PVEH_SEV'], content[i]['PDEATHS']))


def createFillTableParkwork(connection):
    content = read_from_csv()

    mapped_content = []
    for n in range(len(content)):
        mapped_content.append({})
        for i, j in ValueMappings.items():
            if (i == "ST_CASE" or i == "VEH_NO" or i == "PDEATHS"):
                mapped_content[n][i] = content.iloc[n][i]
            else:
                mapped_content[n][i] = j[str(content.iloc[n][i])]

    content = mapped_content

    ### data base operations #################################################################

    # query 1 ##
    try:
        conn = dbapi2.connect(connection.db)
        cursor = conn.cursor()
        statement = """DROP TABLE PARKWORK"""
        cursor.execute(statement)

    except dbapi2.DatabaseError:
        conn.rollback()
    ############

    # query 2 ##
    statement = """CREATE TABLE PARKWORK (
        CASE_NUMBER INTEGER NOT NULL REFERENCES Accident(ST_CASE),
        VEHICLE_NUMBER INTEGER NOT NULL,
        FIRST_HARMFUL_EVENT CHAR(140) NOT NULL,
        CARGO_BODY_TYPE CHAR(60) NOT NULL DEFAULT "Not Applicable",
        SPECIAL_USE CHAR(50) NOT NULL DEFAULT "No Special Use",
        EXTENT_OF_DAMAGE CHAR(25) NOT NULL DEFAULT "No Damage",
        DEATHS INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (CASE_NUMBER, VEHICLE_NUMBER),
        CHECK (DEATHS > -1 AND DEATHS < 100)
    )"""

    # Dont forget to add this line -> FOREIGN KEY CASE_NUMBER REFERENCES ACCIDENT(CASE_NUMBER)

    connection.executeSQLQuery(statement)
    ############

    ## query 3 ##
    for i in range(len(content)):
        statement = f"""INSERT INTO PARKWORK (CASE_NUMBER, VEHICLE_NUMBER, FIRST_HARMFUL_EVENT, CARGO_BODY_TYPE, SPECIAL_USE, EXTENT_OF_DAMAGE, DEATHS) VALUES ({int(content[i]['ST_CASE'])}, {int(content[i]['VEH_NO'])}, {content[i]['PHARM_EV']}, {content[i]['PCARGTYP']}, {content[i]['PSP_USE']}, {content[i]['PVEH_SEV']}, {int(content[i]['PDEATHS'])})"""
        
        connection.executeSQLQuery(statement)
    #############

    ##########################################################################################