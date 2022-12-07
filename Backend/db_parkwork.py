import sqlite3 as dbapi2
from parkwork import parkwork

class db_parkwork:
    def __init__(self, db_file):
        self.db_file = db_file

    def insertToParkwork(self, parkwork):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            statement = "INSERT INTO PARKWORK (ST_CASE, VEH_NO, PHARM_EV, PCARGTYPE, PSP_USE, PVEH_SEV, PDEATHS) VALUES (?,?,?,?,?,?,?)"
            cursor.execute(statement, (parkwork.st_case, parkwork.veh_no, parkwork.pharm_ev, parkwork.pcargtype, parkwork.psp_use, parkwork.pveh_sev, parkwork.pdeaths))
            connection.commit()

    def updateParkwork(self, st_case, veh_no, parkwork):
        with dbapi2.connect(self.db_file) as connection:
            cursor = connection.cursor()
            statement = "UPDATE PARKWORK SET PHARM_EV = ?, PCARGTYPE = ?, PSP_USE = ?, PVEH_SEV = ?, PDEATHS = ?) WHERE (ST_CASE = ? AND VEH_NO = ?)"
            cursor.execute(statement, (parkwork.pharm_ev, parkwork.pcargtype, parkwork.psp_use, parkwork.pveh_sev, parkwork.pdeaths, st_case, veh_no))
            connection.commit()