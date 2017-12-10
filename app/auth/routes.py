from . import handlers

all = [
    ('/login/sent', 'login_sent', handlers.login_sent, ['GET']),
    ('/login/problem', 'login_problem', handlers.login_problem, ['GET']),
    ('/forms/login', 'login_form', handlers.login_form, ['POST']),
    ('/login/<login_token>', 'auth_confirmation', handlers.confirmation, ['GET']),
]