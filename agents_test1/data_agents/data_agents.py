"""数据获取智能体模块，实现各种数据获取智能体"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

from core.base import Agent, Message, Tool, ToolRegistry
from data_agents.data_tools import MarketDataTool, SellingPointDataTool, CompetitorDataTool, PriceDataTool


class DataAgent(Agent):
    """数据获取智能体基类"""
    
    def __init__(self, agent_id: str, agent_type: str):
        super().__init__(agent_id, agent_type)
        self.tool_registry = ToolRegistry()
        self.available_tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """注册工具"""
        self.available_tools[tool.tool_id] = tool
    
    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息，根据消息内容调用相应的工具获取数据"""
        if message.msg_type != "request":
            return None
        
        content = message.content
        if not isinstance(content, dict) or "tool_id" not in content:
            return self.send_message(
                receiver=message.sender,
                content={"error": "Invalid request format. Must contain 'tool_id' field."},
                msg_type="error"
            )
        
        tool_id = content["tool_id"]
        params = content.get("params", {})
        
        if tool_id not in self.available_tools:
            return self.send_message(
                receiver=message.sender,
                content={"error": f"Tool '{tool_id}' not available in this agent."},
                msg_type="error"
            )
        
        try:
            tool = self.available_tools[tool_id]
            result = tool.execute(params)
            return self.send_message(
                receiver=message.sender,
                content=result,
                msg_type="response"
            )
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                content={"error": f"Error executing tool: {str(e)}"},
                msg_type="error"
            )
    
    def run(self) -> None:
        """运行智能体的主要逻辑，处理消息队列中的消息"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            if response:
                # 这里应该是将响应消息发送到消息总线或直接发送给接收者
                # 在实际实现中，可能需要一个消息总线来管理消息的传递
                pass


class MarketDataAgent(DataAgent):
    """市场数据获取智能体，负责获取市场相关数据"""
    
    def __init__(self, agent_id: str = "market_data_agent"):
        super().__init__(agent_id, "data_agent")
        # 注册市场数据工具
        self.register_tool(MarketDataTool())
        self.register_tool(PriceDataTool())


class SellingPointDataAgent(DataAgent):
    """卖点数据获取智能体，负责获取卖点相关数据"""
    
    def __init__(self, agent_id: str = "selling_point_data_agent"):
        super().__init__(agent_id, "data_agent")
        # 注册卖点数据工具
        self.register_tool(SellingPointDataTool())


class CompetitorDataAgent(DataAgent):
    """竞争对手数据获取智能体，负责获取竞争对手相关数据"""
    
    def __init__(self, agent_id: str = "competitor_data_agent"):
        super().__init__(agent_id, "data_agent")
        # 注册竞争对手数据工具
        self.register_tool(CompetitorDataTool())


class ComprehensiveDataAgent(DataAgent):
    """综合数据获取智能体，可以获取多种类型的数据"""
    
    def __init__(self, agent_id: str = "comprehensive_data_agent"):
        super().__init__(agent_id, "data_agent")
        # 注册所有数据工具
        self.register_tool(MarketDataTool())
        self.register_tool(SellingPointDataTool())
        self.register_tool(CompetitorDataTool())
        self.register_tool(PriceDataTool())