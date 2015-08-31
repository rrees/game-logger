import os
import logging
import datetime

import webapp2
import jinja2
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
			"games_logged": games.all_played(user),
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

		webapp2.redirect('/log/'+log_id)

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage),
	webapp2.Route(r'/home', handler=HomePage),
	webapp2.Route(r'/log', handler=LogPlay),
	webapp2.Route(r'/logs', handler=LogsPage),
	webapp2.Route(r'/log/<log_id>', handler=LogPage)
	], debug=True)