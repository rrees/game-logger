import os
from urllib import parse
import psycopg2
import psycopg2.extras

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

psycopg2.extras.register_uuid()

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
