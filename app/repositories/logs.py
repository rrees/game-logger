import datetime
from uuid import uuid4

import iso8601

from app import app

from . import connection

log_insert = """
INSERT INTO game_logs (
    log_id,
    user_id,
    game_name,
    played_on,
    tags,
    notes
)
VALUES (
    %(log_id)s,
    %(user_id)s,
    %(game_name)s,
    %(played_on)s,
    %(tags)s,
    %(notes)s
)
"""

list_user_logs = """
SELECT *
FROM game_logs
"""

def log(user_id, log_data):
    app.logger.info(log_data)
    log_id = uuid4()
    game_name = log_data['game_name']
    played_date = iso8601.parse_date(log_data['date_played'])

    cur = connection.conn.cursor()
    parameters = {
        "log_id": log_id,
        "user_id": user_id,
        "game_name": game_name,
        "played_on": played_date,
        "tags": [],
        "notes": None,
    }
    cur.execute(log_insert, parameters)

    cur.close()

    connection.conn.commit()

    return log_id

def list(user_id):

    cursor = connection.conn.cursor()

    cursor.execute(list_user_logs)

    logs = cursor.fetchall()

    cursor.close()

    return logs