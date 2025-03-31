from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..models.message import Message

class CoordinatorAgent(BaseAgent):
    """
    协调智能体，负责任务分解、分配和监控
    """
    def __init__(self, agent_id: str, name: str):
        """
        初始化协调智能体
        
        Args:
            agent_id: 智能体唯一标识符
            name: 智能体名称
        """
        super().__init__(agent_id, name)
        self.available_agents: Dict[str, Dict[str, Any]] = {}  # 可用智能体信息
        self.active_tasks: Dict[str, Dict[str, Any]] = {}  # 活跃任务信息
        self.task_results: Dict[str, Dict[str, Any]] = {}  # 任务结果
        self.current_analysis_id: Optional[str] = None  # 当前分析ID
    
    def register_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> None:
        """
        注册智能体到协调器
        
        Args:
            agent_id: 智能体ID
            agent_info: 智能体信息，包括类型、专业领域等
        """
        self.available_agents[agent_id] = agent_info
    
    def process_message(self, message: Message) -> None:
        """
        处理接收到的消息
        
        Args:
            message: 接收到的消息
        """
        if message.message_type == 'analysis_request':
            # 接收到分析请求，开始新的分析流程
            self._start_analysis_workflow(message)
        elif message.message_type == 'task_result':
            # 接收到任务结果
            self._process_task_result(message)
        elif message.message_type == 'agent_registration':
            # 接收到智能体注册请求
            self.register_agent(message.from_agent_id, message.content)
            # 发送确认消息
            self.send_message(
                to_agent_id=message.from_agent_id,
                content={'status': 'registered'},
                message_type='registration_confirmation',
                reference_id=message.message_id
            )
    
    def act(self) -> None:
        """
        协调智能体的主要行动逻辑
        """
        # 检查是否有完成的分析流程
        if self.current_analysis_id and self._is_analysis_complete(self.current_analysis_id):
            self._finalize_analysis(self.current_analysis_id)
    
    def _start_analysis_workflow(self, message: Message) -> None:
        """
        启动分析工作流程
        
        Args:
            message: 包含分析请求的消息
        """
        analysis_id = message.message_id
        self.current_analysis_id = analysis_id
        
        # 存储分析请求信息
        self.update_memory(f'analysis_{analysis_id}', {
            'request': message.content,
            'requester_id': message.from_agent_id,
            'status': 'in_progress',
            'tasks': []
        })
        
        # 分解任务
        tasks = self._decompose_analysis_task(message.content)
        
        # 更新分析信息中的任务列表
        analysis_info = self.get_memory(f'analysis_{analysis_id}')
        analysis_info['tasks'] = [task['task_id'] for task in tasks]
        self.update_memory(f'analysis_{analysis_id}', analysis_info)
        
        # 分配任务给适当的智能体
        for task in tasks:
            self._assign_task(task, analysis_id)
    
    def _decompose_analysis_task(self, analysis_request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        将分析请求分解为子任务
        
        Args:
            analysis_request: 分析请求的详细信息
            
        Returns:
            分解后的任务列表
        """
        tasks = []
        analysis_type = analysis_request.get('analysis_type')
        category = analysis_request.get('category')
        time_range = analysis_request.get('time_range')
        
        # 根据分析类型创建不同的任务序列
        if analysis_type == '市场趋势':
            # 1. 数据收集任务
            tasks.append({
                'task_id': f'data_collection_{len(tasks) + 1}',
                'task_type': 'data_collection',
                'parameters': {
                    'category': category,
                    'time_range': time_range,
                    'data_types': ['market_data', 'sales_data']
                },
                'required_expertise': 'market_data'
            })
            
            # 2. 数据分析任务
            tasks.append({
                'task_id': f'data_analysis_{len(tasks) + 1}',
                'task_type': 'data_analysis',
                'parameters': {
                    'analysis_methods': ['trend_analysis', 'seasonality_analysis'],
                    'dimensions': ['sales', 'market_share', 'growth_rate']
                },
                'depends_on': ['data_collection_1'],
                'required_expertise': 'market_analysis'
            })
            
            # 3. 洞察生成任务
            tasks.append({
                'task_id': f'insight_generation_{len(tasks) + 1}',
                'task_type': 'insight_generation',
                'parameters': {
                    'insight_types': ['trend_insights', 'opportunity_insights', 'risk_insights'],
                    'max_insights': 5
                },
                'depends_on': ['data_analysis_2'],
                'required_expertise': 'business_strategy'
            })
        
        elif analysis_type == '竞品分析':
            # 1. 竞品数据收集
            tasks.append({
                'task_id': f'data_collection_{len(tasks) + 1}',
                'task_type': 'data_collection',
                'parameters': {
                    'category': category,
                    'time_range': time_range,
                    'data_types': ['competitor_data', 'product_data']
                },
                'required_expertise': 'competitor_data'
            })
            
            # 2. 竞品对比分析
            tasks.append({
                'task_id': f'data_analysis_{len(tasks) + 1}',
                'task_type': 'data_analysis',
                'parameters': {
                    'analysis_methods': ['comparative_analysis', 'gap_analysis'],
                    'dimensions': ['price', 'features', 'market_position']
                },
                'depends_on': ['data_collection_1'],
                'required_expertise': 'competitor_analysis'
            })
            
            # 3. 竞争策略洞察
            tasks.append({
                'task_id': f'insight_generation_{len(tasks) + 1}',
                'task_type': 'insight_generation',
                'parameters': {
                    'insight_types': ['competitive_advantage', 'threat_insights', 'opportunity_insights'],
                    'max_insights': 5
                },
                'depends_on': ['data_analysis_2'],
                'required_expertise': 'business_strategy'
            })
        
        # 可以根据需要添加更多分析类型的任务分解
        
        return tasks
    
    def _assign_task(self, task: Dict[str, Any], analysis_id: str) -> None:
        """
        将任务分配给合适的智能体
        
        Args:
            task: 任务信息字典
            analysis_id: 分析ID
        """
        # 检查任务依赖是否满足
        if 'depends_on' in task and not self._check_dependencies(task['depends_on'], analysis_id):
            # 如果依赖未满足，将任务加入等待队列
            self.active_tasks[task['task_id']] = {
                'task': task,
                'status': 'waiting',
                'analysis_id': analysis_id
            }
            return

        # 根据required_expertise查找合适的智能体
        suitable_agent = self._find_suitable_agent(task['required_expertise'])
        if not suitable_agent:
            # 如果没有找到合适的智能体，将任务标记为失败
            self.active_tasks[task['task_id']] = {
                'task': task,
                'status': 'failed',
                'analysis_id': analysis_id,
                'error': 'No suitable agent found'
            }
            return

        # 更新活跃任务状态
        self.active_tasks[task['task_id']] = {
            'task': task,
            'status': 'assigned',
            'analysis_id': analysis_id,
            'assigned_agent': suitable_agent
        }

        # 发送任务分配消息给选中的智能体
        self.send_message(
            to_agent_id=suitable_agent,
            content={
                'task': task,
                'analysis_id': analysis_id
            },
            message_type='task_assignment',
            reference_id=task['task_id']
        )

    def _check_dependencies(self, dependencies: List[str], analysis_id: str) -> bool:
        """
        检查任务依赖是否都已完成
        
        Args:
            dependencies: 依赖任务ID列表
            analysis_id: 分析ID
            
        Returns:
            所有依赖是否都已完成
        """
        for dep_task_id in dependencies:
            if dep_task_id not in self.task_results or \
               self.task_results[dep_task_id].get('status') != 'completed':
                return False
        return True

    def _find_suitable_agent(self, required_expertise: str) -> Optional[str]:
        """
        根据所需专业领域查找合适的智能体
        
        Args:
            required_expertise: 所需专业领域
            
        Returns:
            合适的智能体ID，如果没有找到则返回None
        """
        for agent_id, agent_info in self.available_agents.items():
            if agent_info.get('expertise') == required_expertise and \
               agent_info.get('status', 'available') == 'available':
                return agent_id
        return None