import csv
import sqlite3 as dbapi2
import pandas as pd


def read_from_csv():
    file_name = 'FARS2015NationalCSV_parkwork.csv'
    data_frame = pd.read_csv(file_name)

    header = ['ST_CASE', 'VEH_NO', 'PHARM_EV', 'PCARGTYP', 'PSP_USE', 'PVEH_SEV', 'PDEATHS']
    content = data_frame[header]

    return content


def write_to_csv(content):
    filename = 'parkwork.csv'
    content.to_csv(filename, index=False)


def printContent(content):
    print("{} \t {} \t {} \t {} \t {} \t {} \t {}".format('ST_CASE', 'VEH_NO', 'PHARM_EV', 'PCARGTYP', 'PSP_USE', 'PVEH_SEV', 'PDEATHS'))
    for i in range(100):
        print("{} \t\t {} \t\t {} \t\t {} \t\t {} \t\t {} \t\t {}".format(content.iloc[i]['ST_CASE'], content.iloc[i]['VEH_NO'], content.iloc[i]['PHARM_EV'], content.iloc[i]['PCARGTYP'], content.iloc[i]['PSP_USE'], content.iloc[i]['PVEH_SEV'], content.iloc[i]['PDEATHS']))


if __name__ == "__main__":
    content = read_from_csv()

    write_to_csv(content)
    printContent(content)

    #dsn = """user = '' password = '' host = '' port = '' dbname  = ''"""
    connection = dbapi2.connect('ParkWork.db')
    cursor  = connection.cursor()

    ### data base operations #################################################################

    ## query 1 ##
    try:
        statement = """DROP TABLE ParkWork"""
        cursor.execute(statement)

    except dbapi2.DatabaseError:
        connection.rollback()
    #############

    ## query 2 ##
    statement = """CREATE TABLE ParkWork (
        st_case INTEGER NOT NULL REFERENCES Accident(st_case),
        veh_no INTEGER NOT NULL,
        pharm_ev INTEGER NOT NULL,
        pcargtype INTEGER NOT NULL DEFAULT 0,
        psp_use INTEGER NOT NULL DEFAULT 0,
        pveh_sev INTEGER NOT NULL DEFAULT 0,
        pdeaths INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (st_case, veh_no)
    )"""

    cursor.execute(statement)
    #############

    ## query 3 ##
    for i in range(len(content)):
        statement = """INSERT INTO ParkWork (st_case, veh_no, pharm_ev, pcargtype, psp_use, pveh_sev, pdeaths) VALUES (?,?,?,?,?,?,?)"""
        cursor.execute(statement, (int(content.iloc[i]['ST_CASE']), int(content.iloc[i]['VEH_NO']), int(content.iloc[i]['PHARM_EV']), int(content.iloc[i]['PCARGTYP']), int(content.iloc[i]['PSP_USE']), int(content.iloc[i]['PVEH_SEV']), int(content.iloc[i]['PDEATHS'])))
    #############

    ##########################################################################################

    connection.commit()
    cursor.close()
    connection.close()