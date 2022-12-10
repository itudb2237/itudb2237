import sqlite3


class Database:
    def __init__(self, db):
        self.db = db
    def executeSQLQuery(self, query):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            return cursor
