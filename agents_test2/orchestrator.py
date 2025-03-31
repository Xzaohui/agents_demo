from typing import Dict, Any, List
from agents.data_collection_agent import MarketDataCollector, SalesPointCollector
from agents.analysis_agent import MarketAnalysisAgent, TrendAnalysisAgent
from agents.report_agent import ReportGenerationAgent

class AnalysisOrchestrator:
    """分析任务编排器"""
    
    def __init__(self):
        # 初始化所有智能体
        self.market_data_collector = MarketDataCollector()
        self.sales_point_collector = SalesPointCollector()
        self.market_analysis_agent = MarketAnalysisAgent()
        self.trend_analysis_agent = TrendAnalysisAgent()
        self.report_agent = ReportGenerationAgent()
    
    async def run_analysis(self, category: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """运行完整的分析流程"""
        try:
            # 1. 收集市场数据
            market_data_response = await self.market_data_collector.execute({
                "category": category,
                "start_date": start_date,
                "end_date": end_date
            })
            
            if not market_data_response.success:
                return {"success": False, "message": f"Market data collection failed: {market_data_response.message}"}
            
            # 2. 收集销售数据
            sales_data_response = await self.sales_point_collector.execute({
                "category": category,
                "date": end_date  # 使用结束日期作为销售数据的查询日期
            })
            
            if not sales_data_response.success:
                return {"success": False, "message": f"Sales data collection failed: {sales_data_response.message}"}
            
            # 3. 执行市场分析
            market_analysis_response = await self.market_analysis_agent.execute({
                "market_data": market_data_response.data,
                "sales_data": sales_data_response.data
            })
            
            if not market_analysis_response.success:
                return {"success": False, "message": f"Market analysis failed: {market_analysis_response.message}"}
            
            # 4. 执行趋势分析
            trend_analysis_response = await self.trend_analysis_agent.execute({
                "market_data": market_data_response.data,
                "historical_data": []  # 这里可以添加历史数据
            })
            
            if not trend_analysis_response.success:
                return {"success": False, "message": f"Trend analysis failed: {trend_analysis_response.message}"}
            
            # 5. 生成分析报告
            report_response = await self.report_agent.execute({
                "category": category,
                "market_analysis": market_analysis_response.data,
                "trend_analysis": trend_analysis_response.data
            })
            
            if not report_response.success:
                return {"success": False, "message": f"Report generation failed: {report_response.message}"}
            
            # 6. 返回完整结果
            return {
                "success": True,
                "data": {
                    "raw_data": {
                        "market_data": market_data_response.data,
                        "sales_data": sales_data_response.data
                    },
                    "analysis": {
                        "market_analysis": market_analysis_response.data,
                        "trend_analysis": trend_analysis_response.data
                    },
                    "report": report_response.data
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Analysis pipeline failed: {str(e)}"}
