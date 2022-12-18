from __main__ import app, db

import flask
import TableConverters.parkworkTableConverter as parkworkTableConverter


parkwork_attributes = []
query_result = db.executeSQLQuery("PRAGMA table_info(PARKWORK)").fetchall()

for row in query_result:
    name = row[1]
    data_type = row[2]
    
    if data_type.startswith("CHAR"):
        data_type = "CHAR"
        
    attribute = {"name": name, "type": data_type}
    parkwork_attributes.append(attribute)

@app.route('/getParkworkHeader', methods=['GET'])
def getHeadersParkwork():
    response = flask.make_response(parkwork_attributes)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/getParkworks', methods=['GET'])
def getParkworks():
    num_of_row_per_page = flask.request.args.get('rowPerPage', default=100, type=int)
    page_number = flask.request.args.get('pageNumber', default=1, type=int)
    requested_columns = flask.request.args.get('requestedColumns', default=",".join(map(lambda x: x["name"], parkwork_attributes)), type=str).split(",")
    orderBy = flask.request.args.get('orderBy', default="CASE_NUMBER", type=str)
    order = flask.request.args.get('order', default="AZB", type=str)

    particular_CASE_NUMBER = -1
    particular_VEHICLE_NUMBER = -1
    list_of_FIRST_HARMFUL_EVENT = []
    list_of_CARGO_BODY_TYPE = []
    list_of_SPECIAL_USE = []
    list_of_EXTENT_OF_DAMAGE = []
    min_max_DEATHS = []

    filters = []

    
    for i in parkwork_attributes:
        current_filter = flask.request.args.get('filter' + i["name"], default="", type=str)
        if (current_filter == ""):
                continue
        else:
            if (i["name"] == "SPECIAL_USE"):
                list_of_SPECIAL_USE = current_filter.split(',')
            elif (i["name"] == "FIRST_HARMFUL_EVENT"):
                list_of_FIRST_HARMFUL_EVENT = current_filter.split(',')
            elif (i["name"] == "CARGO_BODY_TYPE"):
                list_of_CARGO_BODY_TYPE = current_filter.split(',')
            elif (i["name"] == "EXTENT_OF_DAMAGE"):
                list_of_EXTENT_OF_DAMAGE = current_filter.split(',')
            elif (i["name"] == "CASE_NUMBER"):
                temp = current_filter.split(',')
                particular_CASE_NUMBER = int(temp[0])
            elif (i["name"] == "VEHICLE_NUMBER"):
                temp = current_filter.split(',')
                particular_VEHICLE_NUMBER = int(temp[0])
            elif (i["name"] == "DEATHS"):
                temp = current_filter.split(',')
                min_max_DEATHS.append(int(temp[0]))
                min_max_DEATHS.append(int(temp[1]))                  

    count = db.executeSQLQuery("SELECT COUNT(*) FROM PARKWORK").fetchone()[0]

    statement = f"SELECT * FROM PARKWORK"
    and_clause = False
    additional_statement = ""

    if (len(list_of_CARGO_BODY_TYPE) != 0 or len(list_of_EXTENT_OF_DAMAGE) != 0 or len(list_of_FIRST_HARMFUL_EVENT) != 0 or len(list_of_SPECIAL_USE) != 0 or len(min_max_DEATHS) == 2 or particular_CASE_NUMBER != -1 or particular_VEHICLE_NUMBER != -1):
        additional_statement += " WHERE ("
        if (len(list_of_FIRST_HARMFUL_EVENT) != 0):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += "(FIRST_HARMFUL_EVENT = " + " OR FIRST_HARMFUL_EVENT = ".join([f"\"{str(i)}\"" for i in set(list_of_FIRST_HARMFUL_EVENT)]) + ")"
        if (len(list_of_CARGO_BODY_TYPE) != 0):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement+= "(CARGO_BODY_TYPE = " + " OR CARGO_BODY_TYPE = ".join([f"\"{str(i)}\"" for i in set(list_of_CARGO_BODY_TYPE)]) + ")"
        if (len(list_of_SPECIAL_USE) != 0):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += " (SPECIAL_USE = " + " OR SPECIAL_USE = ".join([f"\"{str(i)}\"" for i in set(list_of_SPECIAL_USE)]) + ")"
        if (len(list_of_EXTENT_OF_DAMAGE) != 0):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += "(EXTENT_OF_DAMAGE = " + " OR EXTENT_OF_DAMAGE = ".join([f"\"{str(i)}\"" for i in set(list_of_EXTENT_OF_DAMAGE)]) + ")"
        if (particular_CASE_NUMBER != -1):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += f"(CASE_NUMBER = {particular_CASE_NUMBER})"
        if (particular_VEHICLE_NUMBER != -1):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += f"(VEHICLE_NUMBER = {particular_VEHICLE_NUMBER})"
        if (len(min_max_DEATHS) == 2):
            if (and_clause):
                additional_statement+= " AND "
            else:
                and_clause = True
            additional_statement += f"(DEATHS > {min_max_DEATHS[0] - 1} AND DEATHS < {min_max_DEATHS[1] + 1})"
        additional_statement += ")"

    additional_statement += f" ORDER BY {orderBy}"            

    results = {
        "data": db.executeSQLQuery(statement + additional_statement +  f" LIMIT {(page_number - 1) * num_of_row_per_page}, {num_of_row_per_page}").fetchall(),
        "header": [i[1] for i in db.executeSQLQuery("PRAGMA table_info(PARKWORK)").fetchall()],
        "maxPageCount": int((count + num_of_row_per_page - 1) / num_of_row_per_page)
    }

    resp = flask.make_response(results)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp



@app.route('/getParkwork/<int:case_number>/<int:vehicle_number>')
def getParkwork(case_number, vehicle_number):
    results = db.executeSQLQuery(f"SELECT * FROM PARKWORK WHERE CASE_NUMBER = {case_number} AND VEHICLE_NUMBER = {vehicle_number}").fetchall()[0]
    response = flask.make_response(list(results))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/addParkwork', methods=['POST'])
def addParkwork():
    data = flask.request.form
    query = f"INSERT INTO PARKWORK ({', '.join([i['name'] for i in parkwork_attributes])}) VALUES (?, ?, ?, ?, ?, ?, ?)"
    print(tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in parkwork_attributes]))
    db.executeSQLQuery(query, tuple([None if data[i["name"]] == "NULL" or data[i["name"]] == "" else (data[i["name"]] if i["type"] == "CHAR" else int(data[i["name"]])) for i in parkwork_attributes]))
    return "OK", 204



if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PARKWORK'").fetchall():
    parkworkTableConverter.createFillTableParkwork(db)