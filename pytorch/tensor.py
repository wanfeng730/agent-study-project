
import numpy as np
import torch


# 创建张量：标量
t1 = torch.tensor(10)
print(f't1: {t1}, type: {type(t1)}')

# 创建张量：二维数组
t2 = torch.tensor([
    [1, 2, 3],
    [4, 5, 6]
])
print(f't2: {t2}, type: {type(t2)}')

# 创建张量：numpy数组
data3 = np.random.randint(0, 10, size=[2, 3])
t3 = torch.tensor(data3)
print(f't3: {t3}, type: {type(t3)}')


# 创建张量：指定形状（随机数）
t4 = torch.Tensor(2, 3, 4)
print(f't4: {t4}, type: {type(t4)}')

# 创建张量：指定数据类型 如果类型不匹配则会自动转类型，转不了报错
"""
[CPU]
    torch.FloatTensor()
    torch.IntTensor()
    torch.LongTensor()
[GPU]
    torch.cuda.FloatTensor()
    torch.cuda.IntTensor()
    torch.cuda.LongTensor()
"""
data5 = np.random.randint(0, 10, size=(2, 3))
t5 = torch.FloatTensor(data5);
print(f't5: {t5}, type: {type(t5)}')


# 创建全1张量 2行，3列
t6 = torch.ones(2, 3)
print(f't6: {t6}')

# 创建全1张量 基于某个张量的格式
t7 = torch.ones_like(t3)
print(f't7: {t7}')

# 创建全0张量 2行3列
t8 = torch.zeros(2, 3)
print(f't8: {t8}')

# 创建全0张量 2行3列
t9 = torch.zeros_like(t3)
print(f't9: {t9}')

# 创建全为指定值的张量 size为尺寸，fill_value为指定值
t10 = torch.full(size=(2, 3), fill_value=34)
print(f't10: {t10}')

# 创建全为指定值的张量 基于某个张量的尺寸
t11 = torch.full_like(t3, fill_value=34)
print(f't11: {t11}')



# 创建线性张量 按步长   torch.arange(start, end, step)
t12 = torch.arange(0, 10, 2)
print(f't12: {t12}')

# 创建线性张量 按个数   torch.linspace(start, end, count)     
t13 = torch.linspace(1, 10, 5)
print(f't13: {t13}')


# 创建随机张量
t14 = torch