#!/usr/bin/python3
# -*- coding:utf-8 -*-

#import epd5in83
import traceback
import rbtv.rbtv as rbtv

def main():
    try:
        #epd = epd5in83.EPD()
        #epd.init()

        rbtv_api = rbtv.RBTV()
        img = rbtv_api.get_screen()

        img.show()

        #img = ImageOps.flip(ImageOps.mirror(img))
        #epd.display(epd.getbuffer(img))
        #time.sleep(2)
            
        #epd.sleep()
    
    except:
        print('traceback.format_exc():\n%s',traceback.format_exc())
        exit()


if __name__ == "__main__":
    main()