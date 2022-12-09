from __main__ import app, db

from flask import make_response
import TableConverters.PersonTableConverter as PersonTableConverter


@app.route('/getPeople')
def hello():

    count = db.executeSQLQuery("SELECT COUNT(*) FROM Person").fetchone()[0]

    results = {
        "data": db.executeSQLQuery("SELECT * FROM PERSON LIMIT 100").fetchall(),
        "header": [i[1] for i in db.executeSQLQuery("PRAGMA table_info(PERSON)").fetchall()],
        "maxPageCount": int((count+99)/100)
    }
    response = make_response(results)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

if db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PERSON'").fetchall() == []:
    PersonTableConverter.createAndFillPeopleTable(db)
