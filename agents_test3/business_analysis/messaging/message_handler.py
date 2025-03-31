from typing import Dict, List, Callable, Any
from ..models.message import Message

class MessageHandler:
    """
    消息处理器，负责智能体之间的消息传递
    """
    def __init__(self):
        """
        初始化消息处理器
        """
        self.agents = {}  # 注册的智能体字典
        self.message_callbacks: Dict[str, List[Callable]] = {}  # 消息回调函数
    
    def register_agent(self, agent_id: str, agent) -> None:
        """
        注册智能体
        
        Args:
            agent_id: 智能体ID
            agent: 智能体实例
        """
        self.agents[agent_id] = agent
        agent.set_message_handler(self)
    
    def send_message(self, message: Message) -> None:
        """
        发送消息
        
        Args:
            message: 要发送的消息
        """
        # 记录消息（可用于调试或监控）
        self._log_message(message)
        
        # 检查接收者是否存在
        if message.to_agent_id not in self.agents:
            print(f"Error: Agent {message.to_agent_id} not found for message {message.message_id}")
            return
        
        # 将消息发送给接收者
        receiver = self.agents[message.to_agent_id]
        receiver.receive_message(message)
        
        # 触发消息回调
        self._trigger_callbacks(message)
    
    def register_callback(self, message_type: str, callback: Callable) -> None:
        """
        注册消息回调函数
        
        Args:
            message_type: 消息类型
            callback: 回调函数
        """
        if message_type not in self.message_callbacks:
            self.message_callbacks[message_type] = []
        
        self.message_callbacks[message_type].append(callback)
    
    def _trigger_callbacks(self, message: Message) -> None:
        """
        触发消息回调函数
        
        Args:
            message: 消息
        """
        if message.message_type in self.message_callbacks:
            for callback in self.message_callbacks[message.message_type]:
                callback(message)
    
    def _log_message(self, message: Message) -> None:
        """
        记录消息
        
        Args:
            message: 消息
        """
        # 在实际实现中，这里可能会将消息记录到日志系统
        # 目前简单地打印消息
        print(f"Message {message.message_id}: {message.from_agent_id} -> {message.to_agent_id} [{message.message_type}]")