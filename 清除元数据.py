import os  # 导入os模块，用于文件和目录操作
from mutagen.easyid3 import EasyID3  # 从mutagen库导入EasyID3，用于处理MP3文件的ID3标签
from mutagen.mp4 import MP4  # 从mutagen库导入MP4，用于处理MP4文件的元数据
from mutagen.id3 import ID3NoHeaderError  # 从mutagen库导入ID3NoHeaderError，用于捕获没有ID3标签的异常

def clear_metadata(file_path):
    try:
        # 检查文件扩展名是否为.mp3
        if file_path.endswith(".mp3"):
            audio = EasyID3(file_path)  # 使用EasyID3加载MP3文件
        # 检查文件扩展名是否为.mp4
        elif file_path.endswith(".mp4"):
            audio = MP4(file_path)  # 使用MP4加载MP4文件
        else:
            # 如果文件不是音频文件，则跳过处理
            print(f"跳过非音频文件：{file_path}")
            return

        audio.delete()  # 删除文件的所有元数据
        print(f"成功清除 {file_path} 的元数据")  # 打印成功消息
    except ID3NoHeaderError:
        # 如果文件没有ID3标签，则打印消息
        print(f"文件没有 ID3 标签：{file_path}")
    except Exception as e:
        # 如果在处理过程中发生任何其他异常，则打印错误消息
        print(f"无法清除 {file_path} 的元数据：{e}")

# 定义一个函数来批量处理目录中的所有文件
def batch_process(directory):
    # 检查提供的路径是否是一个存在的目录
    if not os.path.isdir(directory):
        print("指定的路径不存在或不是一个目录。")
        return

    # 使用os.walk遍历目录及其所有子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 检查文件是否以.mp3或.mp4结尾
            if file.endswith(".mp3") or file.endswith(".mp4"):
                file_path = os.path.join(root, file)  # 获取文件的完整路径
                clear_metadata(file_path)  # 调用clear_metadata函数来清除元数据

# 检查当前脚本是否作为主程序运行
if __name__ == "__main__":
    directory = input("请输入要处理的文件夹路径：")  # 从用户那里获取要处理的目录路径
    batch_process(directory)  # 调用batch_process函数来处理目录
