import random
import string
from PIL import Image, ImageDraw, ImageFont


def generate_captcha(noise=0.06):
    # 定义图像大小和字体
    width, height = 120, 50
    font_size = 40
    font = ImageFont.truetype("arial.ttf", font_size)#使用的字体是"Arial"，它在Windows和Mac OS X操作系统中都是默认安装的常用字体之一。
    
    # 定义随机字符集
    chars = string.ascii_letters + string.digits  # 包含所有大小写字母和数字
    
    # 创建图像对象
    image = Image.new('RGB', (width,height), color = (255,255,255))
    draw = ImageDraw.Draw(image)
    
    # 生成随机字符串
    captcha = ''
    for i in range(5):
        char = random.choice(chars)
        captcha += char
        
        # 绘制随机字符
        x = i * width/5 + random.randint(-10, 10)
        y = random.randint(-10, 10)
        draw.text((x, y), char, fill=(0,0,0), font=font)
        
    # 添加噪声
    for i in range(width):
        for j in range(height):
            if random.random() < noise:
                draw.point((i, j), fill=(0,0,0))
                
    # 返回验证码和图像
    return captcha, image
captcha, image = generate_captcha(noise=0.06)
#image.show()
image.save('captcha.png')

image.show()
