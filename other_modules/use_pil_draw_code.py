# -*- coding:utf-8 -*-


from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


def rand_char():
    """创建随机字母"""
    return chr(random.randint(65, 90))


def rand_color():
    """创建随机颜色"""
    return (random.randint(64, 255),
            random.randint(64, 255), random.randint(64, 255))


def rand_color2():
    """创建随机颜色"""
    return (random.randint(32, 127),
            random.randint(32, 127), random.randint(32, 127),)


# 图片尺寸
width = 60 * 4
height = 60

# 创建新的图片Image.new((mode, size, color=0)
image = Image.new('RGB', (width, height), (255, 255, 255))

# 加载字体
font = ImageFont.truetype('arial.ttf', 36)

# 创建绘图对象
draw = ImageDraw.Draw(image)

# 填充每个像素
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rand_color())

# 指定位置绘制字符， draw.text(position,string, options)
for t in range(4):
    char1 = rand_char()
    draw.text((60 * t + 10, 10), char1, font=font, fill=rand_color2())

image.save('code_source.jpg', 'jpeg')

# 模糊
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
