
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
        self.fontSmall = rbtv_config.fontSmall
        self.fontBig = rbtv_config.fontBig
        self.fontAwesome = rbtv_config.fontAwesome
        self.fontAwesomeBrands = rbtv_config.fontAwesomeBrands

        self.width = rbtv_config.screen_width
        self.height = rbtv_config.screen_height
        
        self.live = rbtv_config.live
        self.neu = rbtv_config.neu
    
    def _draw_header(self, img: Image, today: datetime):
        draw = ImageDraw.Draw(img)
        #clock
        rbtv_printer.printClock(img, today)

        #notifications
        #draw.text((2, 2), '    ', font = rbtv_config.fontAwesomeSmall, fill = 0)
        draw.text((2, 2), '', font = rbtv_config.fontAwesomeSmall, fill = 0)
        draw.text((22, 2), '2', font = rbtv_config.fontTiny, fill = 0)

        #version
        w, h = draw.textsize('v0.1.0', font = rbtv_config.fontTiny)
        draw.text((rbtv_config.screen_width - w - 4, 2), 'v0.1.0', font = rbtv_config.fontTiny, fill = 0)

    def get_screen_blog(self) -> Image:
        today = datetime.today()

        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)

        self._draw_header(img, today)

        draw.text((375, 12), "Blog", font = rbtv_config.fontBig, fill = 255)

        blog = rest.getBlogPromo()

        for i in range(2):
            date = utils.parseTime(blog['data'][i]['publishDate'])
            print(date)
            draw.text((5, 95 + 175 * i), str(utils.getTime(date)) +' - '+ str(utils.getDate(date)), font = rbtv_config.fontSmall, fill = 0)
            draw.text((5 + 210, 95 + 175 * i + 30), str(blog['data'][i]['title']).replace(': ', ':\n'), font = rbtv_config.fontSmall, fill = 0)
            
            draw.text((5 + 210, 95 + 175 * i + (90 if i == 0 else 60)), str(blog['data'][i]['subtitle']).replace('. ', '.\n').replace(', ', ',\n'), font = rbtv_config.fontTiny, fill = 0)

            r = requests.get('https:' + str(blog['data'][i]['thumbImage'][0]['url']))
            preview = Image.open(BytesIO(r.content))
            maxsize = (300, 140)
            tn_image = preview.thumbnail(maxsize)
            img.paste(preview, (5, 95 + 175 * i + 30))

        return img

    def get_screen(self) -> Image:
        today = datetime.today()
        data = rest.getSchedule(today)

        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)

        self._draw_header(img, today)

        #views
        rbtv_printer.printViews((260, 95), img, rest.getStreamCount())


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
                rbtv_printer.printCurrent(img, shows[i], timeStart, timeEnd, today, self.fontSmall)
                hasCurrent = True # sometimes shows overlap a few minutes
                continue

            width, height = draw.textsize(utils.getTime(timeStart), font=self.fontSmall)
            title = utils.string_normalizer(str(shows[i]['title']))
            draw.text((10 + 10 + width, 35 * pos + 230), utils.getTime(timeStart) +' '+ title, font = self.fontSmall, fill = 0)

            if shows[i]['type'] == 'premiere':
                img.paste(self.neu, (10, 35 * pos + 230))
            elif shows[i]['type'] == 'live':
                img.paste(self.live, (10, 35 * pos + 230))

            pos += 1
            if pos > 5:
                break
        return img