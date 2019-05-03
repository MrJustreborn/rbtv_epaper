
import rbtv.rbtv_config as rbtv_config
import rbtv.rbtv_printer as rbtv_printer
import utils
import rbtv.rest as rest

import time
from datetime import datetime
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
import json
from io import BytesIO

class RBTV:
    def __init__(self):
        self.api = rest.API()
    
    def get_layout(self, which = "upcoming", data = None, idx = 0, size = 0):
        img = Image.new('1', (rbtv_config.screen_width, rbtv_config.screen_height), 255)
        
        if which == "boot":
            return self.get_boot_screen(img)
        elif which == "upcoming":
            return self.get_current_screen(img, True)
        elif which == "upcoming-detail":
            return self.get_current_screen(img, True, True)
        elif which == "blog":
            return self.get_blog_screen(img)
        elif which == "notification":
            return self.get_notification_screen(img, data, idx, size)
        elif which == "shutdown":
            return img
        
        return img
    
    def _draw_header(self, img: Image, today: datetime):
        draw = ImageDraw.Draw(img)
        #clock
        rbtv_printer.printClock((0,0), img, today)
        #views
        rbtv_printer.printViews((345, 70), img, self.api.getStreamCount())
        #views
        rbtv_printer.printSelf((5, 75), img, self.api.getSelf(), self.api.getNotifications())
        #placeholder for preview image
        img.paste(rbtv_config.preview_placeholder, (600-250, 0))
        return img

    def get_boot_screen(self, img: Image):
        self.api.reloadNotifications()
        draw = ImageDraw.Draw(img)
        img.paste(rbtv_config.boot, (0, 0))

        w, h = draw.textsize(rbtv_config.version, font = rbtv_config.fontVeryTiny)
        draw.text((600 - w - 5, 448 - h - 2), rbtv_config.version, font = rbtv_config.fontVeryTiny, fill = 255)

        title = "Rocketbeans TV"
        w, h = draw.textsize(title, font = rbtv_config.fontBig)
        draw.text((300 - int(w / 2), 12), title, font = rbtv_config.fontBig, fill = 255)
        title = "ePaper Sendeplan"
        w, h2 = draw.textsize(title, font = rbtv_config.fontSmall)
        draw.text((300 - int(w / 2), 12 + h), title, font = rbtv_config.fontSmall, fill = 255)

        title = "@MrJustreborn"
        w, h = draw.textsize(title, font = rbtv_config.fontVeryTiny)
        draw.text((5, 448 - h - 2), title, font = rbtv_config.fontVeryTiny, fill = 255)
        return img

    def get_notifications(self):
        return self.api.getNotifications()

    def get_notification_screen(self, img: Image, data, idx: int, size: int):
        #rbtv_printer.printNotification((5, 240), img, datetime.today().astimezone(), data, idx, size) #requires pyhton 3.6
        rbtv_printer.printNotification((5, 240), img, datetime.today(), data, idx, size)
        return self.get_current_screen(img)

    def get_blog_screen(self, img: Image):
        #rbtv_printer.printBlog((5, 250), img, datetime.today().astimezone(), self.api.getBlogPromo()) #requires pyhton 3.6
        rbtv_printer.printBlog((5, 250), img, datetime.today(), self.api.getBlogPromo())
        return self.get_current_screen(img)

    def get_current_screen(self, img: Image, upcoming = False, detail = False) -> Image:
        #today = datetime.today().astimezone() #requires pyhton 3.6
        today = datetime.today()
        data = self.api.getSchedule(today)

        draw = ImageDraw.Draw(img)

        self._draw_header(img, today)

        #print(utils.parseTime(data['data'][0]['date']))

        shows = []

        for i in range(len(data['data'])):
            for s in data['data'][i]['elements']:
                shows.append(s)

        print(len(shows))

        pos = 0
        hasCurrent = False
        cnt = 3 if detail else 6
        for i in range(len(shows)):
            timeStart = utils.parseTime(shows[i]['timeStart'])
            timeEnd = utils.parseTime(shows[i]['timeEnd'])

            if timeEnd < today:
                continue

            if timeStart < today and timeEnd > today and not hasCurrent:
                print(shows[i]['title'], i)
                rbtv_printer.printCurrent(img, shows[i], timeStart, timeEnd, today, rbtv_config.fontSmall)
                hasCurrent = True # sometimes shows overlap a few minutes
                continue
            
            if not upcoming:
                break
            rbtv_printer.printUpcomming(img, shows[i], timeStart, pos, detail)

            pos += 1
            if pos > cnt:
                break
        return img
