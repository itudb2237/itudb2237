from flask import Flask, render_template
import sqlite3 as sql

connection = sql.connect('pbtable.db')
cursor = connection.cursor()
my_table_rows = cursor.execute("SELECT * FROM PBTYPE").fetchall()
my_header = [description[0].capitalize() for description in cursor.description] # select all headers and capitilaze first


def home_page():
    global my_table_rows, my_header
    return render_template('home.html', rows = my_table_rows, header = my_header, row_num = len(my_table_rows), col_num = len(my_header))

def create_app():
    my_app = Flask(__name__)
    my_app.config.from_object("settings")
    my_app.add_url_rule("/", view_func=home_page)

    return my_app


if __name__ == '__main__':
    app = create_app()
    port = app.config.get("PORT", 8080)
    app.run(host='0.0.0.0', port=port, debug=True)
