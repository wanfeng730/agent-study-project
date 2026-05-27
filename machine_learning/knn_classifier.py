# KNN算法 回归问题

from sklearn.neighbors import KNeighborsClassifier


# 训练集的特征，每个元素包含多个特征值
x_train = [
    [0],
    [1],
    [2],
    [3]
]
# 训练集的标签，每个元素为一个值
y_train = [0, 0, 1, 1]

# 测试集
x_test = [[5]]

# knn分类模型
# n_neighbors 为k值
model_classifier = KNeighborsClassifier(n_neighbors=2)

# 模型训练
model_classifier.fit(x_train, y_train)
print('分类模型训练已完成')

# 模型测试
y_test = model_classifier.predict(x_test)
print(f'分类模型测试结果: {y_test}')