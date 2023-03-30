import datetime as dt
import secrets

def generate_token():
    return secrets.token_urlsafe(16)

def token_date():
    return dt.datetime.now() + dt.timedelta(hours = 1)