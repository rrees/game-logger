import datetime
from uuid import uuid4
import logging

import iso8601

from rrees_tag_manager import tags

from app import app

from . import connection
from . import statements
from app import models


def log(user_id, log_data):
    app.logger.info(log_data)
    log_id = uuid4()
    game_name = log_data["game_name"]
    played_date = iso8601.parse_date(log_data["date_played"])
    log_tags = tags.process(log_data.get("tags", ""))
    notes = log_data.get("notes", None)

    conn = connection.create_connection()
    cur = connection.conn.cursor()
    parameters = {
        "log_id": log_id,
        "user_id": user_id,
        "game_name": game_name,
        "played_on": played_date,
        "tags": log_tags,
        "notes": notes,
    }
    cur.execute(statements.log_insert, parameters)

    cur.close()

    connection.conn.commit()

    return log_id


def map_result(result):
    return models.GameLog(
        id=result[0],
        name=result[1],
        date_played=result[2],
        tags=result[3],
        notes=result[4] if result[4] != None else "",
    )


def list(user_id):

    cursor = connection.conn.cursor()

    cursor.execute(statements.list_user_logs)

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
    cursor = connection.create_connection().cursor()
    cursor.execute(read_user_log, {"log_id": log_id})
    log = cursor.fetchone()
    cursor.close()

    if not log:
        return None

    return map_result(log)


def delete_log(user_id, log_id, unconditional_delete=False):
    statement_parameters = {
        "user_id": user_id,
        "log_id": log_id,
    }
    statement = (
        statements.delete_log if unconditional_delete else statements.delete_user_log
    )
    cursor = connection.conn.cursor()
    result = cursor.execute(statement, statement_parameters)
    cursor.close()
    connection.conn.commit()
    return


def update_log(user_id, log_id, data):
    tag_list = tags.process(data.get("tags", ""))
    logging.info(tag_list)

    statement_parameters = {
        "log_id": log_id,
        "played_on": data.get("date_played"),
        "tags": tag_list,
        "notes": data.get("notes", ""),
    }
    statement = statements.update_log
    cursor = connection.create_connection().cursor()
    result = cursor.execute(statement, statement_parameters)
    cursor.close()

    connection.conn.commit()

    return


def list_by_year(user_id, year):

    conn = connection.create_connection()

    cursor = conn.cursor()

    statement_parameters = {"year": year}

    cursor.execute(statements.list_user_logs_by_year, statement_parameters)

    logs = cursor.fetchall()

    cursor.close()

    return [map_result(l) for l in logs]


def list_by_tag(user_id, tag):

    conn = connection.create_connection()

    cursor = conn.cursor()

    statement_parameters = {
        "tag": tag,
    }

    cursor.execute(statements.list_user_logs_by_tag, statement_parameters)

    logs = cursor.fetchall()

    cursor.close()

    return [map_result(l) for l in logs]
