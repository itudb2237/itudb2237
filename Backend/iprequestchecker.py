from datetime import datetime, timedelta
from Database import Database

def requestchecker(ip, db):
    current_time = datetime.now()
    one_minute_before = current_time - timedelta(minutes=1)

    statement = f"INSERT INTO LOG VALUES ('{ip}', '{current_time}')"

    db.executeSQLQuery(statement)

    statement = f"""SELECT COUNT(*) FROM LOG 
    WHERE (DATE_TIME BETWEEN '{one_minute_before}' AND '{current_time}')
    GROUP BY IP HAVING (IP = '{ip}');"""

    cursor = db.executeSQLQuery(statement)
    num_of_req = cursor.fetchall()
    num_of_req = num_of_req[0][0]

    if (num_of_req >= 30):
        return False
    else:
        return True