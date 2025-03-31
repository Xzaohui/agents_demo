from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
from ..models.message import Message

class BaseAgent:
    """
    基础智能体类，所有智能体的父类
    提供基本的通信和记忆功能
    """
    def __init__(self, agent_id: str, name: str):
        """
        初始化基础智能体
        
        Args:
            agent_id: 智能体唯一标识符
            name: 智能体名称
        """
        self.agent_id = agent_id
        self.name = name
        self.memory: Dict[str, Any] = {}  # 智能体内部记忆
        self.message_queue: List[Message] = []  # 消息队列
        self.message_handler = None  # 消息处理器
    
    def send_message(self, to_agent_id: str, content: Dict[str, Any], 
                     message_type: str, reference_id: Optional[str] = None) -> str:
        """
        发送消息给其他智能体
        
        Args:
            to_agent_id: 接收消息的智能体ID
            content: 消息内容
            message_type: 消息类型
            reference_id: 引用的消息ID（如果是回复）
            
        Returns:
            发送的消息ID
        """
        message_id = str(uuid.uuid4())
        message = Message(
            message_id=message_id,
            from_agent_id=self.agent_id,
            to_agent_id=to_agent_id,
            content=content,
            message_type=message_type,
            reference_id=reference_id,
            timestamp=datetime.now()
        )
        
        # 这里应该调用消息传递系统将消息发送出去
        # 在实际实现中，这里会连接到消息队列或事件总线
        if self.message_handler:
            self.message_handler.send_message(message)
        
        return message_id
    
    def receive_message(self, message: Message) -> None:
        """
        接收消息
        
        Args:
            message: 接收到的消息
        """
        self.message_queue.append(message)
    
    def process_messages(self) -> None:
        """
        处理消息队列中的所有消息
        """
        while self.message_queue:
            message = self.message_queue.pop(0)
            self.process_message(message)
    
    def process_message(self, message: Message) -> None:
        """
        处理单个消息，子类应该重写此方法
        
        Args:
            message: 接收到的消息
        """
        pass
    
    def update_memory(self, key: str, value: Any) -> None:
        """
        更新智能体内部记忆
        
        Args:
            key: 记忆键
            value: 记忆值
        """
        self.memory[key] = value
    
    def get_memory(self, key: str) -> Any:
        """
        获取智能体内部记忆
        
        Args:
            key: 记忆键
            
        Returns:
            记忆值，如果不存在则返回None
        """
        return self.memory.get(key)
    
    def act(self) -> None:
        """
        智能体的主要行动逻辑，子类应该重写此方法
        """
        pass
    
    def set_message_handler(self, handler) -> None:
        """
        设置消息处理器
        
        Args:
            handler: 消息处理器实例
        """
        self.message_handler = handler