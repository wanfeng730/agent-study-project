# pytorch 张量类型转换、

import numpy as np
import torch

t1 = torch.tensor([1, 6, 3, 5])
t2 = torch.tensor([1, 6, 3, 5], dtype=torch.float)
print(f't1: {t1}, 元素类型：{t1.dtype}')

# 使用.type()转类型
t1_convert = t1.type(torch.float)
print(f't1_convert: {t1_convert}, 元素类型：{t1_convert.dtype}')