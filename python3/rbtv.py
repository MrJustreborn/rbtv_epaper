
import rbtv_config
import rbtv_printer

import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
import json
from io import BytesIO

class RBTV:
    def __init__(self):
        self.fontSmal = rbtv_config.fontSmal
        self.fontBig = rbtv_config.fontBig
        self.width = rbtv_config.screen_width
        self.height = rbtv_config.screen_height
        self.live = rbtv_config.live
        self.neu = rbtv_config.neu
    
    def getRBData(self, today: datetime):
        print(today)

        withouttime = datetime(today.year, today.month, today.day)
        timestamp = datetime.timestamp(withouttime)
        withouttime = datetime(today.year, today.month, today.day + 2)
        timestamp2 = datetime.timestamp(withouttime)

        print(int(timestamp), int(timestamp2))

        req = 'https://api.rocketbeans.tv/v1/schedule/normalized?startDay=' +str(int(timestamp))+ '&endDay=' +str(int(timestamp2))
        print(req)
        r = requests.get(req)
        data = json.loads(r.text)
        print(data['success'])
        return data
    
    def parseTime(self, date):
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_screen(self) -> Image:
        today = datetime.today()
        data = self.getRBData(today)

        img = Image.new('1', (self.width, self.height), 255)
        
        draw = ImageDraw.Draw(img)
        draw.text((40,30), rbtv_printer.getTime(today), font = self.fontBig, fill = 0)
        #draw.text((10,100), str(today.day) +'. '+ str(today.month) +'. '+ str(today.year), font = font24, fill = 0)
        #logo = Image.open('/home/mrjustreborn/Dev/PI/epaper/Cornerlogo_rbtv_151152.bmp')
        #img.paste(logo,  (0,0))

        print(self.parseTime(data['data'][0]['date']))
        #shows = data['data'][0]['elements']

        shows = []

        for i in range(len(data['data'])):
            for s in data['data'][i]['elements']:
                shows.append(s)

        print(len(shows))

        pos = 0
        hasCurrent = False
        for i in range(len(shows)):
            timeStart = self.parseTime(shows[i]['timeStart']) + timedelta(hours=2)
            timeEnd = self.parseTime(shows[i]['timeEnd']) + timedelta(hours=2)

            if timeEnd < today:
                continue

            if timeStart < today and timeEnd > today and not hasCurrent:
                print(shows[i]['title'], i)
                rbtv_printer.printCurrent(img, draw, shows[i], timeStart, timeEnd, today, self.fontSmal)
                hasCurrent = True # sometimes shows overlap a few minutes
                continue

            width, height = draw.textsize(rbtv_printer.getTime(timeStart), font=self.fontSmal)
            title = rbtv_printer.string_normalizer(str(shows[i]['title']))
            draw.text((10 + 10 + width, 35 * pos + 230), rbtv_printer.getTime(timeStart) +' '+ title, font = self.fontSmal, fill = 0)

            if shows[i]['type'] == 'premiere':
                img.paste(self.neu, (10, 35 * pos + 230))
            elif shows[i]['type'] == 'live':
                img.paste(self.live, (10, 35 * pos + 230))

            pos += 1
            if pos > 5:
                break
        return img