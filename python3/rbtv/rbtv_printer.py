
import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
from io import BytesIO

import rbtv.rbtv_config as rbtv_config
import utils

def printViews(xy, draw: ImageDraw, views = {'data':{'total':0,'twitch':0,'youtube':0}}):
    x = xy[0]
    y = xy[1]

    w, h = draw.textsize("", font = rbtv_config.fontAwesomeBrands)
    w2, h2 = draw.textsize("123", font = rbtv_config.fontSmal)

    draw.text((x + 7, y), "", font = rbtv_config.fontAwesomeBrands) #twitch
    draw.text((x, y + h), "", font = rbtv_config.fontAwesomeBrands) #youtube
    draw.text((x, y + h * 2), "", font = rbtv_config.fontAwesome) #total

    v = str(views['data']['twitch'])+'\n'+str(views['data']['youtube'])+'\n'+str(views['data']['total'])
    #w2, h2 = draw.textsize(v, font = rbtv_config.fontSmal)
    draw.multiline_text((x + w + 20, y - 4), v, font = rbtv_config.fontSmal, align = "right", spacing = 0)

def printCurrent(image, draw: ImageDraw, show, timeStart: datetime, timeEnd: datetime, today: datetime, font24):
    lowborder = 10
    ypos = 230

    width, height = draw.textsize(utils.getTime(timeStart), font=font24)
    draw.text((10, ypos - lowborder - height), utils.getTime(timeStart), font = font24, fill = 0)

    width, height = draw.textsize(utils.getTime(timeEnd), font=font24)
    draw.text((600 - 10 - width, ypos - lowborder - height), utils.getTime(timeEnd), font = font24, fill = 0)


    draw.rectangle((10 + 10 + width, ypos - lowborder - height + 2, 600 - 10 - width - 10, ypos - lowborder + 2))

    width2 = 600 - 10 - width - 10 - 2 - (10 + 10 + width + 2)
    sts = datetime.timestamp(timeStart)
    ets = datetime.timestamp(timeEnd)
    tts = datetime.timestamp(today)

    width2 = width2 * (tts-sts)/(ets-sts)

    draw.rectangle((10 + 10 + width + 2, ypos - lowborder - height + 4, 10 + 10 + width + 2 + width2, ypos - lowborder - 0), 0)


    title = utils.string_normalizer(str(show['title']))
    title = title +' - '+ (show['topic'] if show['topic'] else show['game'])
    width2, height = draw.textsize(title, font=font24)

    wasModified = False
    while width2 > 420:
        title = title[:-1]
        width2, height = draw.textsize(title, font=font24)
        wasModified = True
    
    if wasModified:
        title = title + " ..."

    draw.text((10 + 10 + width, ypos - lowborder - height - height - 5), title, font = font24, fill = 0)

    r = requests.get(show['episodeImage'])
    
    img = Image.open(BytesIO(r.content))

    maxsize = (300, 150)
    tn_image = img.thumbnail(maxsize)

    print(img.size, img.size[0])
    image.paste(img, (600-img.size[0] -10,10))
    pass