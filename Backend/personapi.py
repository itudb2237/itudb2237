from __main__ import app, db

from flask import make_response, request
from iprequestchecker import requestchecker
import TableConverters.PersonTableConverter as PersonTableConverter

personColumns = [{"name": i[1], "type": "CHAR" if i[2].startswith("CHAR") else i[2]}
                 for i in db.executeSQLQuery("PRAGMA table_info(PERSON)").fetchall()]

for i in personColumns:
    if i["name"] in ["SEX", "PERSON_TYPE", "INJURY_SEVERITY", "SEATING_POSITION"]:
        i["possibleValues"] = db.executeSQLQuery(f"SELECT DISTINCT {i['name']} FROM PERSON ORDER BY {i['name']};").fetchall()
        if i["possibleValues"][0] == (None,):
            i["possibleValues"][0] = ("NULL",)
        else:
            i["possibleValues"].insert(0, ("NULL",))
        i["possibleValues"].insert(1, ("NOT NULL",))
        i["possibleValues"].insert(0, ("All Values",))

print(personColumns)

@app.route('/getPersonHeader', methods=['GET'])
def getHeaders():
    response = make_response(personColumns)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPeople', methods=['GET'])
def getPeople():
#    if not requestchecker(request.remote_addr, db):
#        return "Too many requests", 429

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], personColumns))
                                        , type=str).split(",")

    orderBy = request.args.get('orderBy', default="CASE_NUMBER", type=str)

    order = request.args.get('order', default="ASC", type=str)

    filters = []

    for i in personColumns:
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

    countQuery = f"SELECT COUNT(*) FROM Person {'WHERE ' + filters if len(filters)>0 else ''}"

    print(countQuery)

    count = db.executeSQLQuery(countQuery).fetchone()[0]

    query = f"SELECT {', '.join(requestedcolumns)} FROM PERSON {'WHERE ' + filters if len(filters)>0 else ''} ORDER BY {orderBy} {order} LIMIT {(pagenumber - 1)*rowperpage}, {rowperpage}"

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


@app.route('/getPerson/<int:case_number>')
def getPeopleInCase(case_number):
    results = db.executeSQLQuery(f"SELECT * FROM PERSON WHERE CASE_NUMBER = {case_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPerson/<int:case_number>/<int:vehicle_number>')
def getPeopleInVehicle(case_number, vehicle_number):
    results = db.executeSQLQuery(f"SELECT * FROM PERSON WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPerson/<int:case_number>/<int:vehicle_number>/<int:person_number>')
def getPerson(case_number, vehicle_number, person_number):
    results = db.executeSQLQuery(f"SELECT * FROM PERSON WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number} AND PERSON_NUMBER = {person_number}").fetchall()
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/addPerson', methods=['POST'])
def addPerson():
    data = request.form
    query = f"INSERT INTO PERSON ({', '.join([i['name'] for i in personColumns])}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    print(tuple([data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]]) for i in personColumns]))
    db.executeSQLQuery(query, tuple([data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]]) for i in personColumns]))
    return "OK", 204


@app.route('/updatePerson', methods=['POST'])
def updatePerson():
    data = request.get_json()
    db.executeSQLQuery(f"UPDATE PERSON SET CASE_NUMBER = {data['CASE_NUMBER']}, VEHICLE_NUMBER = {data['VEHICLE_NUMBER']}, PERSON_NUMBER = {data['PERSON_NUMBER']}, AGE = {data['AGE']}")


if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PERSON'").fetchall():
    PersonTableConverter.createAndFillPeopleTable(db)
