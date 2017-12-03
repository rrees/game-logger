db-migrate:
	yoyo apply --database `echo ${DATABASE_URL}`
