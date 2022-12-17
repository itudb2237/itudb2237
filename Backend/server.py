from flask import Flask
import sqlite3
from Database import Database

if __name__ == "__main__":
    app = Flask(__name__)

    db = Database("database.db")

    import login
    import personapi
    import ceventapi
    import parkworkapi

    app.run(host='0.0.0.0', port=5000)


