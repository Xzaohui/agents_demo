from typing import Dict, Any, List, Optional
import random
from datetime import datetime, timedelta

class DataCollectionTools:
    """
    数据收集工具类，提供各种数据收集功能
    """
    def __init__(self):
        """
        初始化数据收集工具
        """
        # 在实际实现中，这里可能会包含API客户端、数据库连接等
        pass
    
    def get_market_data(self, category: str, time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        获取市场数据
        
        Args:
            category: 类目名称
            time_range: 时间范围，包含start_date和end_date
            
        Returns:
            市场数据
        """
        # 在实际实现中，这里会调用相应的API或查询数据库
        # 目前返回模拟数据
        start_date = datetime.fromisoformat(time_range['start_date'])
        end_date = datetime.fromisoformat(time_range['end_date'])
        
        # 生成时间序列数据
        time_series_data = self._generate_time_series_data(start_date, end_date)
        
        return {
            'category': category,
            'time_range': time_range,
            'market_size': random.randint(1000000, 10000000),
            'growth_rate': round(random.uniform(0.01, 0.2), 3),
            'market_share': {
                'leader': round(random.uniform(0.2, 0.4), 2),
                'second': round(random.uniform(0.1, 0.2), 2),
                'third': round(random.uniform(0.05, 0.1), 2),
                'others': round(random.uniform(0.3, 0.5), 2)
            },
            'trends': {
                'overall_trend': random.choice(['上升', '下降', '稳定']),
                'seasonal_factors': random.choice(['Q4高峰', 'Q2低谷', '无明显季节性']),
                'time_series': time_series_data
            },
            'key_players': [
                {'name': 'Company A', 'market_share': round(random.uniform(0.2, 0.4), 2)},
                {'name': 'Company B', 'market_share': round(random.uniform(0.1, 0.2), 2)},
                {'name': 'Company C', 'market_share': round(random.uniform(0.05, 0.1), 2)}
            ]
        }
    
    def get_sales_data(self, category: str, time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        获取销售数据
        
        Args:
            category: 类目名称
            time_range: 时间范围，包含start_date和end_date
            
        Returns:
            销售数据
        """
        # 在实际实现中，这里会调用相应的API或查询数据库
        # 目前返回模拟数据
        start_date = datetime.fromisoformat(time_range['start_date'])
        end_date = datetime.fromisoformat(time_range['end_date'])
        
        # 生成时间序列数据
        time_series_data = self._generate_time_series_data(start_date, end_date)
        
        return {
            'category': category,
            'time_range': time_range,
            'total_sales': random.randint(100000, 1000000),
            'sales_growth': round(random.uniform(-0.05, 0.15), 3),
            'product_categories': {
                'CategoryA': random.randint(30000, 300000),
                'CategoryB': random.randint(40000, 400000),
                'CategoryC': random.randint(20000, 200000)
            },
            'sales_channels': {
                'online': round(random.uniform(0.4, 0.7), 2),
                'offline': round(random.uniform(0.3, 0.6), 2)
            },
            'time_series': time_series_data,
            'top_products': [
                {'name': 'Product X', 'sales': random.randint(10000, 100000)},
                {'name': 'Product Y', 'sales': random.randint(8000, 80000)},
                {'name': 'Product Z', 'sales': random.randint(5000, 50000)}
            ]
        }
    
    def get_competitor_data(self, category: str, time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        获取竞品数据
        
        Args:
            category: 类目名称
            time_range: 时间范围，包含start_date和end_date
            
        Returns:
            竞品数据
        """
        # 在实际实现中，这里会调用相应的API或查询数据库
        # 目前返回模拟数据
        competitors = [
            {
                'name': 'Competitor A',
                'market_share': round(random.uniform(0.2, 0.4), 2),
                'growth_rate': round(random.uniform(0.02, 0.15), 3),
                'strengths': ['品牌知名度高', '产品线丰富', '渠道覆盖广'],
                'weaknesses': ['价格较高', '创新速度慢'],
                'key_products': ['ProductA1', 'ProductA2', 'ProductA3'],
                'price_positioning': random.choice(['高端', '中高端', '中端'])
            },
            {
                'name': 'Competitor B',
                'market_share': round(random.uniform(0.1, 0.2), 2),
                'growth_rate': round(random.uniform(0.05, 0.25), 3),
                'strengths': ['技术领先', '创新能力强', '目标客户精准'],
                'weaknesses': ['规模较小', '品牌认知度不足'],
                'key_products': ['ProductB1', 'ProductB2'],
                'price_positioning': random.choice(['中高端', '中端', '中低端'])
            },
            {
                'name': 'Competitor C',
                'market_share': round(random.uniform(0.05, 0.15), 2),
                'growth_rate': round(random.uniform(-0.05, 0.1), 3),
                'strengths': ['价格优势', '渠道下沉能力强'],
                'weaknesses': ['产品质量一般', '服务体验较差'],
                'key_products': ['ProductC1', 'ProductC2', 'ProductC3', 'ProductC4'],
                'price_positioning': random.choice(['中低端', '低端'])
            }
        ]
        
        return {
            'category': category,
            'time_range': time_range,
            'competitors': competitors,
            'market_concentration': round(random.uniform(0.3, 0.8), 2),  # 市场集中度
            'competitive_intensity': random.choice(['高', '中', '低']),  # 竞争激烈程度
            'entry_barriers': random.choice(['高', '中', '低']),  # 进入壁垒
            'recent_market_changes': [
                '新进入者增加',
                '价格竞争加剧',
                '产品同质化严重',
                '渠道整合趋势明显'
            ]
        }
    
    def get_product_data(self, category: str, time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        获取产品数据
        
        Args:
            category: 类目名称
            time_range: 时间范围，包含start_date和end_date
            
        Returns:
            产品数据
        """
        # 在实际实现中，这里会调用相应的API或查询数据库
        # 目前返回模拟数据
        products = [
            {
                'name': 'Product X',
                'sales_volume': random.randint(10000, 100000),
                'price_range': f"{random.randint(100, 500)}-{random.randint(500, 1000)}",
                'rating': round(random.uniform(3.5, 5.0), 1),
                'features': ['Feature X1', 'Feature X2', 'Feature X3'],
                'target_audience': ['年轻人', '学生', '专业人士'],
                'launch_date': (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
            },
            {
                'name': 'Product Y',
                'sales_volume': random.randint(8000, 80000),
                'price_range': f"{random.randint(80, 300)}-{random.randint(300, 800)}",
                'rating': round(random.uniform(3.0, 4.8), 1),
                'features': ['Feature Y1', 'Feature Y2', 'Feature Y3', 'Feature Y4'],
                'target_audience': ['家庭用户', '中年人群'],
                'launch_date': (datetime.now() - timedelta(days=random.randint(60, 730))).isoformat()
            },
            {
                'name': 'Product Z',
                'sales_volume': random.randint(5000, 50000),
                'price_range': f"{random.randint(50, 200)}-{random.randint(200, 500)}",
                'rating': round(random.uniform(2.8, 4.5), 1),
                'features': ['Feature Z1', 'Feature Z2'],
                'target_audience': ['价格敏感人群', '入门用户'],
                'launch_date': (datetime.now() - timedelta(days=random.randint(90, 1095))).isoformat()
            }
        ]
        
        return {
            'category': category,
            'time_range': time_range,
            'products': products,
            'price_distribution': {
                'low_end': round(random.uniform(0.2, 0.4), 2),
                'mid_range': round(random.uniform(0.3, 0.5), 2),
                'high_end': round(random.uniform(0.1, 0.3), 2)
            },
            'feature_importance': [
                {'feature': 'Feature 1', 'importance': round(random.uniform(0.1, 0.3), 2)},
                {'feature': 'Feature 2', 'importance': round(random.uniform(0.2, 0.4), 2)},
                {'feature': 'Feature 3', 'importance': round(random.uniform(0.15, 0.35), 2)},
                {'feature': 'Feature 4', 'importance': round(random.uniform(0.1, 0.25), 2)}
            ],
            'customer_satisfaction': {
                'overall': round(random.uniform(3.5, 4.5), 1),
                'by_aspect': {
                    'quality': round(random.uniform(3.0, 4.8), 1),
                    'price': round(random.uniform(2.8, 4.2), 1),
                    'service': round(random.uniform(3.2, 4.5), 1),
                    'user_experience': round(random.uniform(3.3, 4.7), 1)
                }
            }
        }
    
    def _generate_time_series_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        生成时间序列数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            时间序列数据
        """
        time_series = []
        current_date = start_date
        base_value = random.randint(1000, 10000)
        trend = random.uniform(-0.01, 0.03)  # 每天的趋势变化
        
        while current_date <= end_date:
            # 添加一些随机波动和季节性
            seasonal_factor = 1.0 + 0.1 * math.sin(2 * math.pi * current_date.timetuple().tm_yday / 365)
            random_factor = random.uniform(0.9, 1.1)
            
            value = base_value * (1 + trend) ** (current_date - start_date).days * seasonal_factor * random_factor
            
            time_series.append({
                'date': current_date.isoformat(),
                'value': round(value, 2)
            })
            
            current_date += timedelta(days=1)
            base_value = value  # 使用上一个值作为新的基准
        
        return time_series

# 导入math模块，用于数学计算
import math