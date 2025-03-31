"""协调器模块，负责协调多个智能体之间的交互和任务分配"""

from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
import json
import uuid

from core.base import Agent, Message, AgentRegistry


class Task:
    """任务类，表示一个需要完成的分析任务"""
    
    def __init__(self, task_id: str, task_type: str, params: Dict[str, Any], priority: int = 1):
        self.task_id = task_id
        self.task_type = task_type  # 例如：market_analysis, competitor_analysis 等
        self.params = params
        self.priority = priority  # 优先级，数字越大优先级越高
        self.status = "pending"  # pending, running, completed, failed
        self.result = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.assigned_agent = None
        self.parent_task_id = None  # 父任务ID，用于任务分解
        self.subtasks: List[str] = []  # 子任务ID列表
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "params": self.params,
            "priority": self.priority,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "assigned_agent": self.assigned_agent,
            "parent_task_id": self.parent_task_id,
            "subtasks": self.subtasks
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            task_id=data["task_id"],
            task_type=data["task_type"],
            params=data["params"],
            priority=data["priority"]
        )
        task.status = data["status"]
        task.result = data["result"]
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.started_at = datetime.fromisoformat(data["started_at"]) if data["started_at"] else None
        task.completed_at = datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None
        task.assigned_agent = data["assigned_agent"]
        task.parent_task_id = data["parent_task_id"]
        task.subtasks = data["subtasks"]
        return task


class TaskRegistry:
    """任务注册表，用于管理所有任务"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskRegistry, cls).__new__(cls)
            cls._instance.tasks = {}
        return cls._instance
    
    def register(self, task: Task) -> None:
        """注册任务"""
        self.tasks[task.task_id] = task
    
    def unregister(self, task_id: str) -> None:
        """注销任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_tasks_by_type(self, task_type: str) -> List[Task]:
        """根据类型获取任务"""
        return [task for task in self.tasks.values() if task.task_type == task_type]
    
    def get_tasks_by_agent(self, agent_id: str) -> List[Task]:
        """根据分配的智能体获取任务"""
        return [task for task in self.tasks.values() if task.assigned_agent == agent_id]
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return list(self.tasks.values())


class TaskManager:
    """任务管理器，负责任务的创建、分配和状态跟踪"""
    
    def __init__(self):
        self.task_registry = TaskRegistry()
        self.agent_registry = AgentRegistry()
        self.task_type_to_agent_type = {
            "market_analysis": "market_trend_analysis_agent",
            "selling_point_analysis": "selling_point_analysis_agent",
            "competitor_analysis": "competitor_analysis_agent",
            "price_analysis": "price_analysis_agent",
            "comprehensive_analysis": "comprehensive_analysis_agent"
        }
    
    def create_task(self, task_type: str, params: Dict[str, Any], priority: int = 1) -> Task:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        task = Task(task_id, task_type, params, priority)
        self.task_registry.register(task)
        return task
    
    def decompose_task(self, task: Task, subtask_specs: List[Dict[str, Any]]) -> List[Task]:
        """将任务分解为多个子任务"""
        subtasks = []
        for spec in subtask_specs:
            subtask = self.create_task(
                task_type=spec["task_type"],
                params=spec["params"],
                priority=task.priority
            )
            subtask.parent_task_id = task.task_id
            task.subtasks.append(subtask.task_id)
            subtasks.append(subtask)
        
        # 更新父任务状态
        if task.status == "pending":
            task.status = "decomposed"
        
        return subtasks
    
    def assign_task(self, task: Task, agent_id: Optional[str] = None) -> bool:
        """分配任务给智能体"""
        if task.status != "pending":
            return False
        
        # 如果没有指定智能体，根据任务类型自动选择
        if agent_id is None:
            agent_type = self.task_type_to_agent_type.get(task.task_type)
            if not agent_type:
                return False
            
            agents = self.agent_registry.get_agents_by_type(agent_type)
            if not agents:
                return False
            
            # 简单的负载均衡：选择当前任务最少的智能体
            agent_id = min(
                agents,
                key=lambda a: len(self.task_registry.get_tasks_by_agent(a.agent_id))
            ).agent_id
        
        # 检查智能体是否存在
        agent = self.agent_registry.get_agent(agent_id)
        if not agent:
            return False
        
        # 分配任务
        task.assigned_agent = agent_id
        task.status = "assigned"
        task.started_at = datetime.now()
        
        # 发送任务给智能体
        message = Message(
            sender="task_manager",
            receiver=agent_id,
            content={
                "task_id": task.task_id,
                "task_type": task.task_type,
                "params": task.params
            },
            msg_type="task"
        )
        agent.receive_message(message)
        
        return True
    
    def update_task_status(self, task_id: str, status: str, result: Any = None) -> bool:
        """更新任务状态"""
        task = self.task_registry.get_task(task_id)
        if not task:
            return False
        
        task.status = status
        if status == "completed" or status == "failed":
            task.completed_at = datetime.now()
            task.result = result
            
            # 检查父任务是否所有子任务都已完成
            if task.parent_task_id:
                self._check_parent_task_completion(task.parent_task_id)
        
        return True
    
    def _check_parent_task_completion(self, parent_task_id: str) -> None:
        """检查父任务的所有子任务是否都已完成"""
        parent_task = self.task_registry.get_task(parent_task_id)
        if not parent_task or not parent_task.subtasks:
            return
        
        all_completed = True
        subtask_results = {}
        
        for subtask_id in parent_task.subtasks:
            subtask = self.task_registry.get_task(subtask_id)
            if not subtask or subtask.status != "completed":
                all_completed = False
                break
            subtask_results[subtask.task_type] = subtask.result
        
        if all_completed:
            # 所有子任务都已完成，更新父任务状态
            parent_task.status = "completed"
            parent_task.completed_at = datetime.now()
            parent_task.result = subtask_results
            
            # 如果父任务也有父任务，递归检查
            if parent_task.parent_task_id:
                self._check_parent_task_completion(parent_task.parent_task_id)


class Coordinator(Agent):
    """协调器，负责协调多个智能体之间的交互"""
    
    def __init__(self, agent_id: str = "coordinator"):
        super().__init__(agent_id, "coordinator")
        self.task_manager = TaskManager()
        self.agent_registry = AgentRegistry()
        self.callbacks: Dict[str, Callable] = {}  # 回调函数字典，用于处理不同类型的消息
    
    def register_callback(self, msg_type: str, callback: Callable) -> None:
        """注册回调函数"""
        self.callbacks[msg_type] = callback
    
    def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.msg_type in self.callbacks:
            return self.callbacks[message.msg_type](message)
        
        # 默认处理逻辑
        if message.msg_type == "task_request":
            # 处理任务请求
            content = message.content
            if not isinstance(content, dict) or "task_type" not in content:
                return self.send_message(
                    receiver=message.sender,
                    content={"error": "Invalid task request format. Must contain 'task_type' field."},
                    msg_type="error"
                )
            
            task_type = content["task_type"]
            params = content.get("params", {})
            priority = content.get("priority", 1)
            
            # 创建任务
            task = self.task_manager.create_task(task_type, params, priority)
            
            # 如果是综合分析任务，进行任务分解
            if task_type == "comprehensive_analysis":
                category = params.get("category", "")
                start_date = params.get("start_date", "")
                end_date = params.get("end_date", "")
                
                # 分解为多个子任务
                subtask_specs = [
                    {
                        "task_type": "market_analysis",
                        "params": {
                            "category": category,
                            "start_date": start_date,
                            "end_date": end_date,
                            "metrics": ["sales", "volume", "market_share"]
                        }
                    },
                    {
                        "task_type": "selling_point_analysis",
                        "params": {
                            "category": category,
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    },
                    {
                        "task_type": "competitor_analysis",
                        "params": {
                            "category": category,
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    },
                    {
                        "task_type": "price_analysis",
                        "params": {
                            "category": category,
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    }
                ]
                
                subtasks = self.task_manager.decompose_task(task, subtask_specs)
                
                # 分配子任务
                for subtask in subtasks:
                    self.task_manager.assign_task(subtask)
                
                return self.send_message(
                    receiver=message.sender,
                    content={
                        "task_id": task.task_id,
                        "status": "decomposed",
                        "subtasks": [subtask.task_id for subtask in subtasks]
                    },
                    msg_type="task_response"
                )
            else:
                # 直接分配任务
                success = self.task_manager.assign_task(task)
                
                if success:
                    return self.send_message(
                        receiver=message.sender,
                        content={
                            "task_id": task.task_id,
                            "status": "assigned"
                        },
                        msg_type="task_response"
                    )
                else:
                    return self.send_message(
                        receiver=message.sender,
                        content={
                            "error": "Failed to assign task. No suitable agent available."
                        },
                        msg_type="error"
                    )
        
        elif message.msg_type == "task_result":
            # 处理任务结果
            content = message.content
            if not isinstance(content, dict) or "task_id" not in content:
                return None
            
            task_id = content["task_id"]
            status = content.get("status", "completed")
            result = content.get("result")
            
            # 更新任务状态
            self.task_manager.update_task_status(task_id, status, result)
            
            # 获取任务
            task = self.task_manager.task_registry.get_task(task_id)
            if not task:
                return None
            
            # 如果任务有父任务，不需要向原始请求者发送响应
            if task.parent_task_id:
                return None
            
            # 向原始请求者发送任务完成通知
            return self.send_message(
                receiver=message.sender,
                content={
                    "task_id": task_id,
                    "status": status,
                    "result": result
                },
                msg_type="task_completed"
            )
        
        return None
    
    def run(self) -> None:
        """运行协调器的主要逻辑"""
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            if response:
                # 发送响应消息
                receiver = self.agent_registry.get_agent(response.receiver)
                if receiver:
                    receiver.receive_message(response)