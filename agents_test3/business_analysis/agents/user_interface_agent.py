from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..models.message import Message

class UserInterfaceAgent(BaseAgent):
    """
    用户交互智能体，负责与用户进行交互，接收用户请求并返回分析结果
    """
    def __init__(self, agent_id: str, name: str):
        """
        初始化用户交互智能体
        
        Args:
            agent_id: 智能体唯一标识符
            name: 智能体名称
        """
        super().__init__(agent_id, name)
        self.active_requests: Dict[str, Dict[str, Any]] = {}  # 活跃的用户请求
        self.coordinator_id: Optional[str] = None  # 协调智能体ID
    
    def set_coordinator(self, coordinator_id: str) -> None:
        """
        设置协调智能体ID
        
        Args:
            coordinator_id: 协调智能体ID
        """
        self.coordinator_id = coordinator_id
    
    def process_message(self, message: Message) -> None:
        """
        处理接收到的消息
        
        Args:
            message: 接收到的消息
        """
        if message.message_type == 'analysis_report':
            # 接收到分析报告
            self._handle_analysis_report(message)
    
    def submit_analysis_request(self, user_id: str, analysis_request: Dict[str, Any]) -> str:
        """
        提交分析请求
        
        Args:
            user_id: 用户ID
            analysis_request: 分析请求详情
            
        Returns:
            请求ID
        """
        if not self.coordinator_id:
            raise ValueError("Coordinator agent not set")
        
        # 发送分析请求给协调智能体
        request_id = self.send_message(
            to_agent_id=self.coordinator_id,
            content=analysis_request,
            message_type='analysis_request'
        )
        
        # 存储请求信息
        self.active_requests[request_id] = {
            'user_id': user_id,
            'request': analysis_request,
            'status': 'submitted',
            'submitted_at': datetime.now()
        }
        
        return request_id
    
    def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """
        获取请求状态
        
        Args:
            request_id: 请求ID
            
        Returns:
            请求状态信息
        """
        if request_id not in self.active_requests:
            return {'status': 'unknown', 'message': 'Request not found'}
        
        return {
            'status': self.active_requests[request_id]['status'],
            'submitted_at': self.active_requests[request_id]['submitted_at'].isoformat(),
            'request_type': self.active_requests[request_id]['request'].get('analysis_type')
        }
    
    def _handle_analysis_report(self, message: Message) -> None:
        """
        处理分析报告消息
        
        Args:
            message: 分析报告消息
        """
        content = message.content
        analysis_id = content.get('analysis_id')
        report = content.get('report')
        
        if not analysis_id or not report:
            print(f"Error: Invalid analysis report message: {message.message_id}")
            return
        
        # 更新请求状态
        if analysis_id in self.active_requests:
            request_info = self.active_requests[analysis_id]
            request_info['status'] = 'completed'
            request_info['completed_at'] = datetime.now()
            request_info['report'] = report
            self.active_requests[analysis_id] = request_info
            
            # 通知用户分析已完成
            self._notify_user(request_info['user_id'], analysis_id, report)
    
    def _notify_user(self, user_id: str, analysis_id: str, report: Dict[str, Any]) -> None:
        """
        通知用户分析已完成
        
        Args:
            user_id: 用户ID
            analysis_id: 分析ID
            report: 分析报告
        """
        # 在实际实现中，这里会通过某种方式通知用户，如发送邮件、推送通知等
        print(f"Notifying user {user_id} that analysis {analysis_id} is complete")
        
        # 这里可以实现将报告展示给用户的逻辑
        # 例如，生成一个可视化报告，或者将报告发送到用户的邮箱
        
        # 示例：打印报告摘要
        print(f"Analysis Report Summary: {report.get('summary')}")

# 导入datetime模块，用于时间戳
from datetime import datetime