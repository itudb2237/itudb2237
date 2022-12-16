import sqlite3


class Database:
    def __init__(self, db):
        self.db = db

    def executeSQLQuery(self, query, values=()):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            return cursor
