import os
import shutil
from datetime import datetime

# 定义源硬盘路径和目标目录
source_directory = 'D:\\'  # 源硬盘路径（例如 D 盘）
target_directory = 'D:\\整理'  # 目标目录

# 支持的文件扩展名
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')

def rename_file(file_path):
    """重命名文件以避免冲突"""
    name, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path

    while os.path.exists(new_file_path):
        new_file_path = f"{name}_{counter}{ext}"
        counter += 1

    return new_file_path

# 遍历源目录
for root, dirs, files in os.walk(source_directory):
    for file in files:
        # 获取文件扩展名
        ext = os.path.splitext(file)[1].lower()
        
        # 检查是否是图片或视频
        if ext in image_extensions or ext in video_extensions:
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            
            # 检查是否是目标目录，避免重复操作
            if target_directory in file_path:
                continue
            
            # 获取文件的修改时间
            timestamp = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            
            # 创建目标目录（按日期分组）
            date_directory = os.path.join(target_directory, date)
            os.makedirs(date_directory, exist_ok=True)
            
            # 生成新的文件名
            new_file_path = rename_file(os.path.join(date_directory, file))
            
            # 移动文件到目标目录，保持原始的修改时间和创建时间
            shutil.move(file_path, new_file_path)
            
            # 设置文件的修改时间
            os.utime(new_file_path, (timestamp, timestamp))
            
            print(f"Moved: {file_path} to {new_file_path}")
