import logging
import os
import uuid
import hashlib

import flask
import requests

from app import app
from app.config import config, allowed_emails

from . import emails
from app.keys import login_key, session_key, user_key

def login_form():
    email = flask.request.form.get("email")
    #app.logger.info(email)

    if email not in config.allowed_emails:
        return flask.redirect(flask.url_for('login_problem'))

    #app.logger.info(app.redis)

    # Generate login token
    login_token = uuid.uuid4()
    app.logger.info(login_token)

    # Save login token
    app.redis.hmset(login_key(login_token), {"email": email})
    app.redis.expire(login_key(login_token), 120)

    app.logger.info(app.redis.hgetall(login_key(login_token)))

    # Send email
    send_result = emails.send_login(email, login_token)

    if not send_result:
        return flask.redirect(flask.url_for('login_problem'))

    return flask.redirect(flask.url_for('login_sent'))

def confirmation(login_token):
    app.logger.info(login_token)

    # Check token

    login_data = app.redis.hgetall(login_key(login_token))
    app.logger.info(login_data)
    app.logger.info(login_data.keys())

    if not "email" in login_data:
        app.logger.warning("Email not found in login request")
        return flask.redirect('/')
    
    # Turn token into session
    session_id = uuid.uuid4()
    app.redis.hmset(session_key(session_id), {"email": login_data.get("email")})

    app.logger.info(session_id)

    flask.session['session_id'] = session_id
    flask.session.permanent = True

    return flask.redirect(flask.url_for('home'))

def login_sent():
	return flask.render_template('login/sent.html')


def login_problem():
	return flask.render_template('login/problem.html')