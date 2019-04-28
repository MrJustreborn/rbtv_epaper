#!/usr/bin/python
# -*- coding:utf-8 -*-

#import epd5in83
import traceback

import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
import json
from io import BytesIO

def main():
    try:
        #epd = epd5in83.EPD()
        #epd.init()

        print("Drawing")
        # Drawing on the Horizontal image
        Himage = Image.new('1', (600, 448), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(Himage)
        font24 = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', 24)


        draw.text((10, 0), 'hello world', font = font24, fill = 0)
        draw.text((10, 20), '5.83inch e-Paper', font = font24, fill = 0)
        draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
        draw.line((20, 50, 70, 100), fill = 0)
        draw.line((70, 50, 20, 100), fill = 0)
        draw.rectangle((20, 50, 70, 100), outline = 0)
        draw.line((165, 50, 165, 100), fill = 0)
        draw.line((140, 75, 190, 75), fill = 0)
        draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
        draw.rectangle((80, 50, 130, 100), fill = 0)
        draw.chord((200, 50, 250, 100), 0, 360, fill = 0)



        #epd.display(epd.getbuffer(Himage))
        Himage.show()
        time.sleep(2)
        
            
        #epd.sleep()
            
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

def getTime(time: datetime):
    print(time)
    return ('0' if time.hour < 10 else '') + str(time.hour) +':'+ ('0' if time.minute < 10 else '') + str(time.minute)

def getRBData(today: datetime):
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

def parseTime(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

def main2():
    try:
        #epd = epd5in83.EPD()
        #epd.init()
    
        today = datetime.today()

        data = getRBData(today)

        img = Image.new('1', (600, 448), 255)
        
        draw = ImageDraw.Draw(img)
        font24 = ImageFont.truetype('/home/mrjustreborn/Dev/PI/epaper/wqy-microhei.ttc', 24)
        font55 = ImageFont.truetype('/home/mrjustreborn/Dev/PI/epaper/wqy-microhei.ttc', 95)
        draw.text((10,10), getTime(today), font = font55, fill = 0)
        #draw.text((10,100), str(today.day) +'. '+ str(today.month) +'. '+ str(today.year), font = font24, fill = 0)
        logo = Image.open('/home/mrjustreborn/Dev/PI/epaper/Cornerlogo_rbtv_151152.bmp')
        #img.paste(logo,  (0,0))

        print(parseTime(data['data'][0]['date']))
        #shows = data['data'][0]['elements']

        shows = []

        for i in range(len(data['data'])):
            for s in data['data'][i]['elements']:
                shows.append(s)

        print(len(shows))

        pos = 0
        for i in range(len(shows)):
            timeStart = parseTime(shows[i]['timeStart']) + timedelta(hours=2)
            timeEnd = parseTime(shows[i]['timeEnd']) + timedelta(hours=2)

            if timeEnd < today:
                continue

            if timeStart < today and timeEnd > today:
                print(shows[i]['title'], i)
                printCurrent(img, draw, shows[i], timeStart, timeEnd, today, font24)
                continue

            width, height = draw.textsize(getTime(timeStart), font=font24)
            draw.text((10 + 10 + width, 35 * pos + 230), getTime(timeStart) +' '+ str(shows[i]['title']), font = font24, fill = 0)
            pos += 1
            if pos > 5:
                break
    
        #img = ImageOps.flip(ImageOps.mirror(img))
        #epd.display(epd.getbuffer(img))
        #time.sleep(2)
            
        #epd.sleep()

        img.show()
    
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

def printCurrent(image, draw: ImageDraw, show, timeStart: datetime, timeEnd: datetime, today: datetime, font24):
    lowborder = 10
    ypos = 230

    width, height = draw.textsize(getTime(timeStart), font=font24)
    draw.text((10, ypos - lowborder - height), getTime(timeStart), font = font24, fill = 0)

    width, height = draw.textsize(getTime(timeEnd), font=font24)
    draw.text((600 - 10 - width, ypos - lowborder - height), getTime(timeEnd), font = font24, fill = 0)


    draw.rectangle((10 + 10 + width, ypos - lowborder - height, 600 - 10 - width - 10, ypos - lowborder))

    width2 = 600 - 10 - width - 10 - 2 - (10 + 10 + width + 2)
    sts = datetime.timestamp(timeStart)
    ets = datetime.timestamp(timeEnd)
    tts = datetime.timestamp(today)

    width2 = width2 * (tts-sts)/(ets-sts)

    draw.rectangle((10 + 10 + width + 2, ypos - lowborder - height + 2, 10 + 10 + width + 2 + width2, ypos - lowborder - 2), 0)

    width2, height = draw.textsize(show['title'], font=font24)
    draw.text((10 + 10 + width, ypos - lowborder - height - height - height + 5), show['title'] +'\n'+ (show['topic'] if show['topic'] else show['game']), font = font24, fill = 0)

    r = requests.get(show['episodeImage'])
    
    img = Image.open(BytesIO(r.content))

    maxsize = (300, 150)
    tn_image = img.thumbnail(maxsize)

    print(img.size, img.size[0])
    image.paste(img, (600-img.size[0] -10,10))
    pass

if __name__ == "__main__":
    main2()