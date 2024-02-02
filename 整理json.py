import json
import os

# 定义一个函数，用于递归地提取JSON数据中的所有字符串
def extract_strings(data, strings=None):
    if strings is None:
        strings = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                strings.append(value)
            elif isinstance(value, (dict, list)):
                extract_strings(value, strings)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                strings.append(item)
            elif isinstance(item, (dict, list)):
                extract_strings(item, strings)
    return strings

# 指定包含JSON文件的目录
json_directory = 'path/to/json_directory'  # 替换为你的JSON文件所在的目录路径

# 使用os.walk遍历目录及其所有子目录
for root, dirs, files in os.walk(json_directory):
    for filename in files:
        # 检查文件扩展名是否为.json
        if filename.endswith('.json'):
            # 构建完整的文件路径
            file_path = os.path.join(root, filename)
            
            # 读取JSON数据
            with open(file_path, 'r', encoding='utf-8') as f:  # 确保使用正确的编码读取文件
                data = json.load(f)
            
            # 提取所有字符串
            all_strings = extract_strings(data)
            
            # 构建新的文件名，用于保存提取的字符串
            new_filename = f'extracted_{filename}'
            new_file_path = os.path.join(root, new_filename)
            
            # 将提取的字符串保存到新的JSON文件中
            with open(new_file_path, 'w', encoding='utf-8') as f:  # 使用utf-8编码写入文件
                json.dump(all_strings, f, indent=4)
            
            # 打印信息，表明文件已被处理
            print(f'提取字符串从 {file_path} 到 {new_file_path}')
