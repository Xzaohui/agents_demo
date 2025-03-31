"""分析智能体模块，实现各种数据分析智能体"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json

from core.base import Agent, Message, Tool, ToolRegistry
from analysis_agents.analysis_tools import (
    MarketTrendAnalysisTool, 
    SellingPointAnalysisTool, 
    CompetitorAnalysisTool, 
    PriceAnalysisTool
)


class AnalysisAgent(Agent):
    """分析智能体基类"""
    
    def __init__(self, agent_id: str, agent_type: str):
        super().__init__(agent_id, agent_type)
        self.tool_registry = ToolRegistry()
        self.available_tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """注册工具"""
        self.available_tools[tool.tool_id] = tool
    
    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息，根据消息内容调用相应的工具进行分析"""
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


class MarketTrendAnalysisAgent(AnalysisAgent):
    """市场趋势分析智能体，负责分析市场趋势"""
    
    def __init__(self, agent_id: str = "market_trend_analysis_agent"):
        super().__init__(agent_id, "analysis_agent")
        # 注册市场趋势分析工具
        self.register_tool(MarketTrendAnalysisTool())


class SellingPointAnalysisAgent(AnalysisAgent):
    """卖点分析智能体，负责分析卖点数据"""
    
    def __init__(self, agent_id: str = "selling_point_analysis_agent"):
        super().__init__(agent_id, "analysis_agent")
        # 注册卖点分析工具
        self.register_tool(SellingPointAnalysisTool())


class CompetitorAnalysisAgent(AnalysisAgent):
    """竞争对手分析智能体，负责分析竞争对手数据"""
    
    def __init__(self, agent_id: str = "competitor_analysis_agent"):
        super().__init__(agent_id, "analysis_agent")
        # 注册竞争对手分析工具
        self.register_tool(CompetitorAnalysisTool())


class PriceAnalysisAgent(AnalysisAgent):
    """价格分析智能体，负责分析价格数据"""
    
    def __init__(self, agent_id: str = "price_analysis_agent"):
        super().__init__(agent_id, "analysis_agent")
        # 注册价格分析工具
        self.register_tool(PriceAnalysisTool())


class ComprehensiveAnalysisAgent(AnalysisAgent):
    """综合分析智能体，负责整合多种分析结果"""
    
    def __init__(self, agent_id: str = "comprehensive_analysis_agent"):
        super().__init__(agent_id, "analysis_agent")
        # 注册所有分析工具
        self.register_tool(MarketTrendAnalysisTool())
        self.register_tool(SellingPointAnalysisTool())
        self.register_tool(CompetitorAnalysisTool())
        self.register_tool(PriceAnalysisTool())
    
    def integrate_analysis_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """整合多个分析结果"""
        # 这里应该实现结果整合的逻辑
        # 例如，从不同的分析结果中提取关键信息，生成综合报告
        integrated_result = {
            "category": results.get("market_trend", {}).get("category", ""),
            "date_range": results.get("market_trend", {}).get("date_range", {}),
            "market_summary": results.get("market_trend", {}).get("summary", ""),
            "selling_point_summary": results.get("selling_point", {}).get("summary", ""),
            "competitor_summary": results.get("competitor", {}).get("summary", ""),
            "price_summary": results.get("price", {}).get("summary", ""),
            "recommendations": []
        }
        
        # 生成综合建议
        if "market_trend" in results and "trends" in results["market_trend"]:
            market_trends = results["market_trend"]["trends"]
            for metric, trend in market_trends.items():
                if trend.get("trend_direction") == "上升" and trend.get("growth_rate", 0) > 0.1:
                    integrated_result["recommendations"].append(f"市场{metric}增长迅速，建议加大投入")
        
        if "selling_point" in results and "effective_selling_points" in results["selling_point"]:
            effective_points = results["selling_point"]["effective_selling_points"]
            if effective_points:
                top_points = [point["name"] for point in effective_points[:2]]
                integrated_result["recommendations"].append(f"重点推广以下卖点：{', '.join(top_points)}")
        
        if "competitor" in results and "threats" in results["competitor"]:
            threats = results["competitor"]["threats"]
            if threats:
                threat_comps = [threat["competitor"] for threat in threats[:2]]
                integrated_result["recommendations"].append(f"警惕竞争对手：{', '.join(threat_comps)}的市场动向")
        
        if "price" in results and "optimal_price_range" in results["price"]:
            price_range = results["price"]["optimal_price_range"]
            integrated_result["recommendations"].append(f"建议定价区间：{price_range['min']}~{price_range['max']}")
        
        return integrated_result