# Desc  : utils.
# Time  : 2026/6/12 16:29
# Author: wanfeng


# 读取文件内容
def read_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content;