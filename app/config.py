import os

allowed_emails = os.environ.get("ALLOWED_EMAILS", '').split(',')

config = {
    "login": {
        "DEV": {
            "login_prefix": "http://localhost:4545"
        },
        "PROD": {
            "login_prefix": "https://heroku-game-logger.herokuapp.com"
        }
    },
    "app_name": "game-logger",
    "allowed_emails": allowed_emails,
}