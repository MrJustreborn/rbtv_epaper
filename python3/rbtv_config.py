
from PIL import Image,ImageDraw,ImageFont
import os

font = os.path.join(os.path.dirname(__file__), '..', 'font')
img = os.path.join(os.path.dirname(__file__), '..', 'img')

fontSmal = ImageFont.truetype(font + '/wqy-microhei.ttc', 24)
fontBig = ImageFont.truetype(font + '/wqy-microhei.ttc', 95)

fontAwesome = ImageFont.truetype(font + '/Font Awesome 5 Free-Solid-900.otf', 25)

live = Image.open(img + '/live.bmp')
neu = Image.open(img + '/neu.bmp')

screen_width = 600
screen_height = 448