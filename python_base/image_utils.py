import os
import base64
from pathlib import Path

def image_to_base64_url(image_path: str) -> str:
    """
    将图片转换为 base64 格式的 data URL
    
    Args:
        image_path: 图片文件路径
    
    Returns:
        base64 格式的 data URL，格式如：data:image/jpg;base64,xxxxx
    
    Raises:
        FileNotFoundError: 图片文件不存在
        ValueError: 不支持的文件格式
    """
    # 检查文件是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    # 获取图片格式
    ext = os.path.splitext(image_path)[1].lstrip('.').lower()
    
    # 支持的图片格式映射
    supported_formats = {
        'jpg': 'jpeg',
        'jpeg': 'jpeg',
        'png': 'png',
        'gif': 'gif',
        'webp': 'webp',
        'bmp': 'bmp',
        'svg': 'svg+xml'
    }
    
    if ext not in supported_formats:
        raise ValueError(f"不支持的图片格式: {ext}")
    
    # 读取图片并编码
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # 构建 data URL
    mime_type = supported_formats.get(ext, ext)
    base64_str = base64.b64encode(image_data).decode('utf-8')
    image_url = f"data:image/{mime_type};base64,{base64_str}"
    
    return image_url