from flask import Flask, render_template
import sqlite3
from Database import Database


if __name__ == "__main__":
    app = Flask(__name__)

    db = Database("database.db")

    statement = """CREATE TABLE IF NOT EXISTS LOG (
        IP VARCHAR(20) NOT NULL,
        DATE_TIME DATETIME NOT NULL
    )"""
    db.executeSQLQuery(statement)

    import parkworkapi, veh_auxapi, pbtypeapi, personapi, ceventapi, vehicleapi, accidentsapi

    @app.route("/", defaults={'path': ''})
    @app.route("/<path:path>")
    def page(path):
        return render_template("index.html")

    app.run(host='0.0.0.0', port=5000, debug=True)


