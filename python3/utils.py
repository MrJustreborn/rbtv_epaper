
from datetime import datetime

def parseTime(date: datetime):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

def string_normalizer(str: str):
    return str.replace('’s', "'s")

def getTime(time: datetime):
    return ('0' if time.hour < 10 else '') + str(time.hour) +':'+ ('0' if time.minute < 10 else '') + str(time.minute)