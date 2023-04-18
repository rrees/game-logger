import os
from urllib import parse
import psycopg

parse.uses_netloc.append("postgres")
DB_URL = os.environ["DATABASE_URL"]
url = parse.urlparse(DB_URL)

def create_connection():
    return psycopg.connect(DB_URL)
