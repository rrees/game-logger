from google.appengine.ext import ndb

class Configuration(ndb.Model):
	value = ndb.StringProperty(required=True)

class LogEntry(ndb.Model):
	game_name = ndb.StringProperty(required=True)
	date_played = ndb.DateProperty(required=True, auto_now_add=True)