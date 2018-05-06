import flask

def import_logs():
    return flask.render_template('import.html')

def import_logs_form():
    current_user_id = users.current_user_id()

    return flask.redirect(flask.url_for('logs_listing'))