import os
import logging
import datetime

import webapp2
import jinja2


JINJA = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			
		}

		template = JINJA.get_template('index.html')
		self.response.write(template.render(template_values))

class HomePage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			"today": datetime.date.today().isoformat(),
		}

		template = JINJA.get_template('home.html')
		self.response.write(template.render(template_values))

class LogPlay(webapp2.RequestHandler):
	def post(self):
		logging.info(self.request.POST)
		return webapp2.redirect('/home')

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage),
	webapp2.Route(r'/home', handler=HomePage),
	webapp2.Route(r'/log', handler=LogPlay)
	], debug=True)