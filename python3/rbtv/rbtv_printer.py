
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


testNotification = [
    {"type":3,"id":7186464,"date":"2019-04-28T23:04:03.000Z","status":"read","data":{"mgmtid":33,"name":"Simon","title":"The Messenger (8-Bit) Speedrun in 41:52 von Sia | Speedrundale","show":"Speedrundale","id":10084,"thumbnail":[{"height":0,"width":0,"name":"ytsmall","url":"https://img.youtube.com/vi/ISwPB8nL4ik/mqdefault.jpg"},{"height":0,"width":0,"name":"ytbig","url":"https://img.youtube.com/vi/ISwPB8nL4ik/maxresdefault.jpg"}]}},
    {"type":3,"id":7197123,"date":"2019-04-29T18:33:33.000Z","status":"unread","data":{"mgmtid":73,"name":"Donnie","title":"Falscher Cheat Code | Endgegner: Age of Empires | Marco vs. Donnie & Marah","show":"Endgegner","id":10531,"thumbnail":[{"height":0,"width":0,"name":"ytsmall","url":"https://img.youtube.com/vi/wbqMYkHxVys/mqdefault.jpg"},{"height":0,"width":0,"name":"ytbig","url":"https://img.youtube.com/vi/wbqMYkHxVys/maxresdefault.jpg"}]}},
    {"type":3,"id":7210871,"date":"2019-04-30T12:00:29.000Z","status":"unread","data":{"mgmtid":33,"name":"Simon","title":"Gegeißelt vom Geisterwesen | Sekiro Shadows Die Twice mit Simon & Nils #15","show":"Knallhart Durchgenommen","id":10557,"thumbnail":[{"height":0,"width":0,"name":"ytsmall","url":"https://img.youtube.com/vi/Hau_UwwDYG0/mqdefault.jpg"},{"height":0,"width":0,"name":"ytbig","url":"https://img.youtube.com/vi/Hau_UwwDYG0/maxresdefault.jpg"}]}},
    {"type":3,"id":7214132,"date":"2019-04-30T13:03:50.000Z","status":"unread","data":{"mgmtid":33,"name":"Simon","title":"Kindheits(alp)traum: Auge in Auge mit dem Alien dank VR | Alien Isolation mit Simon #02","show":"After Dark","id":10558,"thumbnail":[{"height":0,"width":0,"name":"ytsmall","url":"https://img.youtube.com/vi/83CzRQOPUSg/mqdefault.jpg"},{"height":0,"width":0,"name":"ytbig","url":"https://img.youtube.com/vi/83CzRQOPUSg/maxresdefault.jpg"}]}}
]

def printSelf(xy, img: Image, self = {"success":True,"data":{"displayName":"MrJustreborn"}}, notifications = testNotification):
    x = xy[0]
    y = xy[1]
    
    draw = ImageDraw.Draw(img)
    draw.text((x, y), "", font = rbtv_config.fontAwesome)
    draw.text((x + 30, y - 4), str(self['data']['displayName']), font = rbtv_config.fontSmall)

    unread = 0
    for n in notifications:
        if n['status'] == 'unread':
            unread += 1

    y += 30
    draw.text((x, y), "", font = rbtv_config.fontAwesome)
    draw.text((x + 30, y - 4), str(len(notifications)) + (' (' + str(unread) + ')' if unread > 0 else ''), font = rbtv_config.fontSmall)

    # y += 27
    # draw.text((x, y), "", font = rbtv_config.fontAwesome)
    # draw.text((x + 30, y - 4), 'Updates', font = rbtv_config.fontSmall)









def printUpcomming(img: Image, show, timeStart: datetime, pos):
    draw = ImageDraw.Draw(img)

    width, height = draw.textsize(utils.getTime(timeStart), font = rbtv_config.fontSmall)
    title = utils.string_normalizer(str(show['title']))
    draw.text((10 + 10 + width, 35 * pos + 230), utils.getTime(timeStart) +' '+ title, font = rbtv_config.fontSmall, fill = 0)

    if show['type'] == 'premiere':
        img.paste(rbtv_config.neu, (10, 35 * pos + 230))
    elif show['type'] == 'live':
        img.paste(rbtv_config.live, (10, 35 * pos + 230))


def printCurrent(image: Image, show, timeStart: datetime, timeEnd: datetime, today: datetime, font24):
    draw = ImageDraw.Draw(image)
    
    lowborder = 10
    ypos = 210

    draw.rectangle((0, ypos - 70, 600, ypos - 70))

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

    #r = requests.get(show['episodeImage'])
    
    #img = Image.open(BytesIO(r.content))

    #maxsize = (250, 140)
    #tn_image = img.thumbnail(maxsize)

    #print(img.size, img.size[0])
    #image.paste(img, (600-img.size[0], 25))
    pass