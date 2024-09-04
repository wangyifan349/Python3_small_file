import os
import shutil
import face_recognition
import cv2

def load_known_faces(face_dir):
    """
    加载已知人脸库中的人脸图像，并提取它们的编码。

    :param face_dir: 人脸库文件夹路径
    :return: 已知人脸的编码列表和对应的名字列表
    """
    known_faces = []
    known_names = []
    for filename in os.listdir(face_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(face_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(os.path.splitext(filename)[0])
    return known_faces, known_names

def ensure_unique_filename(directory, filename):
    """
    确保文件名在目录中唯一，如果存在重名则添加数字后缀。

    :param directory: 目标目录
    :param filename: 原始文件名
    :return: 唯一的文件名
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{extension}"
        counter += 1
    return unique_filename

def process_image(image_path, known_faces, known_names, output_dir):
    """
    处理单个图像文件，识别人脸并将图像复制到相应的分类文件夹中。

    :param image_path: 图像文件路径
    :param known_faces: 已知人脸的编码列表
    :param known_names: 已知人脸的名字列表
    :param output_dir: 输出文件夹路径
    """
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        person_dir = os.path.join(output_dir, name)
        os.makedirs(person_dir, exist_ok=True)
        unique_filename = ensure_unique_filename(person_dir, os.path.basename(image_path))
        shutil.copy(image_path, os.path.join(person_dir, unique_filename))

def process_video(video_path, known_faces, known_names, output_dir):
    """
    处理单个视频文件，识别人脸并将视频复制到相应的分类文件夹中。

    :param video_path: 视频文件路径
    :param known_faces: 已知人脸的编码列表
    :param known_names: 已知人脸的名字列表
    :param output_dir: 输出文件夹路径
    """
    video_capture = cv2.VideoCapture(video_path)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(frame_count // 10, 1)  # 处理每个视频的10帧

    for frame_number in range(0, frame_count, frame_interval):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

            person_dir = os.path.join(output_dir, name)
            os.makedirs(person_dir, exist_ok=True)
            unique_filename = ensure_unique_filename(person_dir, os.path.basename(video_path))
            shutil.copy(video_path, os.path.join(person_dir, unique_filename))
            break  # 只根据第一次匹配分类视频

def main(input_dir, face_dir, output_dir):
    """
    主函数，遍历输入文件夹中的所有文件，并根据文件类型调用相应的处理函数。

    :param input_dir: 输入文件夹路径
    :param face_dir: 人脸库文件夹路径
    :param output_dir: 输出文件夹路径
    """
    known_faces, known_names = load_known_faces(face_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                process_image(file_path, known_faces, known_names, output_dir)
            elif file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                process_video(file_path, known_faces, known_names, output_dir)

if __name__ == "__main__":
    input_dir = "path/to/your/input_directory"  # 输入文件夹路径
    face_dir = "path/to/your/face_directory"    # 人脸库文件夹路径
    output_dir = "path/to/your/output_directory"  # 输出文件夹路径

    main(input_dir, face_dir, output_dir)
