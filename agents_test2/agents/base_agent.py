from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """Agent响应的标准格式"""
    success: bool
    data: Any
    message: str = ""

class BaseAgent(ABC):
    """基础智能体类"""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    async def execute(self, task_input: Dict[str, Any]) -> AgentResponse:
        """执行智能体任务的抽象方法"""
        pass
    
    def validate_input(self, task_input: Dict[str, Any]) -> bool:
        """验证输入参数"""
        return True

    def format_response(self, success: bool, data: Any = None, message: str = "") -> AgentResponse:
        """格式化响应"""
        return AgentResponse(
            success=success,
            data=data,
            message=message
        )
