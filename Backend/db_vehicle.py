from vehicle import Vehicle 
import sqlite as dbapi2 

class db_vehicle:
    def __init__(self, dbfile):
        self.dbfile
    
    def insertToVehicle(self, vehicle):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Vehicle VALUES (?,?,?,?,?,?,?)"
            cursor.execute(query, (vehicle.st_case, vehicle.veh_no, vehicle.numoccs, vehicle.hit_run, vehicle.owner, vehicle.make, vehicle.mod_year))
            connection.commit()

    def deleteFromVehicle(self, st_case, veh_no):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Vehicle WHERE (st_case = ? AND veh_no = ?)"
            cursor.execute(query, (st_case, veh_no))
            connection.commit()

    def getVehicles(self):
        vehicles = []
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT st_case, veh_no, numoccs, hit_run, owner, make, mod_year FROM Vehicle ORDER BY st_case, veh_no"
            cursor.execute(query)
            for st_case, veh_no, numoccs, hit_run, owner, make, mod_year in cursor:
                vehicles.append(Vehicle(st_case, veh_no, numoccs, hit_run, owner, make, mod_year))
        return vehicles

    def updateVehicle(self, st_case, veh_no, vehicle):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "UPDATE Vehicle SET numoccs = ?, hit_run = ?, owner = ?, make = ?, mod_year = ? WHERE (st_case = ? AND veh_no = ?)"
            cursor.execute(query, (vehicle.numoccs, vehicle.hit_run, vehicle.owner, vehicle.make, vehicle.mod_year, st_case, veh_no))
            connection.commit()
