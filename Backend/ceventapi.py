from __main__ import app
from __main__ import db as database

from flask import make_response, request
import TableConverters.CeventTableConverter as CeventTableConverter


@app.route('/getCevents')
def getCevents():

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    count = database.executeSQLQuery("SELECT COUNT(*) FROM CEVENT").fetchone()[0]

    results = {
        "data": database.executeSQLQuery(f"SELECT * FROM CEVENT LIMIT {(pagenumber - 1)*rowperpage + 1}, {rowperpage}").fetchall(),
        "header": [i[1] for i in database.executeSQLQuery("PRAGMA table_info(CEVENT)").fetchall()],
        "maxPageCount": int((count+rowperpage - 1)/rowperpage)
    }
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


#if not database.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='CEVENT'").fetchall():
CeventTableConverter.createAndFillCeventTable(database)
