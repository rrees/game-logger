import json

import flask

from rrees_tag_manager import tags

from app import users
from app.repositories import logs

def import_logs():
    return flask.render_template('import.html')

def import_logs_form():
    current_user_id = users.current_user_id()

    json_data = json.loads(flask.request.form.get('import_data'))

    for game in json_data.get('games', []):
        log_data = {}
        log_data.update(game)
        log_data.update({
            "game_name": game['name'],
            "tags": tags.as_string(game['tags']),
        })
        logs.log(current_user_id, log_data)

    return flask.redirect(flask.url_for('logs_listing'))