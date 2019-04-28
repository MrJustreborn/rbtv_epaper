
from PIL import Image,ImageDraw,ImageFont

fontSmal = ImageFont.truetype('../font/wqy-microhei.ttc', 24)
fontBig = ImageFont.truetype('../font/wqy-microhei.ttc', 95)

live = Image.open('../img/live.bmp')
neu = Image.open('../img/neu.bmp')

screen_width = 600
screen_height = 448