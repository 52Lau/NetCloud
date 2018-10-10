#-*- coding:utf-8 -*-
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#设置所使用的字体
font = ImageFont.truetype("src/NetCloud/source/simsun.ttc", 18)

#打开图片
imageFile = "D:\PyCharm\\NetCloud\src\\NetCloud\\songs\\张国荣\敢爱\\18919296579372684.jpg"
im1 = Image.open(imageFile)

#画图
draw = ImageDraw.Draw(im1)
draw.text((0, 0), "世界上还有比张国荣+林夕，陈奕迅+黄伟文更经典的么？", (255, 0, 0), font=font)    #设置文字位置/内容/颜色/字体
draw = ImageDraw.Draw(im1)                          #Just draw it!

#另存图片
im1.save("target.jpg")