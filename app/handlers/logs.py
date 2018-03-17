import flask

from app import app
from app import users

from ..repositories import logs

def log_form():
    app.logger.info(flask.request.form)
    logs.log(users.current_user_id(), flask.request.form)
    return flask.redirect(flask.url_for('home'))