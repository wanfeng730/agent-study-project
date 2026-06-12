# Desc  : demo_middleware.
# Time  : 2026-06-12 20:48
# Author: wanfeng
import logging
from typing import Callable, Any

from langchain.agents import AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call, ModelRequest
from langchain.agents.middleware.types import ResponseT, ModelResponse, ExtendedModelResponse
from langchain_core.messages import ToolMessage, AIMessage
from langgraph.prebuilt.tool_node import ToolCallRequest, ContextT
from langgraph.runtime import Runtime
from langgraph.types import Command

logger = logging.getLogger(__name__)

# agent调用前
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime[ContextT]) -> None:
    logger.info(f'[Middleware: log_before_agent]: {len(state['messages'])}')
    return

# agent调用后
@after_agent
def log_after_agent(state: AgentState, runtime: Runtime[ContextT]) -> None:
    logger.info(f'[Middleware: log_after_agent]: {len(state['messages'])}')
    return

# 模型调用前
@before_model
def log_before_model(state: AgentState, runtime: Runtime[ContextT]) -> None:
    logger.info(f'[Middleware: log_before_model]: {len(state['messages'])}')
    return

# 模型调用后
@after_model
def log_after_model(state: AgentState, runtime: Runtime[ContextT]) -> None:
    logger.info(f'[Middleware: log_after_model]: {len(state['messages'])}')
    return

# 模型调用中
@wrap_model_call
def retry_on_error(
        request: ModelRequest[ContextT],
        handler: Callable[[ModelRequest[ContextT]], ModelResponse[ResponseT]]
) -> ModelResponse[ResponseT] | AIMessage | ExtendedModelResponse[ResponseT]:
    logger.info(f'[Middleware: retry_on_error]: \n  request: {type(request)}\n  handler: {type(handler)}')
    max_retries = 3
    for retry in range(max_retries):
        try:
            logger.info(f'[Middleware: retry_on_error]: 重试第{retry}次')
            return handler(request)
        except Exception as e:
            if retry >= max_retries:

                raise   # 重新抛出，不影响上层调用者捕获
    return None

# 工具调用中
@wrap_tool_call
def log_tool_call(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]]
) -> ToolMessage | Command[Any]:
    logger.info(f'[Middleware: log_tool_call]: \n  request: {type(request)}\n  handler: {type(handler)}')
    # 调用的工具名、参数
    tool_name = request.tool_call['name']
    tool_args = request.tool_call['args']

    try:
        result = handler(request)
        logger.info(f'[Middleware: log_tool_call]: Call Tool Success')
        return result
    except Exception as e:
        logger.error(f'[Middleware: log_tool_call]: Call Tool Failed. {e}')
        raise



