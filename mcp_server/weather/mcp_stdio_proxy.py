"""MCP stdio 代理包装器 - 拦截并记录 MCP Server 的输入输出。

用法:
    python mcp_stdio_proxy.py -- <原始命令> [参数...]

示例 (settings.json 配置):
    {
      "mcpServers": {
        "weather": {
          "command": "python",
          "args": [
            "/path/to/mcp_stdio_proxy.py",
            "--log-file", "/path/to/mcp_weather.log",
            "--",
            "npx",
            "-y",
            "@modelcontextprotocol/server-weather"
          ]
        }
      }
    }
"""

import argparse
import json
import logging
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from queue import Queue
from typing import Optional


def setup_logger(log_file: Optional[str] = None) -> logging.Logger:
    """配置日志记录器。"""
    logger = logging.getLogger("mcp_proxy")
    logger.setLevel(logging.DEBUG)
    logger.handlers = []

    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-5s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def log_json(logger: logging.Logger, direction: str, data: dict, truncate: int = 5000):
    """记录 JSON 数据，过长时截断。"""
    raw = json.dumps(data, ensure_ascii=False, indent=None)
    if len(raw) > truncate:
        raw = raw[:truncate] + f" ... [截断，共 {len(raw)} 字符]"
    logger.info(f"[{direction}] {raw}")


def read_json_lines(stream, queue: Queue, logger: logging.Logger, direction: str):
    """从流中读取 JSON-RPC 消息并放入队列。"""
    while True:
        try:
            line = stream.readline()
            if not line:
                queue.put(None)
                break
            line = line.rstrip("\n\r")
            if not line:
                continue
            try:
                msg = json.loads(line)
                log_json(logger, direction, msg)
            except json.JSONDecodeError:
                logger.warning(f"[{direction}] 非 JSON 行: {line[:200]}")
                msg = line
            queue.put(msg)
        except Exception as e:
            logger.error(f"[{direction}] 读取错误: {e}")
            break


def write_json_lines(stream, queue: Queue, logger: logging.Logger, direction: str):
    """从队列取出消息并写入流。"""
    while True:
        item = queue.get()
        if item is None:
            break
        try:
            if isinstance(item, dict):
                line = json.dumps(item, ensure_ascii=False) + "\n"
            else:
                line = str(item) + "\n"
            stream.write(line)
            stream.flush()
        except Exception as e:
            logger.error(f"[{direction}] 写入错误: {e}")
            break


def run_proxy(command: list[str], log_file: Optional[str] = None):
    """启动代理，拦截 stdin/stdout。"""
    import subprocess

    logger = setup_logger(log_file)
    logger.info(f"启动 MCP stdio 代理: {' '.join(command)}")
    logger.info(f"日志文件: {log_file or '仅控制台'}")

    try:
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
    except Exception as e:
        logger.error(f"启动子进程失败: {e}")
        sys.exit(1)

    # stderr 直接透传并记录
    def forward_stderr():
        for line in proc.stderr:
            logger.warning(f"[SERVER STDERR] {line.rstrip()}")
            sys.stderr.write(line)
            sys.stderr.flush()

    stderr_thread = threading.Thread(target=forward_stderr, daemon=True)
    stderr_thread.start()

    # stdin -> 请求队列 -> proc.stdin
    request_queue: Queue = Queue()
    threading.Thread(
        target=read_json_lines,
        args=(sys.stdin, request_queue, logger, "CLI >>> SRV"),
        daemon=True,
    ).start()
    threading.Thread(
        target=write_json_lines,
        args=(proc.stdin, request_queue, logger, "CLI >>> SRV"),
        daemon=True,
    ).start()

    # proc.stdout -> 响应队列 -> stdout
    response_queue: Queue = Queue()
    threading.Thread(
        target=read_json_lines,
        args=(proc.stdout, response_queue, logger, "CLI <<< SRV"),
        daemon=True,
    ).start()
    threading.Thread(
        target=write_json_lines,
        args=(sys.stdout, response_queue, logger, "CLI <<< SRV"),
        daemon=True,
    ).start()

    # 等待子进程结束
    exit_code = proc.wait()
    logger.info(f"MCP Server 已退出，退出码: {exit_code}")
    sys.exit(exit_code)


def main():
    parser = argparse.ArgumentParser(description="MCP stdio 代理包装器")
    parser.add_argument("--log-file", type=str, default=None, help="日志文件路径")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="原始 MCP Server 命令 (-- 之后)")
    args = parser.parse_args()

    if not args.command or args.command[0] != "--":
        parser.error("必须在命令前使用 -- 分隔符，例如: python mcp_stdio_proxy.py -- npx -y @modelcontextprotocol/server-weather")

    real_command = args.command[1:]
    if not real_command:
        parser.error("未提供原始 MCP Server 命令")

    run_proxy(real_command, args.log_file)


if __name__ == "__main__":
    main()
