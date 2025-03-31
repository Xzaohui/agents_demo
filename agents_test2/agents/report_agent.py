from typing import Any, Dict, List
from .base_agent import BaseAgent, AgentResponse

class ReportGenerationAgent(BaseAgent):
    """报告生成智能体"""
    
    def __init__(self):
        super().__init__("report_generation_agent")
    
    async def execute(self, task_input: Dict[str, Any]) -> AgentResponse:
        try:
            market_analysis = task_input.get("market_analysis")
            trend_analysis = task_input.get("trend_analysis")
            category = task_input.get("category")
            
            if not all([market_analysis, trend_analysis, category]):
                return self.format_response(
                    False,
                    None,
                    "Missing required data: market_analysis, trend_analysis, category"
                )
            
            # 生成分析报告
            report = {
                "title": f"{category}类目商业分析报告",
                "summary": self._generate_summary(market_analysis, trend_analysis),
                "market_insights": self._generate_market_insights(market_analysis),
                "trend_insights": self._generate_trend_insights(trend_analysis),
                "recommendations": self._generate_recommendations(market_analysis, trend_analysis)
            }
            
            return self.format_response(True, report)
            
        except Exception as e:
            return self.format_response(False, None, str(e))
    
    def _generate_summary(self, market_analysis: Dict, trend_analysis: Dict) -> str:
        market_position = market_analysis["competitive_analysis"]["market_position"]
        market_trend = trend_analysis["growth_trend"]["trend_type"]
        market_maturity = trend_analysis["market_maturity"]
        
        return f"市场地位{market_position}，市场趋势{market_trend}，处于{market_maturity}阶段"
    
    def _generate_market_insights(self, market_analysis: Dict) -> List[str]:
        insights = []
        market_share = market_analysis["market_overview"]["market_share"]
        channel_dist = market_analysis["channel_analysis"]["channel_distribution"]
        
        insights.append(f"市场份额：{market_share:.2%}")
        insights.append(f"线上渗透率：{channel_dist['online']:.2%}")
        insights.append(f"线下占比：{channel_dist['offline']:.2%}")
        
        return insights
    
    def _generate_trend_insights(self, trend_analysis: Dict) -> List[str]:
        insights = []
        growth = trend_analysis["growth_trend"]["current_growth"]
        confidence = trend_analysis["future_projection"]["confidence"]
        
        insights.append(f"增长率：{growth:.2%}")
        insights.append(f"预测可信度：{confidence}")
        
        return insights
    
    def _generate_recommendations(self, market_analysis: Dict, trend_analysis: Dict) -> List[str]:
        recommendations = []
        
        # 根据市场位置给出建议
        if market_analysis["competitive_analysis"]["market_position"] == "Leader":
            recommendations.append("保持市场领先地位，关注新进入者")
        else:
            recommendations.append("加大市场投入，提升市场份额")
        
        # 根据渠道分布给出建议
        recommended_channel = market_analysis["channel_analysis"]["recommended_focus"]
        recommendations.append(f"建议重点发展{recommended_channel}渠道")
        
        # 根据市场成熟度给出建议
        if trend_analysis["market_maturity"] == "成长期":
            recommendations.append("把握市场快速增长机会，扩大规模")
        elif trend_analysis["market_maturity"] == "成熟期":
            recommendations.append("注重效率提升，维护现有市场")
        else:
            recommendations.append("谨慎投资，考虑转型机会")
        
        return recommendations
