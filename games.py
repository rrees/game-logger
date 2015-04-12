import logging
import datetime
import models

def log(user, game_name, date_played):
	log_entry = models.LogEntry(user=user, game_name=game_name, date_played=date_played)

	log_entry.put()

	return log_entry

def all_played(user):
	return models.LogEntry.query(models.LogEntry.user == user)