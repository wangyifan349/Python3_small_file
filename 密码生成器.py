import random,string
# 定义密码长度和生成数量
pwd_len = 128
num_pwd = 100
# 定义符号集合
symbols = string.punctuation
# 生成随机密码
def generate_password():
    chars = string.ascii_letters + string.digits + symbols
    return ''.join(random.choice(chars) for _ in range(pwd_len))
# 将生成的密码写入文本文件
with open('passwords.txt', 'w') as f:
    for i in range(num_pwd):
        password = generate_password()
        f.write(password + '\n')
        print(password)
