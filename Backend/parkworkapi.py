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

@app.route('/getParkworks')
def getParkworks():
    num_of_row_per_page = flask.request.args.get('num_of_row_per_page', default=100, type=int)
    page_number = flask.request.args.get('page_number', default=1, type=int)

    count = db.executeSQLQuery("SELECT COUNT(*) FROM PARKWORK").fetchone()[0]

    results = {
        "data": db.executeSQLQuery(f"SELECT * FROM PARKWORK LIMIT {(page_number - 1) * num_of_row_per_page + 1}, {num_of_row_per_page}").fetchall(),
        "header": [i[1] for i in db.executeSQLQuery("PRAGMA table_info(PARKWORK)").fetchall()],
        "maxPageCount": int((count + num_of_row_per_page - 1) / num_of_row_per_page)
    }

    resp = flask.make_response(results)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return resp

if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PARKWORK'").fetchall():
    parkworkTableConverter.createFillTableParkwork(db)