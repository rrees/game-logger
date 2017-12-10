import flask

from app import app

def front_page():
	app.logger.info(flask.session.keys())
	if 'session_id' in flask.session:
		return flask.redirect(flask.url_for('home'))

	return flask.render_template('index.html')

def home_page():
	if not 'session_id' in flask.session:
		return flask.redirect(flask.url_for('index'))

	return flask.render_template('home.html')