
from datetime import datetime

def parseTime(date: datetime):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

def string_normalizer(str: str):
    return str.replace('’s', "'s").replace('∙','-')

def getTime(time: datetime):
    return ('0' if time.hour < 10 else '') + str(time.hour) +':'+ ('0' if time.minute < 10 else '') + str(time.minute)

def getDate(time: datetime):
    return ('0' if time.day < 10 else '') + str(time.day) +'.'+ ('0' if time.month < 10 else '') + str(time.month) +'.'+str(time.year)

def getWeekday(time: datetime):
    if time.weekday() == 0:
        return "Montag"
    if time.weekday() == 1:
        return "Dienstag"
    if time.weekday() == 2:
        return "Mittwoch"
    if time.weekday() == 3:
        return "Donnerstag"
    if time.weekday() == 4:
        return "Freitag"
    if time.weekday() == 5:
        return "Samstag"
    if time.weekday() == 6:
        return "Sonntag"