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
    system = log_data.get("system", None)

    with connection.create_connection() as conn:
        with conn.cursor() as cur:
            parameters = {
                "log_id": log_id,
                "user_id": user_id,
                "game_name": game_name,
                "played_on": played_date,
                "tags": log_tags,
                "notes": notes,
                "system": system,
            }
            cur.execute(statements.log_insert, parameters)
            conn.commit()

    return log_id


def map_result(result):
    return models.GameLog(
        id=result[0],
        game_name=result[1],
        date_played=result[2],
        tags=[t for t in result[3] if t],
        notes=result[4] if result[4] != None else "",
        system=result[5] if result[5] != None else "",
    )


def list(user_id):

    with connection.create_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(statements.list_user_logs)

            logs = cursor.fetchall()

    return [map_result(l) for l in logs]


def read_log(user_id, log_id):
    with connection.create_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute(statements.read_user_log, {"log_id": log_id})
            log = cursor.fetchone()

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
    with connection.connect() as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(statement, statement_parameters)
            conn.commit()
    
    return


def update_log(user_id, log_id, data):
    tag_list = tags.process(data.get("tags", ""))
    logging.info(tag_list)

    statement_parameters = {
        "log_id": log_id,
        "game_name": data.get("game_name"),
        "played_on": data.get("date_played"),
        "tags": tag_list,
        "notes": data.get("notes", ""),
        "system": data.get("system", ""),
    }

    statement = statements.update_log

    with connection.create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(statement, statement_parameters)
            conn.commit()

    return


def list_by_year(user_id, year):

    with connection.create_connection() as conn:
        with conn.cursor() as cursor:

            statement_parameters = {"year": year}

            cursor.execute(statements.list_user_logs_by_year, statement_parameters)

            logs = cursor.fetchall()

    return [map_result(l) for l in logs]


def list_by_tag(user_id, tag):

    with connection.create_connection() as conn:

        with conn.cursor() as cursor:

            statement_parameters = {
                "tag": tag,
            }

            cursor.execute(statements.list_user_logs_by_tag, statement_parameters)

            logs = cursor.fetchall()

    return [map_result(l) for l in logs]

def recent_logs(maximum_logs=100):
    with connection.create_connection() as conn:
        with conn.cursor() as cursor:
            statement_parameters = {
                "limit": maximum_logs,
            }

            cursor.execute(statements.recent_user_logs, statement_parameters)

            logs = cursor.fetchall()

    return [map_result(l) for l in logs]