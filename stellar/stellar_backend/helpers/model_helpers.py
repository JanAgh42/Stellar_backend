import datetime as dt
import secrets

def token_date():
    return dt.datetime.now() + dt.timedelta(hours = 1)

def generate_name():
    return "User-" + secrets.token_urlsafe(8)