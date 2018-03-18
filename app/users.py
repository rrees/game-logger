import hashlib

import flask

from app import app
from . import keys

def current_user_email():
    if not 'session_id' in flask.session:
        return None
    
    session_id = flask.session['session_id']
    app.logger.info(session_id)
    emails = app.redis.hmget(keys.session_key(session_id), 'email')

    app.logger.info(emails)

    return emails.pop()

def current_user_id():
    return hashlib.sha256(current_user_email().encode('utf-8')).hexdigest()
