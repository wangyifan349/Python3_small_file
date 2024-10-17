!pip install scikit-image scikit-learn matplotlib

import matplotlib.pyplot as plt
from skimage import data, color, feature
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# 1. 加载人脸数据集
lfw_people = datasets.fetch_lfw_people(min_faces_per_person=70, resize=0.4)
X = lfw_people.images  # 图像数据
y = lfw_people.target  # 标签数据
target_names = lfw_people.target_names  # 标签名称

# 2. 预处理图像数据并提取 HOG 特征
# 将图像转换为灰度并提取 HOG 特征
hog_features = []
for image in X:
    # 转换为灰度
    gray_image = color.rgb2gray(image)
    # 提取 HOG 特征
    hog_feature = feature.hog(
        gray_image, 
        pixels_per_cell=(8, 8), 
        cells_per_block=(2, 2), 
        visualize=False, 
        multichannel=False
    )
    hog_features.append(hog_feature)

# 转换为适合训练的 numpy 数组
X_hog = np.array(hog_features)

# 3. 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_hog, y, test_size=0.3, random_state=42)

# 4. 训练 SVM 分类器
svm_clf = SVC(kernel='linear', C=1.0, random_state=42)
svm_clf.fit(X_train, y_train)

# 5. 测试分类器
y_pred = svm_clf.predict(X_test)

# 6. 打印分类报告和准确率
print("Classification report:")
print(classification_report(y_test, y_pred, target_names=target_names))

print("Accuracy:", accuracy_score(y_test, y_pred))

# 7. 可视化部分分类结果
fig, axes = plt.subplots(3, 5, figsize=(15, 8))
for i, ax in enumerate(axes.ravel()):
    ax.imshow(X_test[i].reshape(50, 37), cmap='gray')
    ax.set_title(f"Pred: {target_names[y_pred[i]]}\nTrue: {target_names[y_test[i]]}")
    ax.axis('off')

plt.show()

"""
1. **数据加载**：
   - 我们使用 `fetch_lfw_people` 数据集，该数据集是一个人脸数据集。我们只选择每个人至少有70张图像的类别。
   - `X` 是包含面部图像的数据，`y` 是标签，`target_names` 是标签的名称（如人名）。
2. **HOG特征提取**：
   - 使用 `skimage.feature.hog` 提取每张图像的HOG特征。HOG特征提取会将图像划分为小块（cells），计算每个小块的梯度方向直方图，从而生成用于分类的特征向量。
3. **SVM分类器**：
   - `SVC` 是来自 `scikit-learn` 的支持向量机分类器。我们在这个示例中使用线性核函数（`kernel='linear'`）进行分类。线性SVM可以很好地处理这个问题，并且训练速度快。
4. **模型训练和预测**：
   - 我们将数据分为训练集和测试集，使用训练集训练SVM分类器，然后在测试集上进行预测。
5. **可视化**：
   - 使用Matplotlib展示部分预测结果，并将预测标签和实际标签进行对比。
### 结果
- **分类报告**：显示每类的分类精度、召回率和F1分数。
- **准确率**：打印模型在测试集上的总体分类准确率。
- **可视化**：展示部分预测的结果，方便你直观理解模型的效果。

### 总结

- **HOG特征**：HOG特征用于提取图像中的局部梯度方向分布，能够有效捕捉到面部的结构化特征。
- **SVM分类器**：SVM是一种强大的线性分类器，能够在HOG特征的基础上区分不同的面部图像。

该代码展示了如何结合HOG特征和SVM进行面部检测或分类的任务，常用于图像处理中。

"""
