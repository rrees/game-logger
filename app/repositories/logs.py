import datetime
from uuid import uuid4

import iso8601

from app import app

from . import connection
from . import statements
from app import models

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
SELECT
    log_id,
    game_name,
    played_on,
    tags,
    notes
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

def map_result(result):
    return models.GameLog(
        id = result[0],
        name = result[1],
        log_date = result[2],
        tags = result[3],
        notes = result[4],
    )

def list(user_id):

    cursor = connection.conn.cursor()

    cursor.execute(list_user_logs)

    logs = cursor.fetchall()

    cursor.close()

    return [map_result(l) for l in logs]

read_user_log = """
SELECT
    log_id,
    game_name,
    played_on,
    tags,
    notes
FROM game_logs
WHERE log_id = %(log_id)s
"""

def read_log(user_id, log_id):
    cursor = connection.conn.cursor()
    cursor.execute(read_user_log,
        {'log_id': log_id})
    log = cursor.fetchone()
    cursor.close()
    
    if not log:
        return None
    
    return map_result(log)


def delete_log(user_id, log_id, unconditional_delete=False):
    statement_parameters = {
        'user_id': user_id,
        'log_id': log_id,
    }
    statement = statements.delete_log if unconditional_delete else statements.delete_user_log
    cursor = connection.conn.cursor()
    result = cursor.execute(statement, statement_parameters)
    cursor.close()
    connection.conn.commit()
    return