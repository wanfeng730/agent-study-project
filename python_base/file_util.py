import os, json, logging

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = 'utf-8'

# json文件读取
def read_json_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding=DEFAULT_ENCODING) as file:
            data = json.load(file)
            return data
        
    except FileNotFoundError:
        logger.error(f'read_json_file 文件不存在：{file_path}')
        return ''


# json文件写入
def write_json_file(file_path: str, data: str) -> None:
    try:
        with open(file_path, 'w', encoding=DEFAULT_ENCODING) as file:
            json.dump(data, file)

    except FileNotFoundError:
        logger.error(f'read_json_file 文件不存在：{file_path}')



