from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.PBTypeTableConverter as PbtypeTableConverter

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PBTYPE'").fetchall():
    PbtypeTableConverter.createAndFillPBTypeTable()

def get_pbtype_columns():
    pbtypeColumns = [{"name": i[1], "type": "CHAR" if i[2].startswith("CHAR") else i[2]}
                    for i in db.executeSQLQuery("PRAGMA table_info(PBTYPE)").fetchall()]

    for i in pbtypeColumns:
        if i["name"] in ["PERSON_TYPE", "CROSSWALK_PRESENT", "SIDEWALK_PRESENT", "SCHOOLZONE_PRESENT", "MOTOR_MANEUVER"]:
            i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM PBTYPE ORDER BY {i['name']};").fetchall()
            if i["possibleValues"][0] == (None,):
                i["possibleValues"][0] = ("NULL",)
            else:
                i["possibleValues"].insert(0, ("NULL",))
            i["possibleValues"].insert(1, ("NOT NULL",))
            i["possibleValues"].insert(0, ("All Values",))
    
    return pbtypeColumns

pbtypeColumns = get_pbtype_columns()
print(pbtypeColumns)


@app.route('/getPbtypeHeader', methods=['GET'])
def getPbtypeHeaders():
    if not requestchecker(request.remote_addr, db):
        return "Too many requests", 429
        
    response = make_response(pbtypeColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/getPbtypes', methods=['GET'])
def get_pbtypes():
    # Get query parameters
    row_per_page = request.args.get('rowPerPage', default=100, type=int)
    page_number = request.args.get('pageNumber', default=1, type=int)
    requested_columns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], pbtypeColumns))
                                        , type=str).split(",")
    order_by = request.args.get('orderBy', default="CASE_NUMBER", type=str)
    order = request.args.get('order', default="ASC", type=str)

    # Build list of filters
    filters = []
    for column in pbtypeColumns:
        current_filter = request.args.get('filter'+column["name"], default="", type=str)
        if current_filter == "NULL":
            filters.append(column["name"] + " IS NULL")
        elif current_filter == "NOT NULL":
            filters.append(column["name"] + " IS NOT NULL")
        elif current_filter == "All Values":
            continue
        elif current_filter:
            if column["type"] == "CHAR":
                if "possibleValues" in column:
                    filters.append(column["name"] + " == \"" + current_filter + "\"")
                else:
                    filters.append(column["name"] + " LIKE \"" + current_filter + "%\"")
            elif column["type"] == "INTEGER":
                range_of_value = current_filter.split(",")
                if range_of_value[0] and range_of_value[1]:
                    filters.append(column["name"] + " BETWEEN " + range_of_value[0] + " AND " + range_of_value[1])
                elif range_of_value[1]:
                    filters.append(column["name"] + " <= " + range_of_value[1])
                else:
                    filters.append(column["name"] + " >= " + range_of_value[0])

    # Join filters with AND
    filters = " AND ".join(filters)

    # Build count query
    countQuery = f"SELECT COUNT(*) FROM Pbtype {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requested_columns)} FROM PBTYPE {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {order_by} {order} LIMIT {(page_number - 1)*row_per_page}, {row_per_page}"

    print(query)

    results = {
        "data": db.executeSQLQuery(query).fetchall(),
        "maxPageCount": int((count+row_per_page - 1)/row_per_page)
    }
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPbtype/<int:case_number>')
def getPbtypesInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM PBTYPE WHERE CASE_NUMBER = {case_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPbtype/<int:case_number>/<int:vehicle_number>')
def getPbtypesInVehicle(case_number, vehicle_number):
    results = db.executeSQLQuery(f"SELECT * FROM PBTYPE WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPbtype/<int:case_number>/<int:vehicle_number>/<int:person_number>')
def getPbtype(case_number, vehicle_number, person_number):
    results = db.executeSQLQuery(f"SELECT * FROM PBTYPE WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number} AND PERSON_NUMBER = {person_number}").fetchall()[0]
    response = make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/addPbtype', methods=['POST'])
def addPbtype():
    data = request.form
    query = f"INSERT INTO PBTYPE ({', '.join([i['name'] for i in pbtypeColumns])}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    print(tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in pbtypeColumns]))
    db.executeSQLQuery(query, tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in pbtypeColumns]))
    return "OK", 204


@app.route('/updatePbtype', methods=['POST'])
def updatePbtype():
    data = dict(request.form)
    for i in data.keys():
        if data[i] == "NULL" or data[i] == "":
            data[i] = None
    db.executeSQLQuery("UPDATE PBTYPE SET PERSON_TYPE = ?, CROSSWALK_PRESENT = ?, SIDEWALK_PRESENT = ?,SCHOOLZONE_PRESENT = ?, MOTOR_MANEUVER = ? WHERE CASE_NUMBER = ? AND VEHICLE_NUMBER = ? AND PERSON_NUMBER = ?",
                       (data["PERSON_TYPE"], data["CROSSWALK_PRESENT"], data["SIDEWALK_PRESENT"], data["SCHOOLZONE_PRESENT"], data["MOTOR_MANEUVER"], int(data["CASE_NUMBER"]), int(data["VEHICLE_NUMBER"]), int(data["PERSON_NUMBER"])))
    return "OK", 204


@app.route('/deletePbtype/<int:case_number>/<int:vehicle_number>/<int:person_number>', methods=['DELETE'])
def deletePbtype(case_number, vehicle_number, person_number):
    db.executeSQLQuery("DELETE FROM PBTYPE WHERE CASE_NUMBER = ? AND VEHICLE_NUMBER = ? AND PERSON_NUMBER = ?", (case_number, vehicle_number, person_number))
    return "OK", 204


