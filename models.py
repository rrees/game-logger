from google.appengine.ext import ndb

class Configuration(ndb.Model):
	value = ndb.StringProperty(required=True)

class LogEntry(ndb.Model):
	user = ndb.UserProperty(required=True)
	game_name = ndb.StringProperty(required=True)
	date_played = ndb.DateProperty(required=True, auto_now_add=True)
	tags = ndb.StringProperty(repeated=True)
	notes= ndb.TextProperty()

class Game(ndb.Model):
	name = ndb.StringProperty(required=True)
	description = ndb.TextProperty()
	authors = ndb.StringProperty(repeated=True)
	tags = ndb.StringProperty(repeated=True)