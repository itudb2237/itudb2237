from flask import Flask
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

    import personapi
    import parkworkapi

    app.run(host='0.0.0.0', port=5000)