from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

# 生成一个随机密钥
key = get_random_bytes(32)  # ChaCha20密钥长度为32字节

# 加密
data = b'你好，世界！'
cipher = ChaCha20.new(key=key)
nonce = cipher.nonce  # 获取随机生成的nonce
ciphertext = cipher.encrypt(data)

# 将nonce和密文合并在一起
combined = nonce + ciphertext

print(f"合并后的数据 (nonce + 密文): {combined.hex()}")

# 解密
# 从combined中分离出nonce和密文
nonce_from_combined = combined[:8]  # ChaCha20 nonce长度为8字节
ciphertext_from_combined = combined[8:]

cipher = ChaCha20.new(key=key, nonce=nonce_from_combined)
plaintext = cipher.decrypt(ciphertext_from_combined)

print(f"解密后的明文: {plaintext.decode('utf-8')}")
