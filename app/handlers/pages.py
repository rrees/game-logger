import datetime
import functools

import flask

from app import app
from app import users


def front_page():
    # app.logger.info(flask.session.keys())
    if "session_id" in flask.session and users.current_user_id():
        return flask.redirect(flask.url_for("home"))

    return flask.render_template("index.html")


def home_page():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("home.html", today=datetime.date.today().isoformat())


def add_log():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    return flask.render_template(
        "add-log.html", today=datetime.date.today().isoformat()
    )


@functools.cache
def create_years_list(current_year: int):
    first_year = 2016

    return [str(y) for y in range(current_year, first_year - 1, -1)]


def years():
    if not "session_id" in flask.session:
        return flask.redirect(flask.url_for("index"))

    current_year = datetime.date.today().year

    years = create_years_list(current_year)

    return flask.render_template("years.html", years=years)
