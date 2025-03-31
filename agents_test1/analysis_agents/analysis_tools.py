"""分析工具模块，实现各种数据分析工具"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import json
import statistics

from core.base import Tool


class MarketTrendAnalysisTool(Tool):
    """市场趋势分析工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="market_trend_analysis_tool",
            tool_name="市场趋势分析工具",
            description="分析市场数据，识别市场趋势和变化"
        )
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行市场趋势分析
        
        参数:
            params: 包含以下字段的字典
                - market_data: 市场数据，通常是MarketDataTool的输出
                - metrics: 需要分析的指标列表，可选值包括sales, volume, market_share等
        
        返回:
            包含市场趋势分析结果的字典
        """
        market_data = params.get("market_data", {})
        metrics = params.get("metrics", ["sales", "volume", "market_share"])
        
        if not market_data or "data" not in market_data:
            return {"error": "Invalid market data format"}
        
        data_points = market_data["data"]
        if not data_points:
            return {"error": "Empty market data"}
        
        result = {
            "category": market_data.get("category", ""),
            "date_range": market_data.get("date_range", {}),
            "trends": {}
        }
        
        # 分析每个指标的趋势
        for metric in metrics:
            if metric not in data_points[0]:
                continue
                
            # 提取指标数据
            metric_values = [point[metric] for point in data_points if metric in point]
            if not metric_values:
                continue
                
            # 计算基本统计量
            avg_value = sum(metric_values) / len(metric_values)
            min_value = min(metric_values)
            max_value = max(metric_values)
            
            # 计算增长率
            first_value = metric_values[0]
            last_value = metric_values[-1]
            growth_rate = (last_value - first_value) / first_value if first_value != 0 else 0
            
            # 判断趋势方向
            if len(metric_values) >= 3:
                # 简单线性回归计算趋势
                n = len(metric_values)
                x = list(range(n))
                x_mean = sum(x) / n
                y_mean = sum(metric_values) / n
                
                numerator = sum((x[i] - x_mean) * (metric_values[i] - y_mean) for i in range(n))
                denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
                
                slope = numerator / denominator if denominator != 0 else 0
                
                if slope > 0.05 * avg_value:
                    trend_direction = "上升"
                elif slope < -0.05 * avg_value:
                    trend_direction = "下降"
                else:
                    trend_direction = "稳定"
            else:
                trend_direction = "数据点不足，无法判断趋势"
            
            # 计算波动性
            if len(metric_values) >= 2:
                variations = [abs(metric_values[i] - metric_values[i-1]) / metric_values[i-1] 
                             if metric_values[i-1] != 0 else 0 
                             for i in range(1, len(metric_values))]
                volatility = sum(variations) / len(variations) if variations else 0
            else:
                volatility = 0
            
            result["trends"][metric] = {
                "avg_value": round(avg_value, 2),
                "min_value": round(min_value, 2),
                "max_value": round(max_value, 2),
                "growth_rate": round(growth_rate, 4),
                "trend_direction": trend_direction,
                "volatility": round(volatility, 4)
            }
        
        # 生成总体趋势分析
        result["summary"] = self._generate_trend_summary(result["trends"])
        
        return result
    
    def _generate_trend_summary(self, trends: Dict[str, Any]) -> str:
        """生成趋势分析总结"""
        summary_parts = []
        
        for metric, trend in trends.items():
            if metric == "sales":
                metric_name = "销售额"
            elif metric == "volume":
                metric_name = "销量"
            elif metric == "market_share":
                metric_name = "市场份额"
            else:
                metric_name = metric
                
            direction = trend["trend_direction"]
            growth = trend["growth_rate"]
            
            if direction == "上升":
                summary_parts.append(f"{metric_name}呈上升趋势，增长率为{growth*100:.1f}%")
            elif direction == "下降":
                summary_parts.append(f"{metric_name}呈下降趋势，降低率为{abs(growth)*100:.1f}%")
            else:
                summary_parts.append(f"{metric_name}保持稳定，变化率为{growth*100:.1f}%")
        
        return "，".join(summary_parts) + "。"


class SellingPointAnalysisTool(Tool):
    """卖点分析工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="selling_point_analysis_tool",
            tool_name="卖点分析工具",
            description="分析卖点数据，识别有效卖点和趋势"
        )
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行卖点分析
        
        参数:
            params: 包含以下字段的字典
                - selling_point_data: 卖点数据，通常是SellingPointDataTool的输出
                - threshold: 有效卖点的阈值，默认为0.6
        
        返回:
            包含卖点分析结果的字典
        """
        selling_point_data = params.get("selling_point_data", {})
        threshold = params.get("threshold", 0.6)
        
        if not selling_point_data or "selling_points" not in selling_point_data:
            return {"error": "Invalid selling point data format"}
        
        selling_points = selling_point_data["selling_points"]
        if not selling_points:
            return {"error": "Empty selling point data"}
        
        result = {
            "category": selling_point_data.get("category", ""),
            "date_range": selling_point_data.get("date_range", {}),
            "effective_selling_points": [],
            "ineffective_selling_points": [],
            "trending_selling_points": []
        }
        
        # 分析每个卖点的有效性
        for point in selling_points:
            # 计算综合得分 (加权平均)
            score = (point.get("popularity_score", 0) * 0.4 + 
                     point.get("conversion_rate", 0) * 100 * 0.4 + 
                     point.get("avg_price_premium", 0) * 0.2)
            
            point_analysis = {
                "name": point.get("name", ""),
                "score": round(score, 2),
                "is_effective": score >= threshold,
                "is_trending": point.get("trend", "") == "上升",
                "competitor_usage": point.get("competitor_usage", 0),
                "recommendation": ""
            }
            
            # 生成推荐
            if score >= threshold:
                if point.get("trend", "") == "上升":
                    point_analysis["recommendation"] = "强烈推荐使用，市场反应良好且呈上升趋势"
                elif point.get("trend", "") == "稳定":
                    point_analysis["recommendation"] = "推荐使用，市场反应稳定"
                else:
                    point_analysis["recommendation"] = "可以使用，但需关注下降趋势的原因"
                    
                result["effective_selling_points"].append(point_analysis)
            else:
                if point.get("trend", "") == "上升":
                    point_analysis["recommendation"] = "可以尝试使用，虽然当前效果一般但有上升趋势"
                    result["trending_selling_points"].append(point_analysis)
                else:
                    point_analysis["recommendation"] = "不推荐使用，效果不佳"
                    
                result["ineffective_selling_points"].append(point_analysis)
        
        # 排序
        result["effective_selling_points"].sort(key=lambda x: x["score"], reverse=True)
        result["ineffective_selling_points"].sort(key=lambda x: x["score"], reverse=True)
        result["trending_selling_points"].sort(key=lambda x: x["score"], reverse=True)
        
        # 生成总体分析
        result["summary"] = self._generate_selling_point_summary(result)
        
        return result
    
    def _generate_selling_point_summary(self, analysis_result: Dict[str, Any]) -> str:
        """生成卖点分析总结"""
        effective_count = len(analysis_result["effective_selling_points"])
        trending_count = len(analysis_result["trending_selling_points"])
        total_count = effective_count + len(analysis_result["ineffective_selling_points"])
        
        if effective_count == 0:
            return "当前没有有效的卖点，建议开发新的卖点或改进现有卖点。"
        
        top_points = [point["name"] for point in analysis_result["effective_selling_points"][:3]]
        top_points_str = "、".join(top_points)
        
        summary = f"在分析的{total_count}个卖点中，有{effective_count}个卖点表现良好，其中表现最佳的卖点是{top_points_str}。"
        
        if trending_count > 0:
            trending_points = [point["name"] for point in analysis_result["trending_selling_points"][:2]]
            trending_points_str = "、".join(trending_points)
            summary += f"另有{trending_count}个卖点虽然当前效果一般，但呈上升趋势，值得关注，如{trending_points_str}。"
        
        return summary


class CompetitorAnalysisTool(Tool):
    """竞争对手分析工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="competitor_analysis_tool",
            tool_name="竞争对手分析工具",
            description="分析竞争对手数据，识别竞争态势和机会"
        )
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行竞争对手分析
        
        参数:
            params: 包含以下字段的字典
                - competitor_data: 竞争对手数据，通常是CompetitorDataTool的输出
                - market_data: 可选，市场数据，用于计算市场集中度
        
        返回:
            包含竞争对手分析结果的字典
        """
        competitor_data = params.get("competitor_data", {})
        market_data = params.get("market_data", {})
        
        if not competitor_data or "competitors" not in competitor_data:
            return {"error": "Invalid competitor data format"}
        
        competitors = competitor_data["competitors"]
        if not competitors:
            return {"error": "Empty competitor data"}
        
        result = {
            "category": competitor_data.get("category", ""),
            "date_range": competitor_data.get("date_range", {}),
            "competitor_analysis": [],
            "market_concentration": {},
            "competitive_landscape": "",
            "opportunities": [],
            "threats": []
        }
        
        # 分析每个竞争对手
        for competitor in competitors:
            comp_analysis = {
                "name": competitor.get("name", ""),
                "market_share": competitor.get("market_share", 0),
                "growth_rate": competitor.get("growth_rate", 0),
                "price_strategy": self._analyze_price_strategy(competitor.get("price_level", "中")),
                "strengths": competitor.get("strengths", []),
                "weaknesses": competitor.get("weaknesses", []),
                "threat_level": self._calculate_threat_level(competitor)
            }
            
            result["competitor_analysis"].append(comp_analysis)
            
            # 识别威胁
            if comp_analysis["threat_level"] == "高":
                result["threats"].append({
                    "competitor": comp_analysis["name"],
                    "description": f"市场份额{comp_analysis['market_share']*100:.1f}%，增长率{comp_analysis['growth_rate']*100:.1f}%，优势在于{', '.join(comp_analysis['strengths'])}"
                })
        
        # 排序竞争对手分析结果（按市场份额）
        result["competitor_analysis"].sort(key=lambda x: x["market_share"], reverse=True)
        
        # 计算市场集中度
        result["market_concentration"] = self._calculate_market_concentration(result["competitor_analysis"])
        
        # 分析竞争格局
        result["competitive_landscape"] = self._analyze_competitive_landscape(result["market_concentration"])
        
        # 识别机会
        result["opportunities"] = self._identify_opportunities(result["competitor_analysis"])
        
        # 生成总体分析
        result["summary"] = self._generate_competitor_summary(result)
        
        return result
    
    def _analyze_price_strategy(self, price_level: str) -> str:
        """分析价格策略"""
        if price_level == "高":
            return "高端定位，强调产品价值和品质"
        elif price_level == "中":
            return "中端定位，平衡价格和价值"
        else:
            return "低端定位，主打价格优势"
    
    def _calculate_threat_level(self, competitor: Dict[str, Any]) -> str:
        """计算威胁等级"""
        market_share = competitor.get("market_share", 0)
        growth_rate = competitor.get("growth_rate", 0)
        strengths_count = len(competitor.get("strengths", []))
        
        # 简单加权计算
        threat_score = market_share * 0.5 + growth_rate * 0.3 + strengths_count * 0.04
        
        if threat_score > 0.15:
            return "高"
        elif threat_score > 0.08:
            return "中"
        else:
            return "低"
    
    def _calculate_market_concentration(self, competitor_analysis: List[Dict[str, Any]]) -> Dict[str, Any]:
        """计算市场集中度"""
        # 计算CR4（前四大企业集中度）
        total_market_share = sum(comp["market_share"] for comp in competitor_analysis)
        
        cr4 = sum(comp["market_share"] for comp in competitor_analysis[:min(4, len(competitor_analysis))])
        cr4_ratio = cr4 / total_market_share if total_market_share > 0 else 0
        
        # 计算HHI（赫芬达尔-赫希曼指数）
        hhi = sum((comp["market_share"] * 100) ** 2 for comp in competitor_analysis)
        
        # 判断市场集中度
        if cr4_ratio > 0.7:
            concentration_level = "高度集中"
        elif cr4_ratio > 0.4:
            concentration_level = "中度集中"
        else:
            concentration_level = "分散"
        
        return {
            "cr4": round(cr4_ratio, 3),
            "hhi": round(hhi, 1),
            "concentration_level": concentration_level
        }
    
    def _analyze_competitive_landscape(self, market_concentration: Dict[str, Any]) -> str:
        """分析竞争格局"""
        concentration_level = market_concentration["concentration_level"]
        
        if concentration_level == "高度集中":
            return "市场呈寡头垄断格局，少数几家企业占据主导地位，进入壁垒高"
        elif concentration_level == "中度集中":
            return "市场竞争较为充分，有一定数量的主要竞争者，但市场份额分布不均"
        else:
            return "市场高度分散，竞争激烈，没有明显的市场领导者"
    
    def _identify_opportunities(self, competitor_analysis: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """识别市场机会"""
        opportunities = []
        
        # 收集所有竞争对手的弱点
        all_weaknesses = []
        for comp in competitor_analysis:
            all_weaknesses.extend(comp.get("weaknesses", []))
        
        # 统计弱点出现频率
        weakness_count = {}
        for weakness in all_weaknesses:
            weakness_count[weakness] = weakness_count.get(weakness, 0) + 1
        
        # 识别共同弱点作为机会
        for weakness, count in weakness_count.items():
            if count >= 2 or (count == 1 and len(competitor_analysis) <= 3):
                opportunities.append({
                    "area": weakness,
                    "description": f"多个竞争对手在{weakness}方面存在不足，可以将此作为差异化竞争点"
                })
        
        # 如果没有找到共同弱点，尝试从其他角度识别机会
        if not opportunities:
            # 检查是否有价格策略空白
            price_strategies = [comp.get("price_strategy", "") for comp in competitor_analysis]
            if "高端定位，强调产品价值和品质" not in price_strategies:
                opportunities.append({
                    "area": "高端市场",
                    "description": "当前竞争对手缺乏高端定位产品，可以考虑开发高端产品线"
                })
            if "低端定位，主打价格优势" not in price_strategies:
                opportunities.append({
                    "area": "低端市场",
                    "description": "当前竞争对手缺乏低价产品，可以考虑开发经济型产品线"
                })
        
        return opportunities
    
    def _generate_competitor_summary(self, analysis_result: Dict[str, Any]) -> str:
        """生成竞争对手分析总结"""
        competitor_count = len(analysis_result["competitor_analysis"])
        top_competitors = [comp["name"] for comp in analysis_result["competitor_analysis"][:2]]
        top_competitors_str = "和".join(top_competitors)
        
        concentration = analysis_result["market_concentration"]["concentration_level"]
        landscape = analysis_result["competitive_landscape"]
        
        summary = f"市场上有{competitor_count}个主要竞争对手，其中{top_competitors_str}占据主导地位。市场集中度{concentration}，{landscape}。"
        
        if analysis_result["opportunities"]:
            opp_areas = [opp["area"] for opp in analysis_result["opportunities"][:2]]
            opp_areas_str = "和".join(opp_areas)
            summary += f"主要市场机会在于{opp_areas_str}。"
        
        if analysis_result["threats"]:
            threat_comps = [threat["competitor"] for threat in analysis_result["threats"][:2]]
            threat_comps_str = "和".join(threat_comps)
            summary += f"需要警惕的主要竞争对手是{threat_comps_str}。"
        
        return summary


class PriceAnalysisTool(Tool):
    """价格分析工具"""
    
    def __init__(self):
        super().__init__(
            tool_id="price_analysis_tool",
            tool_name="价格分析工具",
            description="分析价格数据，识别价格敏感度和最优价格区间"
        )
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行价格分析
        
        参数:
            params: 包含以下字段的字典
                - price_data: 价格数据，通常是PriceDataTool的输出
                - market_data: 可选，市场数据，用于分析价格与销量的关系
        
        返回:
            包含价格分析结果的字典
        """
        price_data = params.get("price_data", {})
        market_data = params.get("market_data", {})
        
        if not price_data or "price_distribution" not in price_data:
            return {"error": "Invalid price data format"}
        
        price_distribution = price_data["price_distribution"]
        price_trend = price_data.get("price_trend", [])
        
        result = {
            "category": price_data.get("category", ""),
            "date_range": price_data.get("date_range", {}),
            "price_range": {
                "min": price_distribution.get("min_price", 0),
                "max": price_distribution.get("max_price", 0),
                "avg": price_distribution.get("avg_price", 0)
            },
            "price_segments_analysis": [],
            "optimal_price_range": {},
            "price_elasticity": {},
            "price_trend_analysis": {}
        }
        
        # 分析价格分布
        segments = price_distribution.get("price_segments", [])
        for segment in segments:
            price_range = segment.get("price_range", {})
            percentage = segment.get("percentage", 0)
            sales_percentage = segment.get("sales_volume_percentage", 0)
            
            # 计算价格效率（销量百分比/价格百分比的比值）
            price_efficiency = sales_percentage / percentage if percentage > 0 else 0
            
            segment_analysis = {
                "price_range": price_range,
                "percentage": percentage,
                "sales_volume_percentage": sales_percentage,
                "price_efficiency": round(price_efficiency, 2),
                "is_efficient": price_efficiency > 1.1
            }
            
            result["price_segments_analysis"].append(segment_analysis)
        
        # 识别最优价格区间
        if result["price_segments_analysis"]:
            # 按价格效率排序
            sorted_segments = sorted(result["price_segments_analysis"], 
                                     key=lambda x: x["price_efficiency"], 
                                     reverse=True)
            
            optimal_segment = sorted_segments[0]
            result["optimal_price_range"] = {
                "min": optimal_segment["price_range"].get("min", 0),
                "max": optimal_segment["price_range"].get("max", 0),
                "efficiency": optimal_segment["price_efficiency"],
                "sales_percentage": optimal_segment["sales_volume_percentage"]
            }
        
        # 分析价格趋势
        if price_trend:
            prices = [point.get("avg_price", 0) for point in price_trend]
            
            if len(prices) >= 2:
                # 计算价格变化率
                price_changes = [(prices[i] - prices[i-1]) / prices[i-1] 
                                if prices[i-1] > 0 else 0 
                                for i in range(1, len(prices))]
                
                avg_change = sum(price_changes) / len(price_changes) if price_changes else 0
                volatility = statistics.stdev(price_changes) if len(price_changes) > 1 else 0
                
                # 判断趋势方向
                if avg_change > 0.01:
                    trend_direction = "上升"
                elif avg_change < -0.01:
                    trend_direction = "下降"
                else:
                    trend_direction = "稳定"
                
                result["price_trend_analysis"] = {
                    "avg_change_rate": round(avg_change, 4),
                    "volatility": round(volatility, 4),
                    "trend_direction": trend_direction
                }
        
        # 估算价格弹性
        if market_data and "data" in market_data and len(market_data["data"]) > 1:
            # 这里是一个简化的价格弹性计算，实际应用中可能需要更复杂的模型
            market_data_points = market_data["data"]
            
            if "sales" in market_data_points[0] and price_trend:
                # 确保数据点数量一致
                min_points = min(len(market_data_points), len(price_trend))
                
                sales = [point.get("sales", 0) for point in market_data_points[:min_points]]
                prices = [point.get("avg_price", 0) for point in price_trend[:min_points]]
                
                if len(sales) > 1 and len(prices) > 1:
                    # 计算平均价格和销量
                    avg_price = sum(prices) / len(prices)
                    avg_sales = sum(sales) / len(sales)
                    
                    # 计算价格变化率和销量变化率
                    price_changes = [(prices[i] - prices[i-1]) / prices[i-1] 
                                    if prices[i-1] > 0 else 0 
                                    for i in range(1, len(prices))]
                    
                    sales_changes = [(sales[i] - sales[i-1]) / sales[i-1] 
                                    if sales[i-1] > 0 else 0 
                                    for i in range(1, len(sales))]
                    
                    # 计算价格弹性（销量变化率/价格变化率的平均值）
                    elasticities = []
                    for i in range(len(price_changes)):
                        if abs(price_changes[i]) > 0.001:  # 避免除以接近零的值
                            elasticities.append(-sales_changes[i] / price_changes[i])
                    
                    if elasticities:
                        avg_elasticity = sum(elasticities) / len(elasticities)
                        
                        # 判断价格敏感度