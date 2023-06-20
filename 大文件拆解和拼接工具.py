import os
import hashlib
import string
import random


def split_file(filename, num_chunks):
    # 获取文件所在目录并切换工作目录
    dirname = os.path.dirname(os.path.abspath(filename))
    os.chdir(dirname)

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
            blake2b_hash = hashlib.blake2b(chunk_data).hexdigest()

            # 构建文件块的新文件名
            original_filename, extension = os.path.splitext(filename)
            chunk_filename = f"{original_filename}_chunk{i}{extension}"

            # 将文件块写入新的文件中
            with open(chunk_filename, 'wb') as chunk_file:
                chunk_file.write(chunk_data)

            # 将文件块的名称和哈希值写入哈希表中
            with open("hash_table.txt", 'a') as hash_table:
                hash_table.write(f"文件块 {chunk_filename} {blake2b_hash}\n")

    # 计算源文件的哈希值
    with open(filename, 'rb') as source_file:
        data = source_file.read()
        source_hash = hashlib.blake2b(data).hexdigest()

    # 将源文件的名称和哈希值写入哈希表中
    with open("hash_table.txt", 'a') as hash_table:
        hash_table.write(f"源文件 {filename} {source_hash}\n")


def join_files(output_filename):
    # 获取合并文件的文件名和扩展名
    original_filename, extension = os.path.splitext(output_filename)

    # 从哈希表文件中加载文件块的哈希值
    hash_table = {}
    with open("hash_table.txt", 'r') as hash_table_file:
        for line in hash_table_file:
            type, file_path, file_hash = line.strip().split()
            if type == "文件块":
                hash_table[file_path] = file_hash
    chunk_files = sorted(hash_table.keys())

    # 创建一个新的输出文件
    with open(output_filename, 'wb') as output_file:
        for chunk_file in chunk_files:
            # 读取文件块数据
            with open(chunk_file, 'rb') as chunk:
                chunk_data = chunk.read()
            # 写入文件块数据到输出文件中
            output_file.write(chunk_data)

    # 计算合并后的文件的哈希值
    with open(output_filename, 'rb') as output_file:
        data = output_file.read()
        output_hash = hashlib.blake2b(data).hexdigest()

    # 将合并后的文件的名称和哈希值写入哈希表中
    with open("hash_table.txt", 'a') as hash_table:
        hash_table.write(f"重组文件 {output_filename} {output_hash}\n")


def check_integrity(filename):
    # 从哈希表文件中加载哈希值
    hash_table = {}
    with open("hash_table.txt", 'r') as hash_table_file:
        for line in hash_table_file:
            type, file_path, file_hash = line.strip().split()
            hash_table[file_path] = (type, file_hash)

    # 查找源文件和重组文件的哈希值
    source_hash = None
    joined_hash = None
    for file_path, (type, file_hash) in hash_table.items():
        if type == "源文件":
            source_hash = file_hash
        elif type == "重组文件" and file_path == filename:
            joined_hash = file_hash

    # 检查源文件和重组文件的哈希值是否相同
    if source_hash != joined_hash:
        return False

    # 逐个检查文件块的哈希值是否匹配
    for file_path, (type, file_hash) in hash_table.items():
        # 忽略源文件和重组文件
        if type != "文件块":
            continue

        # 读取文件块数据
        with open(file_path, 'rb') as chunk:
            chunk_data = chunk.read()

        # 计算文件块的哈希值（BLAKE2b）
        blake2b_hash = hashlib.blake2b(chunk_data).hexdigest()

        # 检查哈希值是否匹配
        if blake2b_hash != file_hash:
            return False

    return True


# 生成随机字符串作为后缀
def generate_random_suffix(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# 检查文件是否存在，若存在，则添加后缀
def check_existing_file(file_path):
    file_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(file_name)

    suffix = 1
    new_file_path = file_path
    while os.path.exists(new_file_path):
        new_file_name = f"{base_name}_{suffix}{extension}"
        new_file_path = os.path.join(file_dir, new_file_name)
        suffix += 1

    return new_file_path


# 示例用法
filename = r"E:\新建文件夹\1.conf"  # 替换为你的文件名
num_chunks = 5  # 替换为你要分割的文件块数量

random_suffix = generate_random_suffix()
split_filename = f"拆解_{os.path.basename(filename)}_{random_suffix}"
merge_filename = f"合并_{os.path.basename(filename)}_{random_suffix}"

split_file(filename, num_chunks)

# 检查合并后的文件是否存在，若存在则添加后缀
merge_filename = check_existing_file(merge_filename)

join_files(merge_filename)

if check_integrity(merge_filename):
    print("文件完整性验证通过！")
else:
    print("文件完整性验证失败！")
