import logging
import datetime

from google.appengine.ext import ndb

import models

def read_log(user, log_id):
	return ndb.Key(urlsafe=log_id).get()

def create_new_log(user, game_name, date_played, tags=None, notes=None):
	log_entry = models.LogEntry(user=user, game_name=game_name, date_played=date_played)

	if tags:
		log_entry.tags = tags

	if notes:
		log_entry.notes = notes

	log_entry.put()
	return log_entry

def update_log(user, log_id, game_name, date_played, tags=None, notes=None):
	log_entry = read_log(user, log_id)

	if game_name:
		log_entry.game_name = game_name

	if date_played:
		log_entry.date_played = date_played

	if tags:
		log_entry.tags = tags

	if notes:
		log_entry.notes = notes

	log_entry.put()

	return log_entry

def log(user, game_name, date_played, tags=None, notes=None, log_id=None):
	if not log_id:
		return create_new_log(user, game_name, date_played, tags, notes)
	
	return update_log(user, log_id, game_name, date_played, tags, notes)


def all_played(user):
	return models.LogEntry.query(models.LogEntry.user == user).order(-models.LogEntry.date_played)

def delete_log(log_id):
	return ndb.Key(urlsafe=log_id).delete()