
from datetime import datetime,timedelta

import requests
import json

def getRBData(today: datetime):
    print(today)

    yesterday = today + timedelta(days = -1)
    tomorrow = today + timedelta(days = 1)

    withouttime = datetime(yesterday.year, yesterday.month, yesterday.day)
    timestamp = datetime.timestamp(withouttime)
    withouttime = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    timestamp2 = datetime.timestamp(withouttime)

    print(int(timestamp), int(timestamp2))

    req = 'https://api.rocketbeans.tv/v1/schedule/normalized?startDay=' +str(int(timestamp))+ '&endDay=' +str(int(timestamp2))
    print(req)
    r = requests.get(req)
    data = json.loads(r.text)
    print(data['success'])
    return data

def getRBViews():
    req = 'https://api.rocketbeans.tv/StreamCount'
    print(req)
    r = requests.get(req)
    data = json.loads(r.text)
    print(data['success'])
    return data