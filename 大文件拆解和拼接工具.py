import os
import hashlib


def split_file(filename, num_chunks):
    # 创建一个存储分割后文件块的目录
    if not os.path.exists("file_chunks"):
        os.makedirs("file_chunks")

    # 打开原始文件以进行读取
    with open(filename, 'rb') as original_file:
        data = original_file.read()

        # 计算每个文件块的大小
        chunk_size = len(data) // num_chunks

        for i in range(num_chunks):
            # 计算每个文件块的起始和结束位置
            start = i * chunk_size
            end = start + chunk_size

            # 如果是最后一个文件块，结束位置为文件末尾
            if i == num_chunks - 1:
                end = len(data)

            # 获取文件块的数据
            chunk_data = data[start:end]

            # 计算文件块的哈希值（SHA-512）
            sha512_hash = hashlib.sha512(chunk_data).hexdigest()

            # 将文件块写入新的文件中
            chunk_filename = f"file_chunks/chunk{i}.dat"
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk_data)

            print(f"Chunk {i}: {chunk_filename} ({sha512_hash})")

            # 将文件块的名称和哈希值写入哈希表中
            with open("hash_table.txt", 'a') as hash_table:
                hash_table.write(f"{chunk_filename} {sha512_hash}\n")


def join_files(output_filename):
    # 获取存储文件块的目录中的所有文件
    chunk_files = sorted([f for f in os.listdir("file_chunks") if f.startswith("chunk")])

    # 创建一个新的输出文件
    with open(output_filename, 'wb') as output_file:
        for chunk_file in chunk_files:
            # 读取文件块数据
            with open(f"file_chunks/{chunk_file}", 'rb') as chunk:
                chunk_data = chunk.read()

            # 写入文件块数据到输出文件中
            output_file.write(chunk_data)

    print(f"Joined file: {output_filename}")


def check_integrity(filename):
    # 从哈希表文件中加载哈希值
    hash_table = {}
    with open("hash_table.txt", 'r') as hash_table_file:
        for line in hash_table_file:
            chunk_filename, sha512_hash = line.strip().split()
            hash_table[chunk_filename] = sha512_hash

    # 逐个检查文件块的哈希值是否匹配
    with open(filename, 'rb') as joined_file:
        data = joined_file.read()

        for chunk_filename in hash_table:
            # 读取文件块数据
            with open(chunk_filename, 'rb') as chunk_file:
                chunk_data = chunk_file.read()

            # 计算文件块的哈希值（SHA-512）
            sha512_hash = hashlib.sha512(chunk_data).hexdigest()

            # 检查哈希值是否匹配
            if sha512_hash != hash_table[chunk_filename]:
                return False

    return True


# 示例用法
filename = "我的大文件.7z"  # 替换为你的文件名
num_chunks = 20  # 替换为你要分割的文件块数量

split_file(filename, num_chunks)
join_files("joined_file.txt")

if check_integrity("joined_file.txt"):
    print("文件完整性验证通过！")
else:
    print("文件完整性验证失败！")
