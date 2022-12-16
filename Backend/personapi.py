from __main__ import app, db

from flask import make_response, request
import TableConverters.PersonTableConverter as PersonTableConverter

personFieldNames = [{"name": i[1], "type": "CHAR" if i[2].startswith("CHAR") else i[2]}
                        for i in db.executeSQLQuery("PRAGMA table_info(PERSON)").fetchall()]


@app.route('/getPersonHeader', methods=['GET'])
def getHeaders():
    response = make_response(personFieldNames)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route('/getPeople', methods=['GET'])
def getPeople():

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    requestedcolumns = request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], personFieldNames))
                                        , type=str).split(",")

    filters = ""

    count = db.executeSQLQuery("SELECT COUNT(*) FROM Person").fetchone()[0]

    results = {
        "data": db.executeSQLQuery(
            f"SELECT {', '.join(requestedcolumns)} FROM PERSON {'WHERE ' + filters if len(filters)>0 else ''} LIMIT {(pagenumber - 1)*rowperpage + 1}, {rowperpage}"
        ).fetchall(),
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
    data = request.get_json()
    db.executeSQLQuery(f"INSERT INTO PERSON ( CASE_NUMBER, VEHICLE_NUMBER, PERSON_NUMBER, AGE, SEX, PERSON_TYPE, INJURY_SEVERITY, SEATING_POSITION) VALUES ( {data['CASE_NUMBER']}, {data['VEHICLE_NUMBER']}, {data['PERSON_NUMBER']}, {data['AGE']}, {data['SEX']}, {data['PERSON_TYPE']}, {data['INJURY_SEVERITY']}, {data['SEATING_POSITION']})")
    return "OK"


@app.route('/updatePerson', methods=['POST'])
def updatePerson():
    data = request.get_json()
    db.executeSQLQuery(f"UPDATE PERSON SET CASE_NUMBER = {data['CASE_NUMBER']}, VEHICLE_NUMBER = {data['VEHICLE_NUMBER']}, PERSON_NUMBER = {data['PERSON_NUMBER']}, AGE = {data['AGE']}")


if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PERSON'").fetchall():
    PersonTableConverter.createAndFillPeopleTable(db)
