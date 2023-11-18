import datetime as dt
import secrets
import pytz

def token_date():
    return get_time() + dt.timedelta(hours = 1)

def generate_name():
    return "User-" + secrets.token_urlsafe(8)

def get_time():
    return dt.datetime.now(pytz.utc)