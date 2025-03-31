from typing import Dict, Any, List
import uuid
from datetime import datetime

# 导入智能体
from .agents import BaseAgent, CoordinatorAgent, ExpertAgent, UserInterfaceAgent

# 导入消息处理器
from .messaging import MessageHandler

# 导入工具
from .tools import DataCollectionTools, DataAnalysisTools, InsightGenerationTools

class BusinessAnalysisSystem:
    """
    商业数据分析多智能体系统
    整合协调智能体、专家智能体和用户交互智能体，实现完整的分析流程
    """
    def __init__(self):
        """
        初始化商业数据分析系统
        """
        # 创建消息处理器
        self.message_handler = MessageHandler()
        
        # 创建智能体
        self.coordinator = self._create_coordinator()
        self.user_interface = self._create_user_interface()
        self.expert_agents = self._create_expert_agents()
        
        # 注册智能体到消息处理器
        self.message_handler.register_agent(self.coordinator.agent_id, self.coordinator)
        self.message_handler.register_agent(self.user_interface.agent_id, self.user_interface)
        for agent in self.expert_agents:
            self.message_handler.register_agent(agent.agent_id, agent)
        
        # 设置用户界面智能体的协调者
        self.user_interface.set_coordinator(self.coordinator.agent_id)
        
        # 初始化工具
        self._initialize_tools()
    
    def _create_coordinator(self) -> CoordinatorAgent:
        """
        创建协调智能体
        
        Returns:
            协调智能体实例
        """
        coordinator_id = "coordinator_agent_1"
        return CoordinatorAgent(coordinator_id, "业务分析协调者")
    
    def _create_user_interface(self) -> UserInterfaceAgent:
        """
        创建用户交互智能体
        
        Returns:
            用户交互智能体实例
        """
        ui_agent_id = "ui_agent_1"
        return UserInterfaceAgent(ui_agent_id, "用户交互助手")
    
    def _create_expert_agents(self) -> List[ExpertAgent]:
        """
        创建专家智能体
        
        Returns:
            专家智能体列表
        """
        expert_agents = []
        
        # 市场数据专家
        market_expert = ExpertAgent(
            agent_id="market_expert_1",
            name="市场数据专家",
            expertise=["market_data", "competitor_data"]
        )
        expert_agents.append(market_expert)
        
        # 销售数据专家
        sales_expert = ExpertAgent(
            agent_id="sales_expert_1",
            name="销售数据专家",
            expertise=["sales_data", "product_data"]
        )
        expert_agents.append(sales_expert)
        
        # 市场分析专家
        market_analysis_expert = ExpertAgent(
            agent_id="market_analysis_expert_1",
            name="市场分析专家",
            expertise=["market_analysis", "competitor_analysis"]
        )
        expert_agents.append(market_analysis_expert)
        
        # 业务战略专家
        strategy_expert = ExpertAgent(
            agent_id="strategy_expert_1",
            name="业务战略专家",
            expertise=["business_strategy"]
        )
        expert_agents.append(strategy_expert)
        
        return expert_agents
    
    def _initialize_tools(self) -> None:
        """
        初始化并注册工具到专家智能体
        """
        # 创建工具实例
        data_collection_tools = DataCollectionTools()
        data_analysis_tools = DataAnalysisTools()
        insight_generation_tools = InsightGenerationTools()
        
        # 为市场数据专家注册工具
        market_expert = self._get_agent_by_id("market_expert_1")
        if market_expert:
            market_expert.register_tool("market_data", data_collection_tools.get_market_data)
            market_expert.register_tool("competitor_data", data_collection_tools.get_competitor_data)
        
        # 为销售数据专家注册工具
        sales_expert = self._get_agent_by_id("sales_expert_1")
        if sales_expert:
            sales_expert.register_tool("sales_data", data_collection_tools.get_sales_data)
            sales_expert.register_tool("product_data", data_collection_tools.get_product_data)
        
        # 为市场分析专家注册工具
        market_analysis_expert = self._get_agent_by_id("market_analysis_expert_1")
        if market_analysis_expert:
            market_analysis_expert.register_tool("trend_analysis_sales", data_analysis_tools.trend_analysis_sales)
            market_analysis_expert.register_tool("trend_analysis_market_share", data_analysis_tools.trend_analysis_market_share)
            market_analysis_expert.register_tool("trend_analysis_growth_rate", data_analysis_tools.trend_analysis_growth_rate)
            market_analysis_expert.register_tool("seasonality_analysis_sales", data_analysis_tools.seasonality_analysis_sales)
            market_analysis_expert.register_tool("comparative_analysis", data_analysis_tools.comparative_analysis)
            market_analysis_expert.register_tool("gap_analysis", data_analysis_tools.gap_analysis)
        
        # 为业务战略专家注册工具
        strategy_expert = self._get_agent_by_id("strategy_expert_1")
        if strategy_expert:
            strategy_expert.register_tool("trend_insights", insight_generation_tools.generate_trend_insights)
            strategy_expert.register_tool("opportunity_insights", insight_generation_tools.generate_opportunity_insights)
            strategy_expert.register_tool("risk_insights", insight_generation_tools.generate_risk_insights)
            strategy_expert.register_tool("competitive_advantage", insight_generation_tools.generate_competitive_advantage)
            strategy_expert.register_tool("threat_insights", insight_generation_tools.generate_threat_insights)
    
    def _get_agent_by_id(self, agent_id: str) -> BaseAgent:
        """
        根据ID获取智能体
        
        Args:
            agent_id: 智能体ID
            
        Returns:
            智能体实例，如果不存在则返回None
        """
        if agent_id == self.coordinator.agent_id:
            return self.coordinator
        elif agent_id == self.user_interface.agent_id:
            return self.user_interface
        else:
            for agent in self.expert_agents:
                if agent.agent_id == agent_id:
                    return agent
        return None
    
    def submit_analysis_request(self, user_id: str, analysis_request: Dict[str, Any]) -> str:
        """
        提交分析请求
        
        Args:
            user_id: 用户ID
            analysis_request: 分析请求详情
            
        Returns:
            请求ID
        """
        return self.user_interface.submit_analysis_request(user_id, analysis_request)
    
    def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """
        获取请求状态
        
        Args:
            request_id: 请求ID
            
        Returns:
            请求状态信息
        """
        return self.user_interface.get_request_status(request_id)
    
    def run_step(self) -> None:
        """
        运行系统一个步骤
        处理所有智能体的消息队列并执行智能体的行动
        """
        # 处理所有智能体的消息队列
        self.coordinator.process_messages()
        self.user_interface.process_messages()
        for agent in self.expert_agents:
            agent.process_messages()
        
        # 执行所有智能体的行动
        self.coordinator.act()
        self.user_interface.act()
        for agent in self.expert_agents:
            agent.act()
    
    def run(self, steps: int = 10) -> None:
        """
        运行系统指定步数
        
        Args:
            steps: 运行步数
        """
        for _ in range(steps):
            self.run_step()


# 示例使用代码
def example_usage():
    """
    示例：如何使用商业数据分析多智能体系统
    """
    # 创建系统实例
    system = BusinessAnalysisSystem()
    
    # 创建分析请求
    analysis_request = {
        'analysis_type': '市场趋势',
        'category': '智能手机',
        'time_range': {
            'start_date': '2023-01-01',
            'end_date': '2023-12-31'
        },
        'additional_parameters': {
            'focus_competitors': ['CompA', 'CompB', 'CompC'],
            'key_metrics': ['sales', 'market_share', 'growth_rate']
        }
    }
    
    # 提交分析请求
    user_id = "user_123"
    request_id = system.submit_analysis_request(user_id, analysis_request)
    print(f"已提交分析请求，请求ID: {request_id}")
    
    # 运行系统
    print("系统开始运行...")
    system.run(steps=20)  # 运行20个步骤
    
    # 获取请求状态
    status = system.get_request_status(request_id)
    print(f"请求状态: {status}")


if __name__ == "__main__":
    example_usage()