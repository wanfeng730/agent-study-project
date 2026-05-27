# pytorch 张量类型转换、

import numpy as np
import torch

# 张量 -> np数组(numpy.ndarray)
t1 = torch.tensor([1, 6, 3, 5])
n1 = t1.numpy()
print(f'n1: {n1}, 类型：{type(n1)}')

# np数组 -> 张量
n2 = np.arange(1, 10, 2)
t2 = torch.from_numpy(n2)
print(f't2: {t2}, 类型：{type(t2)}')