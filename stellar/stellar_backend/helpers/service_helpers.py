import datetime as dt
import secrets
import pytz

def generate_token():
    return secrets.token_urlsafe(16)

def token_date():
    return get_time() + dt.timedelta(hours = 1)

def get_time():
    return dt.datetime.now(pytz.utc)