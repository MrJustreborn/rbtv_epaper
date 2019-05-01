#!/usr/bin/python3
# -*- coding:utf-8 -*-

#import epd5in83
import traceback
import rbtv.rbtv as rbtv
import time

def main():
    try:
        #epd = epd5in83.EPD()
        #epd.init()

        rbtv_api = rbtv.RBTV()
        img = rbtv_api.get_layout("boot")
        time.sleep(1)
        notifications = rbtv_api.get_notifications()
        size = len(notifications)
        i = 0
        for n in notifications:
            i += 1
            img = rbtv_api.get_layout("notification", n, i, size)
            break

        img.show()
        time.sleep(2)

        #img = ImageOps.flip(ImageOps.mirror(img))
        #epd.display(epd.getbuffer(img))
        #time.sleep(2)
            
        #epd.sleep()
    
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

def cycle():
    try:
        #epd = epd5in83.EPD()
        #epd.init()

        rbtv_api = rbtv.RBTV()

        img = rbtv_api.get_layout("boot")
        time.sleep(20)
        for c in range(3):
            img = rbtv_api.get_layout("upcoming")
            time.sleep(20)

            img = rbtv_api.get_layout("upcoming-detail")
            time.sleep(20)

            img = rbtv_api.get_layout("blog")
            time.sleep(20)

            notifications = rbtv_api.get_notifications()
            for n in notifications:
                img = rbtv_api.get_layout("notification", n)
                time.sleep(20)

        #img = ImageOps.flip(ImageOps.mirror(img))
        #epd.display(epd.getbuffer(img))
            
        #epd.sleep()
    
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()

if __name__ == "__main__":
    main()