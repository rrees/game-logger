import datetime

from google.appengine.ext import ndb

import models

def last(user, datetime_limit):
	return models.LogEntry.query(models.LogEntry.user == user).filter(models.LogEntry.date_played >= datetime_limit).order(-models.LogEntry.date_played)

def last_thirty_days(user):
	return last(user, datetime.datetime.now() - datetime.timedelta(days=30))