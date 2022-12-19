from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.AccidentTableConverter as AccidentTableConverter

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='ACCIDENT'").fetchall():
    AccidentTableConverter.createAndFillAccidentTable()

accidentColumns = [{"name": i[1], "type": "CHAR" if i[2].startswith("CHAR") else i[2]}
                 for i in db.executeSQLQuery("PRAGMA table_info(ACCIDENT)").fetchall()]

for i in accidentColumns:
    if i["name"] in ["STATE", "USED_LAND"]:
        i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM ACCIDENT ORDER BY {i['name']};").fetchall()
        if i["possibleValues"][0] == (None,):
            i["possibleValues"][0] = ("NULL",)
        else:
            i["possibleValues"].insert(0, ("NULL",))
        i["possibleValues"].insert(1, ("NOT NULL",))
        i["possibleValues"].insert(0, ("All Values",))


print(accidentColumns)

@app.route('/getAccidentHeader', methods=['GET'])
def getAccidentHeaders():
    response = make_response(accidentColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getAccidents', methods=['GET'])
def getAccidents():
    if not requestchecker(request.remote_addr, db):
        return "Too many requests", 429

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], accidentColumns))
                                        , type=str).split(",")

    orderBy = request.args.get('orderBy', default="CASE_NUMBER", type=str)

    order = request.args.get('order', default="ASC", type=str)

    filters = []

    for i in accidentColumns:
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

    countQuery = f"SELECT COUNT(*) FROM Accident {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requestedcolumns)} FROM ACCIDENT {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {orderBy} {order} LIMIT {(pagenumber - 1)*rowperpage}, {rowperpage}"

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


@app.route('/getAccident/<int:case_number>')
def getAccidentsInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM ACCIDENT WHERE CASE_NUMBER = {case_number}").fetchall()[0]
    response = make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/addAccident', methods=['POST'])
def addAccident():
    data = request.form
    query = f"INSERT INTO ACCIDENT ({', '.join([i['name'] for i in accidentColumns])}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    print(tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in accidentColumns]))
    db.executeSQLQuery(query, tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in accidentColumns]))
    return "OK", 204


@app.route('/updateAccident', methods=['POST'])
def updateAccident():
    data = dict(request.form)
    for i in data.keys():
        if data[i] == "NULL" or data[i] == "":
            data[i] = None
    db.executeSQLQuery(f"UPDATE ACCIDENT SET STATE = ?, YEAR = ?, USED_LAND = ?,LATITUDE = ?, LONGITUDE = ? WHERE CASE_NUMBER = ?",
                       (int(data["STATE"]) if data["STATE"] else None, data["YEAR"], int(data["USED_LAND"]) if data["USED_LAND"] else None, data["LATITUDE"], data["LONGITUDE"], int(data["CASE_NUMBER"])))
    return "OK", 204


@app.route('/deleteAccident/<int:case_number>/<int:vehicle_number>/<int:accident_number>', methods=['POST'])
def deleteAccident(case_number, vehicle_number, accident_number):
    db.executeSQLQuery(f"DELETE FROM ACCIDENT WHERE CASE_NUMBER = ?", (case_number))
    return "OK", 204

