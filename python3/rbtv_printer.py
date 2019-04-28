
import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
from io import BytesIO


def getTime(time: datetime):
    return ('0' if time.hour < 10 else '') + str(time.hour) +':'+ ('0' if time.minute < 10 else '') + str(time.minute)


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


    title = str(show['title'])
    title = title.replace('Let’s', "Let's")
    width2, height = draw.textsize(title, font=font24)
    draw.text((10 + 10 + width, ypos - lowborder - height - height - height + 5), title +'\n'+ (show['topic'] if show['topic'] else show['game']), font = font24, fill = 0)

    r = requests.get(show['episodeImage'])
    
    img = Image.open(BytesIO(r.content))

    maxsize = (300, 150)
    tn_image = img.thumbnail(maxsize)

    print(img.size, img.size[0])
    image.paste(img, (600-img.size[0] -10,10))
    pass