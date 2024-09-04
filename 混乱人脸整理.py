import os
import cv2
import face_recognition
from sklearn.cluster import DBSCAN
import shutil

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append((filename, img))
    return images

def extract_face_encodings(images):
    encodings = []
    for filename, img in images:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
        for face_encoding in face_encodings:
            encodings.append((filename, face_encoding))
    return encodings

def cluster_faces(encodings, eps=0.5, min_samples=2):
    encodings_only = [encoding for _, encoding in encodings]
    clustering_model = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    clustering_model.fit(encodings_only)
    labels = clustering_model.labels_
    
    clusters = {}
    for label, (filename, encoding) in zip(labels, encodings):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(filename)
    return clusters

def save_clusters(clusters, src_folder, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    for cluster_id, filenames in clusters.items():
        for idx, filename in enumerate(filenames):
            src_path = os.path.join(src_folder, filename)
            dst_filename = f"{cluster_id}_{idx}_{filename}"
            dst_path = os.path.join(dst_folder, dst_filename)
            shutil.copy(src_path, dst_path)

def main():
    folder_path = 'path_to_your_images_folder'  # 替换为你的图片文件夹路径
    images = load_images_from_folder(folder_path)
    encodings = extract_face_encodings(images)
    clusters = cluster_faces(encodings)
    
    for cluster_id, filenames in clusters.items():
        print(f"聚类 {cluster_id}:")
        for filename in filenames:
            print(f" - {filename}")
    
    save_clusters(clusters, folder_path, 'path_to_save_clusters')  # 替换为你想保存聚类结果的文件夹路径

if __name__ == "__main__":
    main()
