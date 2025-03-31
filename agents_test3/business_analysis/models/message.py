from typing import Dict, Any, Optional
from datetime import datetime

class Message:
    """
    智能体之间通信的消息模型
    """
    def __init__(self, message_id: str, from_agent_id: str, to_agent_id: str,
                 content: Dict[str, Any], message_type: str,
                 reference_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        """
        初始化消息
        
        Args:
            message_id: 消息唯一标识符
            from_agent_id: 发送消息的智能体ID
            to_agent_id: 接收消息的智能体ID
            content: 消息内容
            message_type: 消息类型，如'task_assignment', 'task_result', 'analysis_request'等
            reference_id: 引用的消息ID（如果是回复）
            timestamp: 消息时间戳
        """
        self.message_id = message_id
        self.from_agent_id = from_agent_id
        self.to_agent_id = to_agent_id
        self.content = content
        self.message_type = message_type
        self.reference_id = reference_id
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将消息转换为字典
        
        Returns:
            消息的字典表示
        """
        return {
            'message_id': self.message_id,
            'from_agent_id': self.from_agent_id,
            'to_agent_id': self.to_agent_id,
            'content': self.content,
            'message_type': self.message_type,
            'reference_id': self.reference_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        从字典创建消息
        
        Args:
            data: 消息的字典表示
            
        Returns:
            创建的消息实例
        """
        timestamp = None
        if data.get('timestamp'):
            timestamp = datetime.fromisoformat(data['timestamp'])
            
        return cls(
            message_id=data['message_id'],
            from_agent_id=data['from_agent_id'],
            to_agent_id=data['to_agent_id'],
            content=data['content'],
            message_type=data['message_type'],
            reference_id=data.get('reference_id'),
            timestamp=timestamp
        )