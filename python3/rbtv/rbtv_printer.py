
import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
from io import BytesIO

import rbtv.rbtv_config as rbtv_config
import utils

def printClock(img: Image, today: datetime):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 25, rbtv_config.screen_width, 87), fill=0)
    draw.text((0, 12), utils.getTime(today), font = rbtv_config.fontBig, fill = 255)
    draw.text((190, 28), utils.getWeekday(today), font = rbtv_config.fontSmall, fill = 255)
    draw.text((190, 55), utils.getDate(today), font = rbtv_config.fontSmall, fill = 255)

def printViews(xy, img: Image, views = {'data':{'total':0,'twitch':0,'youtube':0}}, alignment = "hdigit"):
    x = xy[0]
    y = xy[1]

    draw = ImageDraw.Draw(img)
    if alignment == "hicons":
        w, h = draw.textsize("", font = rbtv_config.fontAwesomeBrands)

        draw.text((x + 7, y), "", font = rbtv_config.fontAwesomeBrands) #twitch
        draw.text((x, y + h), "", font = rbtv_config.fontAwesomeBrands) #youtube
        draw.text((x, y + h * 2), "", font = rbtv_config.fontAwesome) #total

        v = str(views['data']['twitch'])+'\n'+str(views['data']['youtube'])+'\n'+str(views['data']['total'])
        draw.multiline_text((x + w + 20, y - 4), v, font = rbtv_config.fontSmall, align = "right", spacing = 0)
    elif alignment == "hdigit":
        v = str(views['data']['twitch'])+'\n'+str(views['data']['youtube'])+'\n'+str(views['data']['total'])
        draw.multiline_text((x, y - 4), v, font = rbtv_config.fontSmall, align = "right", spacing = 1.5)

        w, h = draw.textsize("", font = rbtv_config.fontAwesomeBrands)
        w2, h2 = draw.textsize(v, font = rbtv_config.fontSmall)

        draw.text((x + w2 + 7, y), "", font = rbtv_config.fontAwesomeBrands) #twitch
        draw.text((x + w2 + 4, y + h), "", font = rbtv_config.fontAwesomeBrands) #youtube
        draw.text((x + w2 + 4, y + h * 2), "", font = rbtv_config.fontAwesome) #total
    elif alignment == "vicons":
        w, h = draw.textsize("", font = rbtv_config.fontAwesomeBrands)
        w2, h2 = draw.textsize(str(views['data']['twitch']), font = rbtv_config.fontSmall)
        draw.text((x, y), "", font = rbtv_config.fontAwesomeBrands) #twitch
        draw.text((x + w, y - 4), str(views['data']['twitch']), font = rbtv_config.fontSmall) #twitch
        tmpW = w + w2 + 5
        w, h = draw.textsize("", font = rbtv_config.fontAwesomeBrands)
        w2, h2 = draw.textsize(str(views['data']['youtube']), font = rbtv_config.fontSmall)
        draw.text((x + tmpW, y - 2), "", font = rbtv_config.fontAwesomeBrands) #youtube
        draw.text((x + tmpW + w, y - 4), str(views['data']['youtube']), font = rbtv_config.fontSmall) #youtube
        tmpW = tmpW + w + w2 + 5
        w, h = draw.textsize("", font = rbtv_config.fontAwesome)
        w2, h2 = draw.textsize(str(views['data']['total']), font = rbtv_config.fontSmall)
        draw.text((x + tmpW, y - 2), "", font = rbtv_config.fontAwesome) #total
        draw.text((x + tmpW + w, y - 4), str(views['data']['total']), font = rbtv_config.fontSmall) #total

def printCurrent(image: Image, show, timeStart: datetime, timeEnd: datetime, today: datetime, font24):
    draw = ImageDraw.Draw(image)
    
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

    draw.text((10 + 10 + width, ypos - lowborder - 53), title, font = font24, fill = 0)

    r = requests.get(show['episodeImage'])
    
    img = Image.open(BytesIO(r.content))

    maxsize = (250, 140)
    tn_image = img.thumbnail(maxsize)

    print(img.size, img.size[0])
    image.paste(img, (600-img.size[0], 25))
    pass