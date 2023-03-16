import gnupg

# 创建 GPG 实例，参数指定了 GPG 配置文件的存储路径
gpg = gnupg.GPG(gnupghome='./my_gpg')
# 设置密钥参数
key_params = {
    'name_real': 'Mike Computer',  # 真实姓名
    'name_email': 'MikeComputer@gmail.com',  # 电子邮件地址
    'expire_date': '0',  # 密钥过期时间，0 表示永不过期
    'key_type': 'RSA',  # 密钥类型
    'key_length': 4096,  # 密钥长度
    'subkey_type': 'RSA',  # 子密钥类型
    'subkey_length': 4096,  # 子密钥长度
    'passphrase': 'my_password',  # 密钥的保护密码
}

# 生成密钥对
key_input = gpg.gen_key_input(**key_params)
key = gpg.gen_key(key_input)

# 获取公钥
public_key = gpg.export_keys(key.fingerprint)

# 获取加密的私钥
encrypted_private_key = gpg.export_keys(key.fingerprint, True)

# 获取解密的私钥
decrypted_private_key = gpg.export_keys(key.fingerprint, True, passphrase=key_params['passphrase'])

# 打印公钥
print("公钥:\n", public_key)

# 打印私钥
print("加密的私钥:\n", encrypted_private_key)
print("解密的私钥:\n", decrypted_private_key)
