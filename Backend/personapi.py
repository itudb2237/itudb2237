from __main__ import app, db

from flask import make_response, request
import TableConverters.PersonTableConverter as PersonTableConverter


@app.route('/getPeople')
def getPeople():

    rowperpage = request.args.get('rowPerPage', default=100, type=int)

    pagenumber = request.args.get('pageNumber', default=1, type=int)

    count = db.executeSQLQuery("SELECT COUNT(*) FROM Person").fetchone()[0]

    results = {
        "data": db.executeSQLQuery(f"SELECT * FROM PERSON LIMIT {(pagenumber - 1)*rowperpage + 1}, {rowperpage}").fetchall(),
        "header": [i[1] for i in db.executeSQLQuery("PRAGMA table_info(PERSON)").fetchall()],
        "maxPageCount": int((count+rowperpage - 1)/rowperpage)
    }
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


if not db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PERSON'").fetchall():
    PersonTableConverter.createAndFillPeopleTable(db)
