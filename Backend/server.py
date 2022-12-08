from flask import Flask
import sqlite3 


if __name__ == "__main__":
    app = Flask(__name__)

    db = sqlite3.connect("database.sql")

    import personapi

    app.run(host='0.0.0.0', port=5000)