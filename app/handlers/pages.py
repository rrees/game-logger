import flask

def front_page():
	return flask.render_template('index.html')

def home_page():
	if not 'session_id' in flask.session:
		return flask.redirect(flask.url_for('index'))
	return flask.render_template('home.html')