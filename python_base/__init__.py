import inspect

# 从 python文件导入主要功能
from .logging_saf import init_root_logger
from .image_utils import image_to_base64_url

from . import date_util


# 定义 __all__ 指定导出的内容
__all__ = [
    'init_root_logger',
    'image_to_base64_url'
]

# date_util的所有公共方法
for name, obj in inspect.getmembers(date_util):
    if inspect.isfunction(obj) and not name.startswith('_'):
        globals()[name] = obj
        __all__.append(name)