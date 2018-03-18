import flask

from app import app
from app import users

from ..repositories import logs

def log_form():
    app.logger.info(flask.request.form)
    logs.log(users.current_user_id(), flask.request.form)
    return flask.redirect(flask.url_for('home'))

def list():
    user_id = users.current_user_id()

    if not user_id:
        return flask.redirect(flask.url_for('index'))

    all_logs = logs.list(user_id)

    return flask.render_template('list.html', logs=all_logs)