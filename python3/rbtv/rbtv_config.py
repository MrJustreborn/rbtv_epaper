
from PIL import Image,ImageDraw,ImageFont
import os

font = os.path.join(os.path.dirname(__file__), '..', '..', 'font')
img = os.path.join(os.path.dirname(__file__), '..', '..', 'img')

fontVeryTiny = ImageFont.truetype(font + '/wqy-microhei.ttc', 12)
fontTiny = ImageFont.truetype(font + '/wqy-microhei.ttc', 18)
fontSmall = ImageFont.truetype(font + '/wqy-microhei.ttc', 24)
fontBig = ImageFont.truetype(font + '/wqy-microhei.ttc', 35)
fontHuge = ImageFont.truetype(font + '/wqy-microhei.ttc', 75)

fontAwesome = ImageFont.truetype(font + '/Font Awesome 5 Free-Solid-900.otf', 25)
fontAwesomeSmall = ImageFont.truetype(font + '/Font Awesome 5 Free-Solid-900.otf', 18)
fontAwesomeBrands = ImageFont.truetype(font + '/Font Awesome 5 Brands-Regular-400.otf', 25)

boot = Image.open(img + '/boot.png')
live = Image.open(img + '/live.bmp')
neu = Image.open(img + '/neu.bmp')
abonniert = Image.open(img + '/abonniert.bmp')
streamExclusive = Image.open(img + '/ohne_vod.bmp')

preview_placeholder = Image.open(img + '/placeholder.bmp')

screen_width = 600
screen_height = 448
version = 'v0.1.0'