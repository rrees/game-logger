import flask

from app import app

def log_form():
    return flask.redirect(flask.url_for('home'))