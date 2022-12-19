from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.VehicleTableConverter as VehicleTableConverter

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='VEHICLE'").fetchall():
    VehicleTableConverter.createAndFillVehicleTable()

vehicleColumns = [{"name": i[1], "type": "VARCHAR" if i[2].startswith("VARCHAR") else i[2]}   # use starts with to eliminate difference between VARCHAR(x) and VARCHAR(y)
                 for i in db.executeSQLQuery("PRAGMA table_info(VEHICLE)").fetchall()]

for i in vehicleColumns:
    if i["name"] in ["HIT_RUN", "OWNER", "MAKE"]:
        i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM VEHICLE ORDER BY {i['name']};").fetchall()
        if i["possibleValues"][0] == (None,):
            i["possibleValues"][0] = ("NULL",)
        else:
            i["possibleValues"].insert(0, ("NULL",))
        i["possibleValues"].insert(1, ("NOT NULL",))
        i["possibleValues"].insert(0, ("All Values",))

print(vehicleColumns)


@app.route('/getVehicleHeader', methods=['GET'])
def getVehicleHeaders():
    response = make_response(vehicleColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getVehicles', methods=['GET'])
def getVehicles():
#    if not requestchecker(request.remote_addr, db):
#        return "Too many requests", 429

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], vehicleColumns))
                                        , type=str).split(",")

    orderBy = request.args.get('orderBy', default="CASE_NUMBER", type=str)

    order = request.args.get('order', default="ASC", type=str)

    filters = []

    for i in vehicleColumns:
        currentFilter = request.args.get('filter'+i["name"], default="", type=str)
        if currentFilter == "NULL":
            filters.append(i["name"] + " IS NULL")
        elif currentFilter == "NOT NULL":
            filters.append(i["name"] + " IS NOT NULL")
        elif currentFilter == "All Values":
            continue
        elif currentFilter != "":
            if i["type"] == "VARCHAR":
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

    countQuery = f"SELECT COUNT(*) FROM Vehicle {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requestedcolumns)} FROM VEHICLE {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {orderBy} {order} LIMIT {(pagenumber - 1)*rowperpage}, {rowperpage}"

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


@app.route('/getVehicle/<int:case_number>')
def getVehiclesInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM VEHICLE WHERE CASE_NUMBER = {case_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getVehicle/<int:case_number>/<int:vehicle_number>')
def getVehicle(case_number, vehicle_number):
    results = db.executeSQLQuery(f"SELECT * FROM VEHICLE WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number}").fetchall()[0]
    response = make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response