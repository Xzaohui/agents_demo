from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..models.message import Message

class ExpertAgent(BaseAgent):
    """
    专家智能体，负责执行特定领域的分析任务
    """
    def __init__(self, agent_id: str, name: str, expertise: List[str]):
        """
        初始化专家智能体
        
        Args:
            agent_id: 智能体唯一标识符
            name: 智能体名称
            expertise: 专业领域列表
        """
        super().__init__(agent_id, name)
        self.expertise = expertise
        self.current_tasks: Dict[str, Dict[str, Any]] = {}  # 当前正在处理的任务
        self.tools_registry: Dict[str, Any] = {}  # 可用工具注册表
    
    def register_tool(self, tool_name: str, tool_function) -> None:
        """
        注册工具到专家智能体
        
        Args:
            tool_name: 工具名称
            tool_function: 工具函数
        """
        self.tools_registry[tool_name] = tool_function
    
    def process_message(self, message: Message) -> None:
        """
        处理接收到的消息
        
        Args:
            message: 接收到的消息
        """
        if message.message_type == 'task_assignment':
            # 接收到任务分配
            self._handle_task_assignment(message)
        elif message.message_type == 'task_status_inquiry':
            # 接收到任务状态查询
            self._handle_task_status_inquiry(message)
    
    def act(self) -> None:
        """
        专家智能体的主要行动逻辑
        """
        # 处理所有当前任务
        task_ids = list(self.current_tasks.keys())
        for task_id in task_ids:
            task_info = self.current_tasks[task_id]
            if task_info['status'] == 'assigned':
                self._execute_task(task_id)
    
    def _handle_task_assignment(self, message: Message) -> None:
        """
        处理任务分配消息
        
        Args:
            message: 任务分配消息
        """
        content = message.content
        task = content.get('task')
        analysis_id = content.get('analysis_id')
        
        if not task or not analysis_id:
            print(f"Error: Invalid task assignment message: {message.message_id}")
            return
        
        task_id = task['task_id']
        
        # 存储任务信息
        self.current_tasks[task_id] = {
            'task': task,
            'analysis_id': analysis_id,
            'status': 'assigned',
            'assigned_time': message.timestamp
        }
        
        # 发送确认消息
        self.send_message(
            to_agent_id=message.from_agent_id,
            content={
                'task_id': task_id,
                'status': 'accepted'
            },
            message_type='task_acceptance',
            reference_id=message.message_id
        )
    
    def _handle_task_status_inquiry(self, message: Message) -> None:
        """
        处理任务状态查询消息
        
        Args:
            message: 任务状态查询消息
        """
        content = message.content
        task_id = content.get('task_id')
        
        if not task_id or task_id not in self.current_tasks:
            # 任务不存在
            self.send_message(
                to_agent_id=message.from_agent_id,
                content={
                    'task_id': task_id,
                    'status': 'unknown'
                },
                message_type='task_status_response',
                reference_id=message.message_id
            )
            return
        
        # 发送任务状态
        self.send_message(
            to_agent_id=message.from_agent_id,
            content={
                'task_id': task_id,
                'status': self.current_tasks[task_id]['status']
            },
            message_type='task_status_response',
            reference_id=message.message_id
        )
    
    def _execute_task(self, task_id: str) -> None:
        """
        执行任务
        
        Args:
            task_id: 任务ID
        """
        task_info = self.current_tasks[task_id]
        task = task_info['task']
        analysis_id = task_info['analysis_id']
        
        # 更新任务状态
        task_info['status'] = 'in_progress'
        self.current_tasks[task_id] = task_info
        
        try:
            # 根据任务类型执行不同的操作
            task_type = task['task_type']
            parameters = task['parameters']
            
            result = None
            if task_type == 'data_collection':
                result = self._collect_data(parameters)
            elif task_type == 'data_analysis':
                result = self._analyze_data(parameters)
            elif task_type == 'insight_generation':
                result = self._generate_insights(parameters)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            # 更新任务状态为已完成
            task_info['status'] = 'completed'
            task_info['result'] = result
            task_info['completion_time'] = datetime.now()
            self.current_tasks[task_id] = task_info
            
            # 发送任务结果
            self._send_task_result(task_id, analysis_id, result)
            
        except Exception as e:
            # 处理任务执行错误
            error_message = str(e)
            task_info['status'] = 'failed'
            task_info['error'] = error_message
            self.current_tasks[task_id] = task_info
            
            # 发送错误消息
            self._send_task_error(task_id, analysis_id, error_message)
    
    def _collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        收集数据
        
        Args:
            parameters: 数据收集参数
            
        Returns:
            收集的数据
        """
        # 在实际实现中，这里会调用相应的数据收集工具
        category = parameters.get('category')
        time_range = parameters.get('time_range')
        data_types = parameters.get('data_types', [])
        
        result = {}
        for data_type in data_types:
            # 调用相应的数据收集工具
            if data_type in self.tools_registry:
                tool = self.tools_registry[data_type]
                data = tool(category=category, time_range=time_range)
                result[data_type] = data
            else:
                print(f"Warning: No tool found for data type: {data_type}")
        
        return result
    
    def _analyze_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析数据
        
        Args:
            parameters: 数据分析参数
            
        Returns:
            分析结果
        """
        # 在实际实现中，这里会调用相应的数据分析工具
        analysis_methods = parameters.get('analysis_methods', [])
        dimensions = parameters.get('dimensions', [])
        
        # 获取输入数据
        # 在实际实现中，这里会从之前的任务结果中获取数据
        input_data = self._get_input_data_for_analysis()
        
        result = {}
        for method in analysis_methods:
            method_results = {}
            for dimension in dimensions:
                # 调用相应的分析工具
                tool_name = f"{method}_{dimension}"
                if tool_name in self.tools_registry:
                    tool = self.tools_registry[tool_name]
                    analysis_result = tool(data=input_data)
                    method_results[dimension] = analysis_result
                else:
                    print(f"Warning: No tool found for analysis: {tool_name}")
            
            result[method] = method_results
        
        return result
    
    def _generate_insights(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成洞察
        
        Args:
            parameters: 洞察生成参数
            
        Returns:
            生成的洞察
        """
        # 在实际实现中，这里会调用相应的洞察生成工具
        insight_types = parameters.get('insight_types', [])
        max_insights = parameters.get('max_insights', 5)
        
        # 获取输入数据
        # 在实际实现中，这里会从之前的任务结果中获取数据
        input_data = self._get_input_data_for_insights()
        
        result = {}
        for insight_type in insight_types:
            # 调用相应的洞察生成工具
            if insight_type in self.tools_registry:
                tool = self.tools_registry[insight_type]
                insights = tool(data=input_data, max_insights=max_insights)
                result[insight_type] = insights
            else:
                print(f"Warning: No tool found for insight type: {insight_type}")
        
        return result
    
    def _get_input_data_for_analysis(self) -> Dict[str, Any]:
        """
        获取用于分析的输入数据
        
        Returns:
            输入数据
        """
        # 在实际实现中，这里会从之前的任务结果中获取数据
        # 目前返回一个示例数据
        return {
            'market_data': {
                'market_size': 1000000,
                'growth_rate': 0.05,
                'competitors': ['CompA', 'CompB', 'CompC']
            },
            'sales_data': {
                'total_sales': 50000,
                'sales_growth': 0.03,
                'product_categories': {
                    'CategoryA': 20000,
                    'CategoryB': 30000
                }
            }
        }
    
    def _get_input_data_for_insights(self) -> Dict[str, Any]:
        """
        获取用于生成洞察的输入数据
        
        Returns:
            输入数据
        """
        # 在实际实现中，这里会从之前的任务结果中获取数据
        # 目前返回一个示例数据
        return {
            'trend_analysis': {
                'sales': {
                    'trend': 'upward',
                    'growth_rate': 0.03,
                    'seasonality': 'Q4 peak'
                },
                'market_share': {
                    'trend': 'stable',
                    'current_share': 0.05,
                    'competitors_share': {
                        'CompA': 0.2,
                        'CompB': 0.15,
                        'CompC': 0.1
                    }
                }
            },
            'seasonality_analysis': {
                'sales': {
                    'Q1': 10000,
                    'Q2': 12000,
                    'Q3': 13000,
                    'Q4': 15000
                }
            }
        }
    
    def _send_task_result(self, task_id: str, analysis_id: str, result: Dict[str, Any]) -> None:
        """
        发送任务结果
        
        Args:
            task_id: 任务ID
            analysis_id: 分析ID
            result: 任务结果
        """
        # 查找协调智能体ID
        coordinator_id = self._find_coordinator_id()
        
        if not coordinator_id:
            print(f"Error: Cannot find coordinator agent to send task result for task {task_id}")
            return
        
        # 发送任务结果消息
        self.send_message(
            to_agent_id=coordinator_id,
            content={
                'task_id': task_id,
                'analysis_id': analysis_id,
                'result': result
            },
            message_type='task_result'
        )
    
    def _send_task_error(self, task_id: str, analysis_id: str, error_message: str) -> None:
        """
        发送任务错误
        
        Args:
            task_id: 任务ID
            analysis_id: 分析ID
            error_message: 错误消息
        """
        # 查找协调智能体ID
        coordinator_id = self._find_coordinator_id()
        
        if not coordinator_id:
            print(f"Error: Cannot find coordinator agent to send task error for task {task_id}")
            return
        
        # 发送任务错误消息
        self.send_message(
            to_agent_id=coordinator_id,
            content={
                'task_id': task_id,
                'analysis_id': analysis_id,
                'error': error_message
            },
            message_type='task_error'
        )
    
    def _find_coordinator_id(self) -> Optional[str]:
        """
        查找协调智能体ID
        
        Returns:
            协调智能体ID，如果没有找到则返回None
        """
        # 在实际实现中，这里可能会查询某个注册表或配置
        # 目前简单地返回一个固定值
        return "coordinator_agent_1"

# 导入datetime模块，用于时间戳
from datetime import datetime