import os
import logging
import datetime
import json

import webapp2
import jinja2

import queries
import games

from google.appengine.api import users

JINJA = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		if user:
			return webapp2.redirect('/home')
		
		template_values = {
			
		}

		template = JINJA.get_template('index.html')
		self.response.write(template.render(template_values))

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		template_values = {
			"today": datetime.date.today().isoformat(),
			"games_logged": queries.period.last_thirty_days(user),
		}

		template = JINJA.get_template('home.html')
		self.response.write(template.render(template_values))

class LogPlay(webapp2.RequestHandler):
	def get(self):

		template_values = {
		}

		template = JINJA.get_template('log.html')
		self.response.write(template.render(template_values))

	def post(self):
		#logging.info(self.request.POST)
		user = users.get_current_user()

		date_played = datetime.datetime.strptime(self.request.POST['date_played'], '%Y-%m-%d').date()

		tags = self.request.POST.get('tags', '').split(',')

		tags = filter(lambda tag: len(tag) > 0, tags)

		notes = self.request.POST.get('notes', None)

		games.log(user, self.request.POST['game_name'], date_played, tags=tags, notes=notes)
		return webapp2.redirect('/home')

class LogsPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		template_values = {
			"games_logged": games.all_played(user),
		}

		template = JINJA.get_template('logs.html')
		self.response.write(template.render(template_values))

class LogPage(webapp2.RequestHandler):
	def get(self, log_id):
		user = users.get_current_user()

		template_values = {
			"log": games.read_log(user, log_id),
		}

		template = JINJA.get_template('log.html')
		self.response.write(template.render(template_values))

	def post(self, log_id):
		user = users.get_current_user()

		date_played = datetime.datetime.strptime(self.request.POST['date_played'], '%Y-%m-%d').date()

		tags = self.request.POST.get('tags', '').split(',')

		tags = filter(lambda tag: len(tag) > 0, tags)

		notes = self.request.POST.get('notes', None)

		games.log(user, self.request.POST['game_name'], date_played, tags=tags, notes=notes, log_id=log_id)

		return webapp2.redirect('/log/'+log_id)

class DeleteLogPage(webapp2.RequestHandler):
	def post(self, log_id):
		games.delete_log(log_id)
		return webapp2.redirect('/logs')

class Export(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'

		user = users.get_current_user()

		all_games = games.all_played(user)

		def to_dict(game_log):
			return {
				"name": game_log.game_name,
				"date_played": game_log.date_played.isoformat(),
				"tags": [tag.strip() for tag in game_log.tags],
				"notes": game_log.notes if game_log.notes else "",
			}

		payload = {
			"message": "Game log exports",
			"games": [to_dict(game) for game in all_games],
		}

		serialised_json = json.dumps(payload)

		self.response.out.write(serialised_json)

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage),
	webapp2.Route(r'/home', handler=HomePage),
	webapp2.Route(r'/log', handler=LogPlay),
	webapp2.Route(r'/logs', handler=LogsPage),
	webapp2.Route(r'/log/<log_id>', handler=LogPage),
	webapp2.Route(r'/log/<log_id>/delete', handler=DeleteLogPage),
	webapp2.Route(r'/export', handler=Export),
	], debug=True)