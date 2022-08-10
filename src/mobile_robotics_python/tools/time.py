from datetime import datetime


def get_utc_stamp():
    epoch = datetime.utcfromtimestamp(0)
    utc_time = datetime.utcnow()
    return (utc_time - epoch).total_seconds()
