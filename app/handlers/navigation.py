from dataclasses import dataclass
from functools import wraps

import flask

from app import app, keys

@dataclass
class Navigation:
    label: str
    url: str

def user_required(handler):
    @wraps(handler)
    def decorated_function(*args, **kwargs):
        session_id = flask.session.get('session_id')
        if not session_id or not app.redis.exists(keys.session_key(session_id)):
            return flask.redirect(flask.url_for("index"))

        return handler(*args, **kwargs)

    return decorated_function

@user_required
def logs():
    return flask.render_template("navigation.html", title="Logs")
