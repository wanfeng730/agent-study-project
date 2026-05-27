# pytorch 张量运算

import numpy as np
import torch


t1 = torch.tensor([1, 6, 3, 5])

# 加减乘除
t2 = t1.add(10)
t2 = t1.sub(10)
t2 = t1.mul(10)
t2 = t1.div(10)

# 取反
t2 = t1.neg()

# 整除
t2 = t1 // 3

# 方法名后带下划线会修改t1的值
# t2 = t1.add_(10)

print(f't1: {t1}')
print(f't2: {t2}')


t3 = torch.tensor([
    [1],
    [3],
    [5],
    [3]
])

# 点乘
# 两个张量的维度相同，对应位置的元素相乘
t4 = t1.mul(t3)
print(f't4: {t4}')

# 矩阵乘法
t5 = t1.matmul(t3)
# t5 = t1 @ t3
print(f't5: {t5}')
