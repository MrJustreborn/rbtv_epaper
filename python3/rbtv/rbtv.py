
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
        self.api = rest.API()
    
    def _draw_header(self, img: Image, today: datetime):
        draw = ImageDraw.Draw(img)

        #clock
        rbtv_printer.printClock((0,0), img, today)

        #views
        rbtv_printer.printViews((345, 70), img, self.api.getStreamCount())

        #views
        rbtv_printer.printSelf((5, 75), img)

        #placeholder for preview image
        img.paste(rbtv_config.preview_placeholder, (600-250, 0))

        #notifications
        #draw.text((2, 2), '    ', font = rbtv_config.fontAwesomeSmall, fill = 0)
        #draw.text((2, 2), '', font = rbtv_config.fontAwesomeSmall, fill = 0)
        #draw.text((22, 2), '2', font = rbtv_config.fontTiny, fill = 0)

        #version
        #vString = "Beans on (e)Paper v0.1.0"
        #w, h = draw.textsize(vString, font = rbtv_config.fontTiny)
        #draw.text((rbtv_config.screen_width - w - 4, 2), vString, font = rbtv_config.fontTiny, fill = 0)

    # def get_screen_blog(self) -> Image:
    #     today = datetime.today()

    #     img = Image.new('1', (rbtv_config.screen_width, rbtv_config.screen_height), 255)
    #     draw = ImageDraw.Draw(img)

    #     self._draw_header(img, today)

    #     draw.text((375, 12), "Blog", font = rbtv_config.fontBig, fill = 255)

    #     blog = self.api.getBlogPromo()

    #     for i in range(2):
    #         date = utils.parseTime(blog['data'][i]['publishDate'])
    #         print(date)
    #         draw.text((5, 95 + 175 * i), str(utils.getTime(date)) +' - '+ str(utils.getDate(date)), font = rbtv_config.fontSmall, fill = 0)
    #         draw.text((5 + 210, 95 + 175 * i + 30), str(blog['data'][i]['title']).replace(': ', ':\n'), font = rbtv_config.fontSmall, fill = 0)
            
    #         draw.text((5 + 210, 95 + 175 * i + (90 if i == 0 else 60)), str(blog['data'][i]['subtitle']).replace('. ', '.\n').replace(', ', ',\n'), font = rbtv_config.fontTiny, fill = 0)

    #         r = requests.get('https:' + str(blog['data'][i]['thumbImage'][0]['url']))
    #         preview = Image.open(BytesIO(r.content))
    #         maxsize = (300, 140)
    #         tn_image = preview.thumbnail(maxsize)
    #         img.paste(preview, (5, 95 + 175 * i + 30))

        return img

    def printBlog(self, img: Image):
        draw = ImageDraw.Draw(img)
        blog = self.api.getBlogPromo()

        date = utils.parseTime(blog['data'][0]['publishDate'])
        print(date)
        draw.text((5, 95 + 155), str(utils.getTime(date)) +' - '+ str(utils.getDate(date)), font = rbtv_config.fontSmall, fill = 0)
        draw.text((5 + 210, 95 + 155 + 30), str(blog['data'][0]['title']).replace(': ', ':\n'), font = rbtv_config.fontSmall, fill = 0)
        
        draw.text((5 + 210, 95 + 175 + 65), str(blog['data'][0]['subtitle']).replace('. ', '.\n').replace(', ', ',\n'), font = rbtv_config.fontTiny, fill = 0)

        r = requests.get('https:' + str(blog['data'][0]['thumbImage'][0]['url']))
        preview = Image.open(BytesIO(r.content))
        maxsize = (300, 140)
        tn_image = preview.thumbnail(maxsize)
        img.paste(preview, (5, 95 + 155 + 30))

    def get_screen(self) -> Image:
        today = datetime.today()
        data = self.api.getSchedule(today)

        img = Image.new('1', (rbtv_config.screen_width, rbtv_config.screen_height), 255)
        draw = ImageDraw.Draw(img)

        self._draw_header(img, today)


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
                rbtv_printer.printCurrent(img, shows[i], timeStart, timeEnd, today, rbtv_config.fontSmall)
                hasCurrent = True # sometimes shows overlap a few minutes
                continue
            
            # if today.minute % 2 == 0:
            rbtv_printer.printUpcomming(img, shows[i], timeStart, pos)

            pos += 1
            if pos > 6:
                break
        # if today.minute % 2 == 1:
        #     self.printBlog(img)
        return img
