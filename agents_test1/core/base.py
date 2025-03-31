"""基础架构模块，定义了智能体系统的核心组件和接口"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Callable
import json


class Message:
    """消息类，用于智能体之间的通信"""
    
    def __init__(self, sender: str, receiver: str, content: Any, msg_type: str = "request"):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.msg_type = msg_type  # request, response, notification
        
    def to_dict(self) -> Dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "msg_type": self.msg_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            content=data["content"],
            msg_type=data["msg_type"]
        )


class Agent(ABC):
    """智能体基类，定义了智能体的基本接口"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.message_queue: List[Message] = []
        
    def receive_message(self, message: Message) -> None:
        """接收消息"""
        if message.receiver == self.agent_id:
            self.message_queue.append(message)
    
    def send_message(self, receiver: str, content: Any, msg_type: str = "request") -> Message:
        """发送消息"""
        message = Message(self.agent_id, receiver, content, msg_type)
        return message
    
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息，返回响应消息"""
        pass
    
    @abstractmethod
    def run(self) -> Any:
        """运行智能体的主要逻辑"""
        pass


class AgentRegistry:
    """智能体注册表，用于管理所有智能体"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance.agents = {}
        return cls._instance
    
    def register(self, agent: Agent) -> None:
        """注册智能体"""
        self.agents[agent.agent_id] = agent
    
    def unregister(self, agent_id: str) -> None:
        """注销智能体"""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取智能体"""
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: str) -> List[Agent]:
        """根据类型获取智能体"""
        return [agent for agent in self.agents.values() if agent.agent_type == agent_type]
    
    def get_all_agents(self) -> List[Agent]:
        """获取所有智能体"""
        return list(self.agents.values())


class Tool(ABC):
    """工具基类，定义了工具的基本接口"""
    
    def __init__(self, tool_id: str, tool_name: str, description: str):
        self.tool_id = tool_id
        self.tool_name = tool_name
        self.description = description
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """执行工具的主要逻辑"""
        pass
    
    def to_dict(self) -> Dict:
        return {
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "description": self.description
        }


class ToolRegistry:
    """工具注册表，用于管理所有工具"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance
    
    def register(self, tool: Tool) -> None:
        """注册工具"""
        self.tools[tool.tool_id] = tool
    
    def unregister(self, tool_id: str) -> None:
        """注销工具"""
        if tool_id in self.tools:
            del self.tools[tool_id]
    
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """获取工具"""
        return self.tools.get(tool_id)
    
    def get_all_tools(self) -> List[Tool]:
        """获取所有工具"""
        return list(self.tools.values())
    
    def get_tool_descriptions(self) -> List[Dict]:
        """获取所有工具的描述"""
        return [tool.to_dict() for tool in self.tools.values()]