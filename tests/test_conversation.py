#!/usr/bin/env python3
"""
对话功能测试

测试持续对话的各种功能和边界情况。
"""

import sys
import os
import unittest
import tempfile
import json
import time
from typing import Dict, List

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from interactive_mcp_popup.conversation import (
    ConversationManager, 
    Conversation, 
    ConversationMessage,
    get_conversation_manager
)


class TestConversationMessage(unittest.TestCase):
    """测试对话消息"""
    
    def test_message_creation(self):
        """测试消息创建"""
        message = ConversationMessage(
            id="test-id",
            conversation_id="conv-id",
            timestamp="2025-01-12 10:00:00",
            sender="user",
            content="测试消息",
            message_type="answer"
        )
        
        self.assertEqual(message.id, "test-id")
        self.assertEqual(message.conversation_id, "conv-id")
        self.assertEqual(message.sender, "user")
        self.assertEqual(message.content, "测试消息")
        self.assertEqual(message.message_type, "answer")
    
    def test_message_dataclass(self):
        """测试消息数据类"""
        message = ConversationMessage(
            id="test-id",
            conversation_id="conv-id",
            timestamp="2025-01-12 10:00:00",
            sender="assistant",
            content="助手消息",
            message_type="question"
        )
        
        # 测试转换为字典
        message_dict = message.__dict__
        self.assertEqual(message_dict["id"], "test-id")
        self.assertEqual(message_dict["sender"], "assistant")
    
    def test_message_validation(self):
        """测试消息验证"""
        # 测试有效消息
        message = ConversationMessage(
            id="valid-id",
            conversation_id="valid-conv",
            timestamp="2025-01-12 10:00:00",
            sender="user",
            content="有效消息",
            message_type="answer"
        )
        
        self.assertIsNotNone(message)
        
        # 测试必需字段
        with self.assertRaises(TypeError):
            ConversationMessage(
                id="test-id",
                # 缺少必需字段
            )


class TestConversation(unittest.TestCase):
    """测试对话会话"""
    
    def test_conversation_creation(self):
        """测试对话创建"""
        conversation = Conversation(
            id="test-conv",
            topic="测试主题",
            context="测试上下文",
            created_at="2025-01-12 10:00:00",
            updated_at="2025-01-12 10:00:00",
            status="active",
            messages=[]
        )
        
        self.assertEqual(conversation.id, "test-conv")
        self.assertEqual(conversation.topic, "测试主题")
        self.assertEqual(conversation.status, "active")
        self.assertEqual(len(conversation.messages), 0)
    
    def test_conversation_add_message(self):
        """测试添加消息"""
        conversation = Conversation(
            id="test-conv",
            topic="测试主题",
            context="测试上下文",
            created_at="2025-01-12 10:00:00",
            updated_at="2025-01-12 10:00:00",
            status="active",
            messages=[]
        )
        
        message = ConversationMessage(
            id="msg-1",
            conversation_id="test-conv",
            timestamp="2025-01-12 10:01:00",
            sender="user",
            content="用户消息",
            message_type="answer"
        )
        
        conversation.messages.append(message)
        
        self.assertEqual(len(conversation.messages), 1)
        self.assertEqual(conversation.messages[0].content, "用户消息")
    
    def test_conversation_status_change(self):
        """测试对话状态变更"""
        conversation = Conversation(
            id="test-conv",
            topic="测试主题",
            context="测试上下文",
            created_at="2025-01-12 10:00:00",
            updated_at="2025-01-12 10:00:00",
            status="active",
            messages=[]
        )
        
        # 改变状态
        conversation.status = "ended"
        conversation.updated_at = "2025-01-12 10:30:00"
        
        self.assertEqual(conversation.status, "ended")
        self.assertEqual(conversation.updated_at, "2025-01-12 10:30:00")


class TestConversationManager(unittest.TestCase):
    """测试对话管理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.manager = ConversationManager()
    
    def test_create_conversation(self):
        """测试创建对话"""
        conv_id = self.manager.create_conversation("测试主题", "测试上下文")
        
        self.assertIsNotNone(conv_id)
        self.assertIn(conv_id, self.manager.conversations)
        
        conversation = self.manager.conversations[conv_id]
        self.assertEqual(conversation.topic, "测试主题")
        self.assertEqual(conversation.context, "测试上下文")
        self.assertEqual(conversation.status, "active")
        self.assertEqual(len(conversation.messages), 1)  # 系统消息
    
    def test_add_message(self):
        """测试添加消息"""
        conv_id = self.manager.create_conversation("测试主题")
        
        msg_id = self.manager.add_message(conv_id, "user", "用户消息", "answer")
        
        self.assertIsNotNone(msg_id)
        
        conversation = self.manager.conversations[conv_id]
        self.assertEqual(len(conversation.messages), 2)  # 系统消息 + 用户消息
        
        user_message = conversation.messages[-1]
        self.assertEqual(user_message.sender, "user")
        self.assertEqual(user_message.content, "用户消息")
    
    def test_add_message_to_nonexistent_conversation(self):
        """测试向不存在的对话添加消息"""
        with self.assertRaises(ValueError):
            self.manager.add_message("non-existent", "user", "消息")
    
    def test_get_conversation(self):
        """测试获取对话"""
        conv_id = self.manager.create_conversation("测试主题")
        
        conversation = self.manager.get_conversation(conv_id)
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation.id, conv_id)
        
        # 测试获取不存在的对话
        nonexistent = self.manager.get_conversation("non-existent")
        self.assertIsNone(nonexistent)
    
    def test_get_all_conversations(self):
        """测试获取所有对话"""
        # 创建多个对话
        conv1 = self.manager.create_conversation("主题1")
        conv2 = self.manager.create_conversation("主题2")
        
        all_convs = self.manager.get_all_conversations()
        self.assertEqual(len(all_convs), 2)
        
        conv_ids = [conv.id for conv in all_convs]
        self.assertIn(conv1, conv_ids)
        self.assertIn(conv2, conv_ids)
    
    def test_end_conversation(self):
        """测试结束对话"""
        conv_id = self.manager.create_conversation("测试主题")
        
        success = self.manager.end_conversation(conv_id, "测试总结")
        self.assertTrue(success)
        
        conversation = self.manager.conversations[conv_id]
        self.assertEqual(conversation.status, "ended")
        
        # 检查是否添加了结束消息
        end_messages = [msg for msg in conversation.messages if msg.message_type == "system" and "对话结束" in msg.content]
        self.assertTrue(len(end_messages) > 0)
    
    def test_end_nonexistent_conversation(self):
        """测试结束不存在的对话"""
        success = self.manager.end_conversation("non-existent")
        self.assertFalse(success)
    
    def test_get_conversation_history(self):
        """测试获取对话历史"""
        conv_id = self.manager.create_conversation("测试主题")
        
        # 添加一些消息
        self.manager.add_message(conv_id, "assistant", "助手消息1", "question")
        self.manager.add_message(conv_id, "user", "用户回复1", "answer")
        self.manager.add_message(conv_id, "assistant", "助手消息2", "question")
        
        history = self.manager.get_conversation_history(conv_id)
        self.assertEqual(len(history), 4)  # 系统消息 + 3 个用户消息
        
        # 检查消息格式
        for msg in history:
            self.assertIn("id", msg)
            self.assertIn("conversation_id", msg)
            self.assertIn("timestamp", msg)
            self.assertIn("sender", msg)
            self.assertIn("content", msg)
            self.assertIn("message_type", msg)
    
    def test_get_conversation_history_nonexistent(self):
        """测试获取不存在对话的历史"""
        history = self.manager.get_conversation_history("non-existent")
        self.assertEqual(history, [])
    
    def test_delete_conversation(self):
        """测试删除对话"""
        conv_id = self.manager.create_conversation("测试主题")
        
        # 确认对话存在
        self.assertIn(conv_id, self.manager.conversations)
        
        # 删除对话
        success = self.manager.delete_conversation(conv_id)
        self.assertTrue(success)
        
        # 确认对话已删除
        self.assertNotIn(conv_id, self.manager.conversations)
    
    def test_delete_nonexistent_conversation(self):
        """测试删除不存在的对话"""
        success = self.manager.delete_conversation("non-existent")
        self.assertFalse(success)
    
    def test_save_and_load_conversations(self):
        """测试保存和加载对话"""
        # 创建一些对话
        conv1 = self.manager.create_conversation("主题1", "上下文1")
        conv2 = self.manager.create_conversation("主题2", "上下文2")
        
        # 添加消息
        self.manager.add_message(conv1, "user", "消息1", "answer")
        self.manager.add_message(conv2, "assistant", "消息2", "question")
        
        # 保存到文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            save_success = self.manager.save_to_file(temp_file)
            self.assertTrue(save_success)
            
            # 创建新的管理器并加载
            new_manager = ConversationManager()
            load_success = new_manager.load_from_file(temp_file)
            self.assertTrue(load_success)
            
            # 验证加载的数据
            self.assertEqual(len(new_manager.conversations), 2)
            self.assertIn(conv1, new_manager.conversations)
            self.assertIn(conv2, new_manager.conversations)
            
            # 验证消息
            conv1_loaded = new_manager.conversations[conv1]
            self.assertEqual(len(conv1_loaded.messages), 2)  # 系统消息 + 用户消息
            
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    def test_save_to_invalid_file(self):
        """测试保存到无效文件路径"""
        invalid_path = "/invalid/path/that/does/not/exist/file.json"
        
        save_success = self.manager.save_to_file(invalid_path)
        self.assertFalse(save_success)
    
    def test_load_from_invalid_file(self):
        """测试从无效文件加载"""
        invalid_file = "/invalid/path/that/does/not/exist/file.json"
        
        load_success = self.manager.load_from_file(invalid_file)
        self.assertFalse(load_success)
    
    def test_load_from_invalid_json(self):
        """测试从无效 JSON 文件加载"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name
        
        try:
            load_success = self.manager.load_from_file(temp_file)
            self.assertFalse(load_success)
        finally:
            os.unlink(temp_file)


class TestConversationIntegration(unittest.TestCase):
    """测试对话集成功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.manager = ConversationManager()
    
    def test_complete_conversation_workflow(self):
        """测试完整的对话工作流程"""
        # 1. 创建对话
        conv_id = self.manager.create_conversation("完整测试", "这是一个完整的测试对话")
        self.assertIsNotNone(conv_id)
        
        # 2. 多轮对话
        msg1_id = self.manager.add_message(conv_id, "assistant", "你好！这是一个测试。", "question")
        msg2_id = self.manager.add_message(conv_id, "user", "你好！测试收到。", "answer")
        msg3_id = self.manager.add_message(conv_id, "assistant", "测试进行得怎么样？", "question")
        msg4_id = self.manager.add_message(conv_id, "user", "测试进行得很顺利！", "answer")
        
        # 3. 获取历史
        history = self.manager.get_conversation_history(conv_id)
        self.assertEqual(len(history), 5)  # 系统消息 + 4 个用户消息
        
        # 4. 结束对话
        end_success = self.manager.end_conversation(conv_id, "完整测试成功")
        self.assertTrue(end_success)
        
        # 5. 验证最终状态
        conversation = self.manager.get_conversation(conv_id)
        self.assertEqual(conversation.status, "ended")
        self.assertEqual(len(conversation.messages), 6)  # 系统消息 + 4 个用户消息 + 结束消息
    
    def test_multiple_conversations(self):
        """测试多个对话的管理"""
        # 创建多个对话
        conv_ids = []
        for i in range(3):
            conv_id = self.manager.create_conversation(f"对话{i+1}", f"这是第{i+1}个测试对话")
            conv_ids.append(conv_id)
        
        # 为每个对话添加消息
        for i, conv_id in enumerate(conv_ids):
            self.manager.add_message(conv_id, "assistant", f"助手消息{i+1}", "question")
            self.manager.add_message(conv_id, "user", f"用户回复{i+1}", "answer")
        
        # 获取所有对话
        all_convs = self.manager.get_all_conversations()
        self.assertEqual(len(all_convs), 3)
        
        # 验证每个对话的消息数
        for conv in all_convs:
            self.assertEqual(len(conv.messages), 3)  # 系统消息 + 助手消息 + 用户消息
        
        # 结束所有对话
        for conv_id in conv_ids:
            self.manager.end_conversation(conv_id, f"对话{conv_id}结束")
        
        # 验证所有对话都已结束
        all_convs_after = self.manager.get_all_conversations()
        for conv in all_convs_after:
            self.assertEqual(conv.status, "ended")
    
    def test_conversation_persistence(self):
        """测试对话持久化"""
        # 创建对话并添加消息
        conv_id = self.manager.create_conversation("持久化测试", "测试对话持久化功能")
        self.manager.add_message(conv_id, "assistant", "测试消息", "question")
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # 保存
            save_success = self.manager.save_to_file(temp_file)
            self.assertTrue(save_success)
            
            # 创建新管理器并加载
            new_manager = ConversationManager()
            load_success = new_manager.load_from_file(temp_file)
            self.assertTrue(load_success)
            
            # 验证数据完整性
            loaded_conv = new_manager.get_conversation(conv_id)
            self.assertIsNotNone(loaded_conv)
            self.assertEqual(loaded_conv.topic, "持久化测试")
            self.assertEqual(len(loaded_conv.messages), 2)
            
            # 在新管理器中继续对话
            new_manager.add_message(conv_id, "user", "加载后的回复", "answer")
            
            updated_history = new_manager.get_conversation_history(conv_id)
            self.assertEqual(len(updated_history), 3)
            
        finally:
            os.unlink(temp_file)


def run_conversation_demo():
    """运行对话功能演示"""
    print("🧪 对话功能演示")
    print("=" * 40)
    
    manager = ConversationManager()
    
    # 演示1: 创建对话
    print("\n1. 创建对话")
    conv_id = manager.create_conversation("演示对话", "这是一个功能演示")
    print(f"对话ID: {conv_id}")
    
    # 演示2: 添加消息
    print("\n2. 添加消息")
    manager.add_message(conv_id, "assistant", "你好！这是一个演示。", "question")
    manager.add_message(conv_id, "user", "你好！演示收到。", "answer")
    print("已添加 2 条消息")
    
    # 演示3: 查看历史
    print("\n3. 查看对话历史")
    history = manager.get_conversation_history(conv_id)
    print(f"历史消息数: {len(history)}")
    for msg in history:
        print(f"  {msg['sender']}: {msg['content']}")
    
    # 演示4: 结束对话
    print("\n4. 结束对话")
    manager.end_conversation(conv_id, "演示完成")
    print("对话已结束")
    
    # 演示5: 查看所有对话
    print("\n5. 查看所有对话")
    all_convs = manager.get_all_conversations()
    print(f"总对话数: {len(all_convs)}")
    for conv in all_convs:
        print(f"  {conv['topic']} - {conv['status']} ({conv['message_count']} 条消息)")
    
    print("\n✅ 演示完成")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_conversation_demo()
    else:
        unittest.main()
