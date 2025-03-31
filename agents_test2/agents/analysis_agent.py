from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentResponse

class MarketAnalysisAgent(BaseAgent):
    """市场分析智能体"""
    
    def __init__(self):
        super().__init__("market_analysis_agent")
    
    async def execute(self, task_input: Dict[str, Any]) -> AgentResponse:
        try:
            market_data = task_input.get("market_data")
            sales_data = task_input.get("sales_data")
            
            if not all([market_data, sales_data]):
                return self.format_response(
                    False,
                    None,
                    "Missing required data: market_data, sales_data"
                )
            
            # 执行市场分析
            analysis_result = {
                "market_overview": {
                    "total_market_size": market_data["market_size"],
                    "market_growth": market_data["growth_rate"],
                    "market_share": sales_data["total_sales"] / market_data["market_size"]
                },
                "competitive_analysis": {
                    "competitor_count": len(market_data["competitors"]),
                    "market_position": "Leader" if sales_data["total_sales"] > market_data["market_size"] * 0.3 else "Follower"
                },
                "channel_analysis": {
                    "channel_distribution": sales_data["sales_channels"],
                    "recommended_focus": "online" if sales_data["sales_channels"]["online"] > 0.5 else "offline"
                }
            }
            
            return self.format_response(True, analysis_result)
            
        except Exception as e:
            return self.format_response(False, None, str(e))

class TrendAnalysisAgent(BaseAgent):
    """趋势分析智能体"""
    
    def __init__(self):
        super().__init__("trend_analysis_agent")
    
    async def execute(self, task_input: Dict[str, Any]) -> AgentResponse:
        try:
            market_data = task_input.get("market_data")
            historical_data = task_input.get("historical_data", [])
            
            if not market_data:
                return self.format_response(
                    False,
                    None,
                    "Missing required data: market_data"
                )
            
            # 执行趋势分析
            trend_analysis = {
                "growth_trend": {
                    "current_growth": market_data["growth_rate"],
                    "trend_type": "上升" if market_data["growth_rate"] > 0.1 else "平稳" if market_data["growth_rate"] > 0 else "下降"
                },
                "market_maturity": "成熟期" if 0.05 <= market_data["growth_rate"] <= 0.15 else "成长期" if market_data["growth_rate"] > 0.15 else "衰退期",
                "future_projection": {
                    "short_term": market_data["market_size"] * (1 + market_data["growth_rate"]),
                    "confidence": "高" if len(historical_data) > 5 else "中"
                }
            }
            
            return self.format_response(True, trend_analysis)
            
        except Exception as e:
            return self.format_response(False, None, str(e))
