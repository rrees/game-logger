
from . import connection

from .. import app

_LOG = app.logger

def log(log_data):
    _LOG.info(log_data)
    return None