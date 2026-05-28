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



# 求和、总和  、
t7 = t4.sum()           # 整体求和
t7 = t4.sum(dim=0)      # dim=0 按列求和
t7 = t4.sum(dim=1)      # dim=1 按行求和
print(f't7: {t7}')


# 平均值  必须为float或double类型
# dim为维度（dimission）
t6 = t1.type(torch.float).mean()
t6 = t3.type(torch.float).mean(dim=0)
print(f't6: {t6}')