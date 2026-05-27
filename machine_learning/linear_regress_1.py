# 线性回归: 一元线性回归

from sklearn.linear_model import LinearRegression

# 训练集
x_train = [[160], [166], [172], [174], [180]]
y_train = [56.3, 60.6, 65.1, 68.5, 75]



# 模型
model_linear = LinearRegression()

# 进行训练
model_linear.fit(x_train, y_train)

# 获取权重：coef_
# 获取偏置：intercept_
print(f'模型训练已完成 weight={model_linear.coef_}, bias={model_linear.intercept_}')

# 测试集
x_test = [[176], [183]]
# 测试
y_test = model_linear.predict(x_test)
print(f'模型测试结果: {y_test}')
