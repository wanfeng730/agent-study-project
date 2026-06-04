from datetime import datetime

def get_current_date_time() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def get_current_date_time_cn() -> str:
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H时%M分%S秒")