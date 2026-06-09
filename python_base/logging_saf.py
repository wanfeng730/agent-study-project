import logging
import os

# https://docs.python.org/3/library/logging.html#logrecord-attributes


# ANSI 颜色代码
class Colors:
    RESET = '\033[0m'
    # 文字颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    # 背景颜色
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    # 样式
    BOLD = '\033[1m'
    DIM = '\033[2m'

class ColorfulFormatter(logging.Formatter):
    """继承默认的日志格式化器，重写format方法时加入ANSI颜色代码"""
    
    LEVEL_COLORS = {
        logging.DEBUG: Colors.BLUE,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.BG_RED + Colors.WHITE + Colors.BOLD,
    }
    
    def format(self, record):
        # 保存原始级别名称
        original_levelname = record.levelname
        # 添加颜色
        color = self.LEVEL_COLORS.get(record.levelno, Colors.WHITE)
        # 格式化日志名称（包含颜色代码、宽度8左对齐）
        record.levelname = f"{color}{original_levelname:<8}{Colors.RESET}"
        result = super().format(record)
        # 恢复原始级别名称
        record.levelname = original_levelname
        return result



def init_root_logger(log_file='logs/logging_saf.log', log_level=logging.INFO):
    """配置日志：同时输出到控制台和文件"""
    
    # 创建日志目录
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # 获取根 Logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 清除已有的 Handlers（避免重复）
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # 文件日志格式化器
    file_formatter = logging.Formatter(
        fmt='[%(filename)s: %(lineno)d] %(asctime)s.%(msecs)03d %(levelname)-5s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台日志格式化器
    console_formatter = ColorfulFormatter(
        fmt='%(asctime)s.%(msecs)03d %(levelname)-5s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件 Handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    # 控制台 Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    # 添加 Handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
