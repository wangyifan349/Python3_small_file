import os
import shutil
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def hash_file(file_path):
    """计算文件的SHA-256哈希值"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def rename_file(original_name, file_hash, ext):
    """根据文件哈希和原始文件名生成新的文件名"""
    base_name = os.path.splitext(original_name)[0]
    return f"{base_name}_{file_hash}{ext}"


def move_file(file_path, dest_path):
    """移动文件到目标路径"""
    shutil.move(file_path, dest_path)


def copy_file(file_path, dest_path):
    """拷贝文件到目标路径"""
    shutil.copy2(file_path, dest_path)


def process_file(file_path, dest_dir, seen_hashes, move=False):
    """处理单个文件，仅处理图片和视频文件"""
    ext = os.path.splitext(file_path)[1].lower()
    
    # 仅处理图片和视频文件
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', 
                   '.mp4', '.avi', '.mkv', '.flv']:
        return  # 跳过非图片/视频文件

    file_hash = hash_file(file_path)

    # 检查是否已经处理过该文件
    if file_hash in seen_hashes:
        print(f"重复文件，跳过: {file_path}")
        return
    seen_hashes.add(file_hash)

    # 获取文件修改时间
    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    year_month = mod_time.strftime("%Y-%m")

    # 确定文件类型
    file_type = 'images' if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp'] else 'videos'

    target_dir = os.path.join(dest_dir, file_type, year_month)
    os.makedirs(target_dir, exist_ok=True)

    # 生成新的文件名
    new_file_name = rename_file(os.path.basename(file_path), file_hash, ext)
    target_file_path = os.path.join(target_dir, new_file_name)

    # 检查目标文件是否已存在
    if os.path.exists(target_file_path):
        print(f"目标文件已存在，跳过: {target_file_path}")
        return

    # 拷贝或移动文件
    if move:
        move_file(file_path, target_file_path)
    else:
        copy_file(file_path, target_file_path)
    
    print(f"{'移动' if move else '拷贝'}文件: {file_path} 到 {target_file_path}")


def copy_and_organize_files(src_dirs, dest_dir, move=False):
    """拷贝或移动文件到目标目录，仅处理图片和视频"""
    seen_hashes = set()

    # 先计算哈希值，避免重复
    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path, dest_dir, seen_hashes, move)

    messagebox.showinfo("完成", "文件拷贝/移动和整理完成！")


def select_src_dirs():
    """选择源目录"""
    src_dirs = filedialog.askdirectory(mustexist=True, title="选择源目录")
    if src_dirs:
        src_dir_list.append(src_dirs)
        update_src_display()


def select_multiple_src_dirs():
    """选择多个源目录"""
    src_dirs = filedialog.askdirectory(mustexist=True, title="选择多个源目录")
    if src_dirs:
        src_dir_list.append(src_dirs)
        update_src_display()


def update_src_display():
    """更新源目录显示"""
    src_dir_display.config(state='normal')
    src_dir_display.delete(1.0, tk.END)
    src_dir_display.insert(tk.END, "\n".join(src_dir_list))
    src_dir_display.config(state='disabled')


def select_dest_dir():
    """选择目标目录"""
    dest_dir = filedialog.askdirectory(mustexist=True, title="选择目标目录")
    if dest_dir:
        dest_dir_path.set(dest_dir)


def start_copying():
    """启动拷贝或移动过程"""
    if not src_dir_list or not dest_dir_path.get():
        messagebox.showwarning("警告", "请确保选择了源目录和目标目录！")
        return

    move_files = move_var.get()  # 获取用户选择的操作
    # 启动后台线程进行文件拷贝或移动
    executor.submit(copy_and_organize_files, src_dir_list.copy(), dest_dir_path.get(), move_files)


# GUI设置
src_dir_list = []

root = tk.Tk()

src_dir_display = tk.StringVar()
dest_dir_path = tk.StringVar()

root.title("文件拷贝和整理工具")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

src_dir_label = tk.Label(frame, text="源目录:")
src_dir_label.pack()

src_dir_display = scrolledtext.ScrolledText(frame, width=70, height=10, state='disabled')
src_dir_display.pack(pady=5)

select_src_button = tk.Button(frame, text="选择源目录", command=select_multiple_src_dirs)
select_src_button.pack(pady=5)

dest_dir_label = tk.Label(frame, text="目标目录:")
dest_dir_label.pack()

dest_dir_entry = tk.Entry(frame, textvariable=dest_dir_path, width=70)
dest_dir_entry.pack(pady=5)

select_dest_button = tk.Button(frame, text="选择目标目录", command=select_dest_dir)
select_dest_button.pack(pady=5)

# 选择操作类型
move_var = tk.BooleanVar()
move_checkbutton = tk.Checkbutton(frame, text="移动文件", variable=move_var)
move_checkbutton.pack(pady=5)

start_button = tk.Button(frame, text="开始拷贝/移动", command=start_copying)
start_button.pack(pady=20)

# 启动线程池
executor = ThreadPoolExecutor()

root.mainloop()
