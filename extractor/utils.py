import datetime

def utc_timestamp():
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
