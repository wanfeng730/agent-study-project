# KNN算法 回归问题

from sklearn.neighbors import KNeighborsRegressor


# 训练集的特征，每个元素包含多个特征值
x_train = [
    [0, 1, 1],
    [1, 1, 0],
    [2, 4, 5],
    [3, 8, 7]
]
# 训练集的标签，每个元素为一个值
y_train = [4.6, 3.0, 2.5, 2.0]

# 测试集
x_test = [
    [5, 4, 3],
    [0, 0, 0]
]

# knn回归模型
model_regress = KNeighborsRegressor(n_neighbors=2)

# 模型训练
model_regress.fit(x_train, y_train)
print('回归模型训练已完成')

# 模型预测
y_test = model_regress.predict(x_test)
print(f'回归模型预测结果：{y_test}')