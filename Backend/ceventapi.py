from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.CeventTableConverter as CeventTableConverter

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='CEVENT'").fetchall():
    CeventTableConverter.createAndFillCeventTable(db.db)

ceventColumns = [{"name": i[1], "type": "VARCHAR" if i[2].startswith("VARCHAR") else i[2]}   # use starts with to eliminate difference between VARCHAR(x) and VARCHAR(y)
                 for i in db.executeSQLQuery("PRAGMA table_info(CEVENT)").fetchall()]

for i in ceventColumns:
    if i["name"] in ["AREA_OF_IMPACT_1", "SEQUENCE_OF_EVENTS", "AREA_OF_IMPACT_2"]:
        i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM CEVENT ORDER BY {i['name']};").fetchall()
        if i["possibleValues"][0] == (None,):
            i["possibleValues"][0] = ("NULL",)
        else:
            i["possibleValues"].insert(0, ("NULL",))
        i["possibleValues"].insert(1, ("NOT NULL",))
        i["possibleValues"].insert(0, ("All Values",))
print()
print()
print()
print()

print(ceventColumns)


@app.route('/getCeventHeader', methods=['GET'])
def getCeventHeaders():
    response = make_response(ceventColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getCevents', methods=['GET'])
def getCevents():
#    if not requestchecker(request.remote_addr, db):
#        return "Too many requests", 429

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], ceventColumns))
                                        , type=str).split(",")

    orderBy = request.args.get('orderBy', default="CASE_NUMBER", type=str)

    order = request.args.get('order', default="ASC", type=str)

    filters = []

    for i in ceventColumns:
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

    countQuery = f"SELECT COUNT(*) FROM Cevent {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requestedcolumns)} FROM CEVENT {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {orderBy} {order} LIMIT {(pagenumber - 1)*rowperpage}, {rowperpage}"

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


@app.route('/getCevent/<int:case_number>')
def getCeventsInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM CEVENT WHERE CASE_NUMBER = {case_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getCevent/<int:case_number>/<int:event_number>')
def getCevent(case_number, event_number):
    results = db.executeSQLQuery(f"SELECT * FROM CEVENT WHERE CASE_NUMBER = {case_number} AND EVENT_NUMBER = {event_number}").fetchall()[0]
    response = make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/addCevent', methods=['POST'])
def addCevent():
    data = request.form
    query = f"INSERT INTO CEVENT ({', '.join([i['name'] for i in ceventColumns])}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    print(tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "VARCHAR" else int(data[i["name"]])) for i in ceventColumns]))
    db.executeSQLQuery(query, tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "VARCHAR" else int(data[i["name"]])) for i in ceventColumns]))
    return "OK", 204


@app.route('/updateCevent', methods=['POST'])
def updateCevent():
    data = dict(request.form)
    for i in data.keys():
        if data[i] == "NULL" or data[i] == "":
            data[i] = None
    db.executeSQLQuery(f"UPDATE CEVENT SET VEHICLE_NUMBER_1 = ?, AREA_OF_IMPACT_1 = ?, SEQUENCE_OF_EVENTS = ?,VEHICLE_NUMBER_2 = ?, AREA_OF_IMPACT_2 = ? WHERE CASE_NUMBER = ? AND EVENT_NUMBER = ?",
                       (int(data["VEHICLE_NUMBER_1"]) if data["VEHICLE_NUMBER_1"] else None, data["AREA_OF_IMPACT_1"], data["SEQUENCE_OF_EVENTS"], int(data["VEHICLE_NUMBER_2"]) if data["VEHICLE_NUMBER_2"] else None, data["AREA_OF_IMPACT_2"], int(data["CASE_NUMBER"]), int(data["EVENT_NUMBER"])))
    return "OK", 204


@app.route('/deleteCevent/<int:case_number>/<int:event_number>', methods=['DELETE'])
def deleteCevent(case_number, event_number):
    db.executeSQLQuery(f"DELETE FROM CEVENT WHERE CASE_NUMBER = ? AND EVENT_NUMBER = ?", (case_number, event_number))
    return "OK", 204

