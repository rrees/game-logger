from uuid import uuid4

from app import app

from . import connection

log_insert = """
INSERT INTO game_logs (
    log_id,
    user_id,
    game_name,
    date_played,
    tags,
    notes
)
VALUES (
    %(log_id)s,
    %(user_id)s,
    %(game_name)s,
    %(date_played)s,
    %(tags)s,
    %(notes)s
)
"""

def log(log_data):
    app.logger.info(log_data)
    log_id = uuid4()
    return None