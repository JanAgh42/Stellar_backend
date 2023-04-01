import datetime as dt
import secrets
import pytz
import bcrypt

def generate_token():
    return secrets.token_urlsafe(16)

def token_date():
    return get_time() + dt.timedelta(hours = 1)

def get_time():
    return dt.datetime.now(pytz.utc)

def generate_hash(password):
    pw_bytes = password.encode("utf-8")

    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")