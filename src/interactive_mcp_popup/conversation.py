"""
持续对话管理模块

支持多轮对话，保持对话上下文和历史记录。
"""

import json
import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ConversationMessage:
    """对话消息"""
    id: str
    conversation_id: str
    timestamp: str
    sender: str  # "user" or "assistant"
    content: str
    message_type: str  # "question", "answer", "system"


@dataclass
class Conversation:
    """对话会话"""
    id: str
    topic: str
    context: str
    created_at: str
    updated_at: str
    status: str  # "active", "ended"
    messages: List[ConversationMessage]


class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        
    def create_conversation(self, topic: str, context: str = "") -> str:
        """创建新对话
        
        Args:
            topic: 对话主题
            context: 上下文信息
            
        Returns:
            对话ID
        """
        conversation_id = str(uuid.uuid4())
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        conversation = Conversation(
            id=conversation_id,
            topic=topic,
            context=context,
            created_at=current_time,
            updated_at=current_time,
            status="active",
            messages=[]
        )
        
        # 添加系统消息
        system_message = ConversationMessage(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            timestamp=current_time,
            sender="system",
            content=f"对话开始: {topic}",
            message_type="system"
        )
        conversation.messages.append(system_message)
        
        self.conversations[conversation_id] = conversation
        return conversation_id
    
    def add_message(self, conversation_id: str, sender: str, content: str, message_type: str = "question") -> str:
        """添加消息到对话
        
        Args:
            conversation_id: 对话ID
            sender: 发送者 ("user" or "assistant")
            content: 消息内容
            message_type: 消息类型
            
        Returns:
            消息ID
        """
        if conversation_id not in self.conversations:
            raise ValueError(f"对话 {conversation_id} 不存在")
        
        conversation = self.conversations[conversation_id]
        message_id = str(uuid.uuid4())
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        message = ConversationMessage(
            id=message_id,
            conversation_id=conversation_id,
            timestamp=current_time,
            sender=sender,
            content=content,
            message_type=message_type
        )
        
        conversation.messages.append(message)
        conversation.updated_at = current_time
        
        return message_id
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """获取对话
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            对话对象，如果不存在则返回 None
        """
        return self.conversations.get(conversation_id)
    
    def get_all_conversations(self) -> List[Conversation]:
        """获取所有对话
        
        Returns:
            对话列表
        """
        return list(self.conversations.values())
    
    def end_conversation(self, conversation_id: str, summary: str = "") -> bool:
        """结束对话
        
        Args:
            conversation_id: 对话ID
            summary: 对话总结
            
        Returns:
            是否成功
        """
        if conversation_id not in self.conversations:
            return False
        
        conversation = self.conversations[conversation_id]
        conversation.status = "ended"
        conversation.updated_at = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if summary:
            self.add_message(conversation_id, "system", f"对话结束: {summary}", "system")
        
        return True
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """获取对话历史
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            消息历史列表
        """
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return []
        
        return [asdict(message) for message in conversation.messages]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """删除对话
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            是否成功
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False
    
    def save_to_file(self, filepath: str) -> bool:
        """保存对话到文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            是否成功
        """
        try:
            data = {
                "conversations": {
                    conv_id: asdict(conv) for conv_id, conv in self.conversations.items()
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存对话失败: {e}")
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """从文件加载对话
        
        Args:
            filepath: 文件路径
            
        Returns:
            是否成功
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            conversations_data = data.get("conversations", {})
            
            for conv_id, conv_data in conversations_data.items():
                messages_data = conv_data.pop("messages", [])
                messages = [ConversationMessage(**msg_data) for msg_data in messages_data]
                
                conversation = Conversation(**conv_data)
                conversation.messages = messages
                
                self.conversations[conv_id] = conversation
            
            return True
        except Exception as e:
            print(f"加载对话失败: {e}")
            return False


# 全局对话管理器实例
conversation_manager = ConversationManager()


def get_conversation_manager() -> ConversationManager:
    """获取全局对话管理器实例"""
    return conversation_manager


if __name__ == "__main__":
    # 测试对话管理器
    manager = ConversationManager()
    
    # 创建对话
    conv_id = manager.create_conversation("测试对话", "这是一个测试对话")
    print(f"创建对话: {conv_id}")
    
    # 添加消息
    manager.add_message(conv_id, "assistant", "你好！这是一个测试消息")
    manager.add_message(conv_id, "user", "你好！这是用户回复")
    
    # 获取对话历史
    history = manager.get_conversation_history(conv_id)
    print(f"对话历史: {len(history)} 条消息")
    
    # 结束对话
    manager.end_conversation(conv_id, "测试完成")
    
    # 保存到文件
    manager.save_to_file("test_conversation.json")
    print("对话已保存到 test_conversation.json")
