from __main__ import app, db

from flask import make_response
import TableConverters.PersonTableConverter as PersonTableConverter
@app.route("/test")
def test():
    return "test"

if db.executeSQLQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='PERSON'").fetchall() == []:
    PersonTableConverter.createAndFillPeopleTable(db)
