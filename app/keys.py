import hashlib

from app.config import config

app_key = config.get("app_name")

def login_key(login_token):
    return f"{app_key}:login:{login_token}"

def session_key(session_id):
    return f"{app_key}:session:{session_id}"

def user_key(email):
    email_hash = hashlib.md5(email).hexdigest()
    return f"{app_key}:user:{email_hash}"