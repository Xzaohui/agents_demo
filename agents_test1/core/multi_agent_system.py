"""多智能体系统模块，实现多智能体协作的商业数据分析系统"""

from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import json
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor

from core.base import Agent, Message, AgentRegistry, ToolRegistry
from core.coordinator import Coordinator, TaskManager, Task
from data_agents.data_agents import (
    MarketDataAgent, 
    SellingPointDataAgent, 
    CompetitorDataAgent, 
    PriceDataAgent,
    ComprehensiveDataAgent
)
from analysis_agents.analysis_agents import (
    MarketTrendAnalysisAgent, 
    SellingPointAnalysisAgent, 
    CompetitorAnalysisAgent, 
    PriceAnalysisAgent,
    ComprehensiveAnalysisAgent
)


class MemoryModule:
    """记忆模块，用于存储和检索历史分析结果"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryModule, cls).__new__(cls)
            cls._instance.memory = {}
            cls._instance.index = {}
        return cls._instance
    
    def store(self, key: str, data: Any, metadata: Dict[str, Any] = None) -> None:
        """存储数据"""
        if metadata is None:
            metadata = {}
        
        timestamp = datetime.now().isoformat()
        entry = {
            "data": data,
            "metadata": metadata,
            "timestamp": timestamp
        }
        
        self.memory[key] = entry
        
        # 更新索引
        for k, v in metadata.items():
            if k not in self.index:
                self.index[k] = {}
            if v not in self.index[k]:
                self.index[k][v] = []
            if key not in self.index[k][v]:
                self.index[k][v].append(key)
    
    def retrieve(self, key: str) -> Optional[Any]:
        """检索数据"""
        entry = self.memory.get(key)
        return entry["data"] if entry else None
    
    def search(self, query: Dict[str, Any]) -> List[str]:
        """搜索符合条件的数据键"""
        results = set()
        first_key = True
        
        for k, v in query.items():
            if k in self.index and v in self.index[k]:
                if first_key:
                    results = set(self.index[k][v])
                    first_key = False
                else:
                    results &= set(self.index[k][v])
            else:
                return []
        
        return list(results)
    
    def get_recent(self, n: int = 10) -> List[Dict[str, Any]]:
        """获取最近的n条记录"""
        sorted_entries = sorted(
            [(k, v) for k, v in self.memory.items()],
            key=lambda x: x[1]["timestamp"],
            reverse=True
        )
        
        return [
            {"key": k, "data": v["data"], "metadata": v["metadata"], "timestamp": v["timestamp"]}
            for k, v in sorted_entries[:n]
        ]


class MessageBus:
    """消息总线，用于智能体之间的通信"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageBus, cls).__new__(cls)
            cls._instance.subscribers = {}
            cls._instance.message_queue = asyncio.Queue()
            cls._instance.running = False
        return cls._instance
    
    def subscribe(self, agent_id: str, agent: Agent) -> None:
        """订阅消息"""
        self.subscribers[agent_id] = agent
    
    def unsubscribe(self, agent_id: str) -> None:
        """取消订阅"""
        if agent_id in self.subscribers:
            del self.subscribers[agent_id]
    
    async def publish(self, message: Message) -> None:
        """发布消息"""
        await self.message_queue.put(message)
    
    async def start(self) -> None:
        """启动消息总线"""
        self.running = True
        while self.running:
            try:
                message = await self.message_queue.get()
                await self._deliver_message(message)
                self.message_queue.task_done()
            except Exception as e:
                print(f"Error in message bus: {str(e)}")
    
    async def stop(self) -> None:
        """停止消息总线"""
        self.running = False
    
    async def _deliver_message(self, message: Message) -> None:
        """投递消息"""
        if message.receiver == "broadcast":
            # 广播消息
            for agent_id, agent in self.subscribers.items():
                if agent_id != message.sender:
                    agent.receive_message(message)
        elif message.receiver in self.subscribers:
            # 单播消息
            self.subscribers[message.receiver].receive_message(message)


class MultiAgentSystem:
    """多智能体系统，整合各种智能体和组件"""
    
    def __init__(self):
        # 初始化组件
        self.agent_registry = AgentRegistry()
        self.tool_registry = ToolRegistry()
        self.memory = MemoryModule()
        self.message_bus = MessageBus()
        self.coordinator = Coordinator()
        self.task_manager = TaskManager()
        
        # 初始化线程池
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # 初始化事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # 初始化智能体
        self._init_agents()
        
        # 注册协调器回调
        self._register_coordinator_callbacks()
    
    def _init_agents(self) -> None:
        """初始化所有智能体"""
        # 数据智能体
        market_data_agent = MarketDataAgent()
        selling_point_data_agent = SellingPointDataAgent()
        competitor_data_agent = CompetitorDataAgent()
        price_data_agent = PriceDataAgent()
        comprehensive_data_agent = ComprehensiveDataAgent()
        
        # 分析智能体
        market_trend_analysis_agent = MarketTrendAnalysisAgent()
        selling_point_analysis_agent = SellingPointAnalysisAgent()
        competitor_analysis_agent = CompetitorAnalysisAgent()
        price_analysis_agent = PriceAnalysisAgent()
        comprehensive_analysis_agent = ComprehensiveAnalysisAgent()
        
        # 注册智能体
        self.agent_registry.register(market_data_agent)
        self.agent_registry.register(selling_point_data_agent)
        self.agent_registry.register(competitor_data_agent)
        self.agent_registry.register(price_data_agent)
        self.agent_registry.register(comprehensive_data_agent)
        
        self.agent_registry.register(market_trend_analysis_agent)
        self.agent_registry.register(selling_point_analysis_agent)
        self.agent_registry.register(competitor_analysis_agent)
        self.agent_registry.register(price_analysis_agent)
        self.agent_registry.register(comprehensive_analysis_agent)
        
        self.agent_registry.register(self.coordinator)
        
        # 订阅消息总线
        self.message_bus.subscribe(market_data_agent.agent_id, market_data_agent)
        self.message_bus.subscribe(selling_point_data_agent.agent_id, selling_point_data_agent)
        self.message_bus.subscribe(competitor_data_agent.agent_id, competitor_data_agent)
        self.message_bus.subscribe(price_data_agent.agent_id, price_data_agent)
        self.message_bus.subscribe(comprehensive_data_agent.agent_id, comprehensive_data_agent)
        
        self.message_bus.subscribe(market_trend_analysis_agent.agent_id, market_trend_analysis_agent)
        self.message_bus.subscribe(selling_point_analysis_agent.agent_id, selling_point_analysis_agent)
        self.message_bus.subscribe(competitor_analysis_agent.agent_id, competitor_analysis_agent)
        self.message_bus.subscribe(price_analysis_agent.agent_id, price_analysis_agent)
        self.message_bus.subscribe(comprehensive_analysis_agent.agent_id, comprehensive_analysis_agent)
        
        self.message_bus.subscribe(self.coordinator.agent_id, self.coordinator)
    
    def _register_coordinator_callbacks(self) -> None:
        """注册协调器回调函数"""
        # 这里可以注册各种回调函数，处理不同类型的消息
        pass
    
    async def start(self) -> None:
        """启动多智能体系统"""
        # 启动消息总线
        self.loop.create_task(self.message_bus.start())
    
    async def stop(self) -> None:
        """停止多智能体系统"""
        # 停止消息总线
        await self.message_bus.stop()
        # 关闭线程池
        self.executor.shutdown()
    
    async def submit_task(self, task_type: str, params: Dict[str, Any], priority: int = 1) -> str:
        """提交任务"""
        # 创建任务请求消息
        message = Message(
            sender="user",
            receiver="coordinator",
            content={
                "task_type": task_type,
                "params": params,
                "priority": priority
            },
            msg_type="task_request"
        )
        
        # 发布消息
        await self.message_bus.publish(message)
        
        # 返回任务ID（这里简化处理，实际应该等待协调器的响应）
        return str(uuid.uuid4())
    
    async def get_task_result(self, task_id: str, timeout: int = 60) -> Optional[Dict[str, Any]]:
        """获取任务结果"""
        # 这里简化处理，实际应该实现等待任务完成的逻辑
        # 可以使用异步等待、回调或轮询等方式
        task = self.task_manager.task_registry.get_task(task_id)
        if not task:
            return None
        
        if task.status == "completed":
            return task.result
        
        # 等待任务完成
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            await asyncio.sleep(1)
            task = self.task_manager.task_registry.get_task(task_id)
            if task and task.status == "completed":
                return task.result
        
        return {"error": "Task timeout"}
    
    def run_analysis(self, analysis_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """运行分析任务（同步接口）"""
        # 将异步接口包装为同步接口
        async def _run():
            task_id = await self.submit_task(analysis_type, params)
            return await self.get_task_result(task_id)
        
        return self.loop.run_until_complete(_run())


class AnalysisWorkflow:
    """分析工作流，定义常见的分析流程"""
    
    def __init__(self, system: MultiAgentSystem):
        self.system = system
    
    def market_overview_analysis(self, category: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """市场概览分析"""
        params = {
            "category": category,
            "start_date": start_date,
            "end_date": end_date
        }
        
        return self.system.run_analysis("comprehensive_analysis", params)
    
    def competitor_landscape_analysis(self, category: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """竞争格局分析"""
        params = {
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "focus": "competitor"
        }
        
        return self.system.run_analysis("competitor_analysis", params)
    
    def pricing_strategy_analysis(self, category: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """定价策略分析"""
        params = {
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "focus": "price"
        }
        
        return self.system.run_analysis("price_analysis", params)
    
    def selling_point_effectiveness_analysis(self, category: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """卖点效果分析"""
        params = {
            "category": category,
            "start_date": start_date,
            "end_date": end_date,
            "focus": "selling_point"
        }
        
        return self.system.run_analysis("selling_point_analysis", params)
    
    def custom_analysis(self, analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """自定义分析"""
        # 支持用户自定义分析流程
        if "task_type" not in analysis_config or "params" not in analysis_config:
            return {"error": "Invalid analysis configuration"}
        
        return self.system.run_analysis(analysis_config["task_type"], analysis_config["params"])


# 示例使用方法
def main():
    # 初始化多智能体系统
    system = MultiAgentSystem()
    
    # 创建分析工作流
    workflow = AnalysisWorkflow(system)
    
    # 运行市场概览分析
    result = workflow.market_overview_analysis(
        category="手机",
        start_date="2023-01-01",
        end_date="2023-12-31"
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()