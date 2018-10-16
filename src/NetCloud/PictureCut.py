from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#设置所使用的字体
font = ImageFont.truetype("src/NetCloud/source/simsun.ttc", 26)
font2 = ImageFont.truetype("src/NetCloud/source/simsun.ttc", 45)
# 加载底图
base_img = Image.open(u'D:\PyCharm\\NetCloud\\src\\NetCloud\songs\张国荣\\bg2.jpg')
# 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
# print base_img.size, base_img.mode
box = (110, 140, 360, 400)  # 底图上需要P掉的区域  x轴 y轴 宽（减去x） 高（减去y）

# 加载需要P上去的图片
tmp_img = Image.open(u'D:\PyCharm\\NetCloud\src\\NetCloud\songs\张国荣\曾经我也想过一了百了\\109951163250233892.jpg')
# 这里可以选择一块区域或者整张图片
# region = tmp_img.crop((0,0,304,546)) #选择一块区域
# 或者使用整张图片
region = tmp_img

# 使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
# 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
# 提前将图片进行缩放，以适应box区域大小
# region = region.rotate(180) #对图片进行旋转
region = region.resize((box[2] - box[0], box[3] - box[1]))
base_img.paste(region, box)

#画图
draw = ImageDraw.Draw(base_img)
#评论者信息
draw.text((120, 420), "@lau52y\n\n2016-05-05 20:28:54\n\n在《xxxx》下的评论", (255, 0, 0), font=font)    #设置文字位置/内容/颜色/字体
#评论内容
text='目前唯一支撑我活下去的就是我的父母了，想要让父母过得更好，不想结婚也不想交男朋友，深夜时总会一个人躺在床上胡思乱想，父母已经不年轻了，总有一天会先于我离开，真的到了那一天……我不知道我会不会跟着一起走，只希望，他们可以长命百岁，虽然不太可能，但是我自私的希望他们可以过得比我更久'
textPur = ''
while text:
    textPur=textPur+text[:20]+"\n"
    #print(text[:20])
    text=text[20:]
draw.text((420, 200), textPur, (255, 0, 0), font=font2)    #设置文字位置/内容/颜色/字体
draw = ImageDraw.Draw(base_img)

base_img.show() # 查看合成的图片
base_img.save('./out.png')  # 保存图片
#base_img.save('D:\PyCharm\\NetCloud\src\\NetCloud\songs\张国荣\曾经我也想过一了百了\\109951163451310964.jpg')  # 保存图片



# text='sadadadasda'
# while text:
#     print(text[:20])
#     text=text[20:]