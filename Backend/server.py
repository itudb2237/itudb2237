from flask import Flask, render_template
import sqlite3
from Database import Database


if __name__ == "__main__":
    app = Flask(__name__)

    db = Database("database.db")

    import personapi, pbtypeapi


    @app.route("/", defaults={'path': ''})
    @app.route("/<path:path>")
    def page(path):
        return render_template("index.html")

    app.run(host='0.0.0.0', port=5000, debug=True)

