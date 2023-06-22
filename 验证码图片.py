import random
import string
from PIL import Image, ImageDraw, ImageFont


def generate_captcha(noise=0.06):
    # 定义图像大小和字体
    width, height = 120, 50
    font_size = 40
    font = ImageFont.truetype("arial.ttf", font_size)
    chars = string.ascii_letters + string.digits

    # 创建图像对象
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    captcha = ''
    for i in range(5):
        char = random.choice(chars)
        captcha += char

        # 绘制随机字符
        x = i * width / 5 + random.randint(-10, 10)
        y = random.randint(-10, 10)
        draw.text((x, y), char, fill=(0, 0, 0), font=font)

    # 添加噪声
    for i in range(width):
        for j in range(height):
            if random.random() < noise:
                draw.point((i, j), fill=(0, 0, 0))

    return captcha, image


def save_captcha_image(file_path, noise=0.06):
    captcha, image = generate_captcha(noise)
    image.save(file_path)
    print("验证码已生成并保存为：", file_path)
    image.show()


save_captcha_image('captcha.png')
