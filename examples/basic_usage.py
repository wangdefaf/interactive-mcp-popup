#!/usr/bin/env python3
"""
基础使用示例

演示 Interactive MCP Popup 的基本功能。
"""

import sys
import os

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from interactive_mcp_popup import ask_user_popup, start_conversation, continue_conversation, end_conversation


def basic_popup_example():
    """基础弹窗示例"""
    print("=== 基础弹窗示例 ===")
    
    # 简单提问
    result = ask_user_popup(
        question="你觉得这个弹窗功能怎么样？",
        context="这是一个基础功能测试"
    )
    
    if result["status"] == "answered":
        print(f"✅ 用户回答: {result['answer']}")
        return result["answer"]
    else:
        print("❌ 用户取消了回答")
        return None


def context_popup_example():
    """带上下文的弹窗示例"""
    print("\n=== 带上下文的弹窗示例 ===")
    
    result = ask_user_popup(
        question="这个设计方案是否满足你的需求？",
        context="我们正在讨论用户界面的设计方案，包括布局、颜色和交互方式。"
    )
    
    if result["status"] == "answered":
        print(f"✅ 用户回答: {result['answer']}")
        print(f"📝 上下文: {result['context']}")
        return result
    else:
        print("❌ 用户取消了回答")
        return None


def conversation_example():
    """持续对话示例"""
    print("\n=== 持续对话示例 ===")
    
    # 开始对话
    conv_result = start_conversation(
        topic="项目规划讨论",
        context="讨论新项目的设计方案和实施计划"
    )
    
    if conv_result["status"] != "conversation_started":
        print("❌ 开始对话失败")
        return
    
    conv_id = conv_result["conversation_id"]
    print(f"🎯 对话已开始，ID: {conv_id}")
    
    # 第一轮对话
    response = continue_conversation(
        conversation_id=conv_id,
        message="你觉得这个设计方案怎么样？有什么优点和缺点？"
    )
    
    if response["status"] == "replied":
        print(f"💬 用户回复: {response['user_reply']}")
        
        # 第二轮对话
        response = continue_conversation(
            conversation_id=conv_id,
            message="基于你的反馈，你觉得我们应该优先改进哪个方面？"
        )
        
        if response["status"] == "replied":
            print(f"💬 用户建议: {response['user_reply']}")
    
    # 结束对话
    end_result = end_conversation(
        conversation_id=conv_id,
        summary="讨论了设计方案，收集了用户反馈和改进建议"
    )
    
    if end_result["status"] == "conversation_ended":
        print("🏁 对话已结束")
        return conv_id
    else:
        print("❌ 结束对话失败")
        return None


def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    def safe_ask_question(question, context=""):
        """安全的提问函数"""
        try:
            result = ask_user_popup(question, context)
            
            if result["status"] == "answered":
                return result["answer"]
            elif result["status"] == "cancelled":
                print("ℹ️ 用户取消了回答")
                return None
            elif result["status"] == "error":
                print(f"❌ 错误: {result['message']}")
                return None
            else:
                print(f"⚠️ 未知状态: {result['status']}")
                return None
                
        except Exception as e:
            print(f"💥 异常: {e}")
            return None
    
    # 使用示例
    answer = safe_ask_question("这个错误处理示例怎么样？")
    if answer:
        print(f"✅ 安全获取的回答: {answer}")


def main():
    """主函数"""
    print("🚀 Interactive MCP Popup 基础使用示例")
    print("=" * 50)
    
    # 基础弹窗
    basic_popup_example()
    
    # 带上下文的弹窗
    context_popup_example()
    
    # 持续对话
    conversation_example()
    
    # 错误处理
    error_handling_example()
    
    print("\n✨ 所有示例完成！")


if __name__ == "__main__":
    main()
