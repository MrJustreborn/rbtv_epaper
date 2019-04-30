
import time
from datetime import datetime,timedelta
import calendar

from PIL import Image,ImageDraw,ImageFont

import requests
from io import BytesIO

import rbtv.rbtv_config as rbtv_config
import utils

def printClock(xy, img: Image, today: datetime):
    x = xy[0]
    y = xy[1]


    draw = ImageDraw.Draw(img)
    draw.rectangle((x, y, rbtv_config.screen_width, 65), fill=0)
    draw.text((x, y - 12), utils.getTime(today), font = rbtv_config.fontBig, fill = 255)
    draw.text((x + 200, y + 3), utils.getWeekday(today), font = rbtv_config.fontSmall, fill = 255)
    draw.text((x + 200, y + 32), utils.getDate(today), font = rbtv_config.fontSmall, fill = 255)

def printViews(xy, img: Image, views = {'data':{'total':0,'twitch':0,'youtube':0}}, alignment = "hdigit", anchor = "right"):
    x = xy[0]
    y = xy[1]

    draw = ImageDraw.Draw(img)
    if anchor == "right":
        w, h = draw.textsize(str(views['data']['total']), font = rbtv_config.fontSmall)
        print("width ", w)
        x = x - (w + 30) # ~ size of icon
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

def printSelf(xy, img: Image, self = {"success":True,"data":{"displayName":"MrJustreborn"}}, notifications = []):
    x = xy[0]
    y = xy[1]
    
    draw = ImageDraw.Draw(img)

    if self:
        draw.text((x, y), "", font = rbtv_config.fontAwesome)
        draw.text((x + 30, y), str(self['data']['displayName']), font = rbtv_config.fontSmall)

    if len(notifications) > 0:
        unread = 0
        for n in notifications:
            if n['status'] == 'unread':
                unread += 1

        y += 30
        draw.text((x, y), "", font = rbtv_config.fontAwesome)
        draw.text((x + 30, y - 2), str(len(notifications)) + (' (' + str(unread) + ')' if unread > 0 else ''), font = rbtv_config.fontSmall)

    # y += 27
    # draw.text((x, y), "", font = rbtv_config.fontAwesome)
    # draw.text((x + 30, y - 4), 'Updates', font = rbtv_config.fontSmall)









def printUpcomming(img: Image, show, timeStart: datetime, pos, detail = False):
    draw = ImageDraw.Draw(img)

    if detail:
        pos *= 2

    width, height = draw.textsize(utils.getTime(timeStart), font = rbtv_config.fontSmall)
    
    title = str(show['title'])
    if not detail:
        title = title +' - '+ (show['topic'] if show['topic'] else show['game'])
    title = utils.string_normalizer(title)
    title = truncateString(draw, title)

    height = 220 if detail else 210
    if detail:
        height += pos * 5
    paddingLeft = 70
    draw.text((10 + paddingLeft, 33 * pos + height), utils.getTime(timeStart) +' '+ title, font = rbtv_config.fontSmall, fill = 0)
    
    if detail:
        detailStr = str((show['topic'] if show['topic'] else show['game']))
        detailStr = utils.string_normalizer(detailStr)
        detailStr = truncateString(draw, detailStr)
        draw.text((10 + paddingLeft + width, 33 * pos + height + 32), ' ' +detailStr, font = rbtv_config.fontSmall, fill = 0)

    if show['type'] == 'premiere':
        img.paste(rbtv_config.neu, (10, 33 * pos + height))
    elif show['type'] == 'live':
        img.paste(rbtv_config.live, (10, 33 * pos + height))
    
    if detail and show.get('isSubscribed', False):
        img.paste(rbtv_config.abonniert, (10, 33 * pos + height + 32))


def printCurrent(image: Image, show, timeStart: datetime, timeEnd: datetime, today: datetime, font = rbtv_config.fontSmall):
    draw = ImageDraw.Draw(image)
    
    lowborder = 10
    ypos = 210

    draw.rectangle((0, ypos - 70, 600, ypos - 70))

    width, height = draw.textsize(utils.getTime(timeStart), font = font)
    draw.text((10, ypos - lowborder - height), utils.getTime(timeStart), font = font, fill = 0)

    width, height = draw.textsize(utils.getTime(timeEnd), font = font)
    draw.text((600 - 10 - width, ypos - lowborder - height), utils.getTime(timeEnd), font = font, fill = 0)


    draw.rectangle((10 + 10 + width, ypos - lowborder - height + 2, 600 - 10 - width - 10, ypos - lowborder + 2))

    width2 = 600 - 10 - width - 10 - 2 - (10 + 10 + width + 2)
    sts = datetime.timestamp(timeStart)
    ets = datetime.timestamp(timeEnd)
    tts = datetime.timestamp(today)

    width2 = width2 * (tts-sts)/(ets-sts)

    draw.rectangle((10 + 10 + width + 2, ypos - lowborder - height + 4, 10 + 10 + width + 2 + width2, ypos - lowborder - 0), 0)


    title = str(show['title'])
    title = title +' - '+ (show['topic'] if show['topic'] else show['game'])
    title = utils.string_normalizer(title)
    title = truncateString(draw, title, 500)

    draw.text((10 + 10 + width, ypos - lowborder - 53), title, font = font, fill = 0)

    if show['type'] == 'premiere':
        image.paste(rbtv_config.neu, (10, ypos - lowborder - 53))
    elif show['type'] == 'live':
        image.paste(rbtv_config.live, (10, ypos - lowborder - 53))

    r = requests.get(show['episodeImage'])
    try:
        img = Image.open(BytesIO(r.content))

        maxsize = (250, 140)
        tn_image = img.thumbnail(maxsize)

    #print(img.size, img.size[0])
        image.paste(img, (350, 0))
    except:
        print('could not load episodeImage')
        pass
    pass

def truncateString(draw: ImageDraw, text: str, maxWidth = 420, font = rbtv_config.fontSmall):
    w, h = draw.textsize(text, font = font)

    wasModified = False
    while w > maxWidth:
        text = text[:-1]
        w, h = draw.textsize(text, font = font)
        wasModified = True
    
    if wasModified:
        text = text + " ..."
    
    return text