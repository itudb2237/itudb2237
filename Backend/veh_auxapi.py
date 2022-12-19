from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.vehAuxTableConverter as vehAuxTableConverter

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='VEH_AUX'").fetchall():
    vehAuxTableConverter.createAndFillVehicleAuxillaryTable()

vehAuxColumns = [{"name": i[1], "type": "CHAR" if i[2].startswith("CHAR") else i[2]}   # use starts with to eliminate difference between CHAR(x) and CHAR(y)
                 for i in db.executeSQLQuery("PRAGMA table_info(VEH_AUX)").fetchall()]

for i in vehAuxColumns:
    if i["name"] in ["VEHICLE_BODY_TYPE", "MOTORCYCLE_LICENSE_STATUS", "SCHOOL_BUS", "SPEEDING_VEHICLE", "ROLLOVER"]:
        i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM VEH_AUX ORDER BY {i['name']};").fetchall()
        if i["possibleValues"][0] == (None,):
            i["possibleValues"][0] = ("NULL",)
        else:
            i["possibleValues"].insert(0, ("NULL",))
        i["possibleValues"].insert(1, ("NOT NULL",))
        i["possibleValues"].insert(0, ("All Values",))

print(vehAuxColumns)


@app.route('/getVehAuxHeader', methods=['GET'])
def getVehAuxHeaders():
    response = make_response(vehAuxColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getVehAuxes', methods=['GET'])
def getVehAuxes():
    if not requestchecker(request.remote_addr, db):
        return "Too many requests", 429

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], vehAuxColumns))
                                        , type=str).split(",")

    orderBy = request.args.get('orderBy', default="CASE_NUMBER", type=str)

    order = request.args.get('order', default="ASC", type=str)

    filters = []

    for i in vehAuxColumns:
        currentFilter = request.args.get('filter'+i["name"], default="", type=str)
        if currentFilter == "NULL":
            filters.append(i["name"] + " IS NULL")
        elif currentFilter == "NOT NULL":
            filters.append(i["name"] + " IS NOT NULL")
        elif currentFilter == "All Values":
            continue
        elif currentFilter != "":
            if i["type"] == "CHAR":
                if "possibleValues" in i:
                    filters.append(i["name"] + " == \"" + currentFilter + "\"")
                else:
                    filters.append(i["name"] + " LIKE \"" + currentFilter + "%\"")
            elif i["type"] == "INTEGER":
                rangeOfValue = currentFilter.split(",")
                if rangeOfValue[0] != "" and rangeOfValue[1] != "":
                    filters.append(i["name"] + " BETWEEN " + rangeOfValue[0] + " AND " + rangeOfValue[1])
                elif rangeOfValue[1] != "":
                    filters.append(i["name"] + " <= " + rangeOfValue[1])
                else:
                    filters.append(i["name"] + " >= " + rangeOfValue[0])

    filters = " AND ".join(filters)
    print(filters)

    countQuery = f"SELECT COUNT(*) FROM VEH_AUX {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requestedcolumns)} FROM VEH_AUX {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {orderBy} {order} LIMIT {(pagenumber - 1)*rowperpage}, {rowperpage}"

    print(query)

    results = {
        "data": db.executeSQLQuery(query).fetchall(),
        "maxPageCount": int((count+rowperpage - 1)/rowperpage)
    }
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getVehAux/<int:case_number>')
def getVehAuxesInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM VEH_AUX WHERE CASE_NUMBER = {case_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getVehAux/<int:case_number>/<int:vehicle_number>')
def getVehAux(case_number, vehicle_number):
    results = db.executeSQLQuery(f"SELECT * FROM VEH_AUX WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number}").fetchall()[0]
    response = make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/addVehAux', methods=['POST'])
def addVehAux():
    data = request.form
    query = f"INSERT INTO VEH_AUX ({', '.join([i['name'] for i in vehAuxColumns])}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    print(tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in vehAuxColumns]))
    db.executeSQLQuery(query, tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in vehAuxColumns]))
    return "OK", 204


@app.route('/updateVehAux', methods=['POST'])
def updateVehAux():
    data = dict(request.form)
    for i in data.keys():
        if data[i] == "NULL" or data[i] == "":
            data[i] = None
    db.executeSQLQuery(f"UPDATE VEH_AUX SET VEHICLE_BODY_TYPE = ?, MOTORCYCLE_LICENSE_STATUS = ?, SCHOOL_BUS = ?,SPEEDING_VEHICLE = ?, ROLLOVER = ? WHERE CASE_NUMBER = ? AND VEHICLE_NUMBER = ?",
                       (data["VEHICLE_BODY_TYPE"], data["MOTORCYCLE_LICENSE_STATUS"], data["SCHOOL_BUS"], data["SPEEDING_VEHICLE"],data["ROLLOVER"], int(data["CASE_NUMBER"]), int(data["VEHICLE_NUMBER"])))
    return "OK", 204


@app.route('/deleteVehAux/<int:case_number>/<int:vehicle_number>', methods=['POST'])
def deleteVehAux(case_number, vehicle_number):
    db.executeSQLQuery(f"DELETE FROM VEH_AUX WHERE CASE_NUMBER = ? AND VEHICLE_NUMBER = ?", (case_number, vehicle_number))
    return "OK", 204
