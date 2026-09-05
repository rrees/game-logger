db-migrate:
	yoyo apply --database `echo ${DATABASE_URL}`

serve:
	pipenv run python runserver.py