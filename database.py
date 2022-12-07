import sqlite3 as dbapi2

from Cevent import Cevent  


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile  

    def insertToCevent(self, Cevent):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Cevent VALUES(?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (Cevent.st_case, Cevent.eventnum, Cevent.vnumber1, Cevent.aoi1, Cevent.soe, Cevent.vnumber2, Cevent.aoi2))
            connection.commit()

    def updateCevent(self, st_case, eventnum,):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE Cevent SET VNUMBER1 = ?, AOI1 = ?, SOE = ?, VNUMBER2 = ?, AOI2 = ? WHERE (ST_CASE = ? AND EVENTNUM = ?)"
            cursor.execute(query, (Cevent.vnumber1, Cevent.aoi1, Cevent.soe, Cevent.vnumber2, Cevent.aoi2, st_case, eventnum))
            connection.commit()

    # def deleteFromCevent(self, st_case = 0, eventnum = 0, vnumber1 = 0, aoi1 = 0, soe = 0, vnumber2 = 0, aoi2 = 0):
    #     ### TODO-2: COMPLETE delete_Cevent function
    #     with dbapi2.connect(self.dbfile) as connection:
    #         cursor = connection.cursor()
    #         query = "DELETE FROM Cevent WHERE (ID = ?)"
    #         cursor.execute(query, (Cevent_key,))
    #         connection.commit()


    #     ####################################################################

    def get_Cevent(self, st_case, eventnum):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM CEVENT WHERE (ST_CASE = ? AND EVENTNUM = ?)"
            cursor.execute(query, (st_case, eventnum))
            tuple_string = cursor.fetchone()
        return tuple_string