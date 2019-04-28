
import rbtv.rbtv_config as rbtv_config
import rbtv.rbtv_printer as rbtv_printer
import utils
import rbtv.rest as rest

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
        self.fontAwesome = rbtv_config.fontAwesome
        self.fontAwesomeBrands = rbtv_config.fontAwesomeBrands

        self.width = rbtv_config.screen_width
        self.height = rbtv_config.screen_height
        
        self.live = rbtv_config.live
        self.neu = rbtv_config.neu

    def get_screen(self) -> Image:
        today = datetime.today()
        data = rest.getRBData(today)

        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)

        #clock
        draw.rectangle((0, 25, 500, 87), fill=0)
        draw.text((0, 12), utils.getTime(today), font = self.fontBig, fill = 255)
        draw.text((190, 28), utils.getWeekday(today), font = self.fontSmal, fill = 255)
        draw.text((190, 55), utils.getDate(today), font = self.fontSmal, fill = 255)

        #notifications
        #draw.text((2, 2), '    ', font = self.fontAwesome, fill = 0)

        #views
        rbtv_printer.printViews((230, 95), draw, rest.getRBViews())


        print(utils.parseTime(data['data'][0]['date']))

        shows = []

        for i in range(len(data['data'])):
            for s in data['data'][i]['elements']:
                shows.append(s)

        print(len(shows))

        pos = 0
        hasCurrent = False
        for i in range(len(shows)):
            timeStart = utils.parseTime(shows[i]['timeStart']) + timedelta(hours=2)
            timeEnd = utils.parseTime(shows[i]['timeEnd']) + timedelta(hours=2)

            if timeEnd < today:
                continue

            if timeStart < today and timeEnd > today and not hasCurrent:
                print(shows[i]['title'], i)
                rbtv_printer.printCurrent(img, draw, shows[i], timeStart, timeEnd, today, self.fontSmal)
                hasCurrent = True # sometimes shows overlap a few minutes
                continue

            width, height = draw.textsize(utils.getTime(timeStart), font=self.fontSmal)
            title = utils.string_normalizer(str(shows[i]['title']))
            draw.text((10 + 10 + width, 35 * pos + 230), utils.getTime(timeStart) +' '+ title, font = self.fontSmal, fill = 0)

            if shows[i]['type'] == 'premiere':
                img.paste(self.neu, (10, 35 * pos + 230))
            elif shows[i]['type'] == 'live':
                img.paste(self.live, (10, 35 * pos + 230))

            pos += 1
            if pos > 5:
                break
        return img