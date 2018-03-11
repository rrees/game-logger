import flask

from app import app

from ..repositories import logs

def log_form():
    app.logger.info(flask.request.form)
    logs.log(flask.request.form)
    return flask.redirect(flask.url_for('home'))