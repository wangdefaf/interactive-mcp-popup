"""
Interactive MCP Popup 主服务器 (修复版本)

整合 Qt 弹窗和持续对话功能的 MCP 服务器。
修复了输出验证错误，所有工具返回字符串。
"""

import json
import tempfile
import os
import sys
from typing import Annotated, Dict, Optional

from pydantic import Field
from fastmcp import FastMCP

# 添加当前目录到 Python 路径，支持相对导入
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

from interactive_mcp_popup.popup import show_popup_dialog, save_result_to_file
from interactive_mcp_popup.conversation import get_conversation_manager, ConversationManager

# 创建 FastMCP 实例
mcp = FastMCP("Interactive MCP Popup", log_level="ERROR")

# 获取对话管理器
conversation_manager = get_conversation_manager()


@mcp.tool()
def ask_user_popup(
    question: Annotated[str, Field(description="要问用户的问题")],
    context: Annotated[str, Field(description="上下文信息，可选")] = ""
) -> str:
    """使用 Qt 弹窗向用户提问并等待回答"""
    try:
        result = show_popup_dialog(question, context)
        
        if result:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
                output_file = f.name
            
            if save_result_to_file(result, output_file):
                response_data = {
                    "status": "answered",
                    "question": question,
                    "context": context,
                    "answer": result["answer"],
                    "output_file": output_file,
                    "message": "用户已通过弹窗回答问题"
                }
            else:
                response_data = {
                    "status": "answered",
                    "question": question,
                    "context": context,
                    "answer": result["answer"],
                    "message": "用户已通过弹窗回答问题（保存文件失败）"
                }
        else:
            response_data = {
                "status": "cancelled",
                "question": question,
                "context": context,
                "message": "用户取消了回答"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "question": question,
            "context": context,
            "message": f"弹窗操作失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def start_conversation(
    topic: Annotated[str, Field(description="对话主题")],
    context: Annotated[str, Field(description="上下文信息，可选")] = ""
) -> str:
    """开始一个持续对话"""
    try:
        conversation_id = conversation_manager.create_conversation(topic, context)
        
        response_data = {
            "status": "conversation_started",
            "conversation_id": conversation_id,
            "topic": topic,
            "context": context,
            "message": "对话已开始",
            "instructions": "使用 continue_conversation 工具继续对话，使用 end_conversation 工具结束对话"
        }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "message": f"开始对话失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def continue_conversation(
    conversation_id: Annotated[str, Field(description="对话ID")],
    message: Annotated[str, Field(description="你的消息")]
) -> str:
    """继续对话"""
    try:
        conversation_manager.add_message(conversation_id, "assistant", message, "question")
        
        result = show_popup_dialog(message, f"对话ID: {conversation_id}")
        
        if result:
            user_reply = result["answer"]
            conversation_manager.add_message(conversation_id, "user", user_reply, "answer")
            
            response_data = {
                "status": "replied",
                "conversation_id": conversation_id,
                "your_message": message,
                "user_reply": user_reply,
                "message": "用户已回复，可以继续对话"
            }
        else:
            response_data = {
                "status": "cancelled",
                "conversation_id": conversation_id,
                "your_message": message,
                "message": "用户取消了回复"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "conversation_id": conversation_id,
            "your_message": message,
            "message": f"继续对话失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def end_conversation(
    conversation_id: Annotated[str, Field(description="对话ID")],
    summary: Annotated[str, Field(description="对话总结")] = ""
) -> str:
    """结束对话"""
    try:
        success = conversation_manager.end_conversation(conversation_id, summary)
        
        if success:
            response_data = {
                "status": "conversation_ended",
                "conversation_id": conversation_id,
                "summary": summary,
                "message": "对话已结束"
            }
        else:
            response_data = {
                "status": "error",
                "conversation_id": conversation_id,
                "message": "对话不存在或已结束"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "conversation_id": conversation_id,
            "message": f"结束对话失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def get_conversation_history(
    conversation_id: Annotated[str, Field(description="对话ID")]
) -> str:
    """获取对话历史"""
    try:
        history = conversation_manager.get_conversation_history(conversation_id)
        conversation = conversation_manager.get_conversation(conversation_id)
        
        if conversation:
            response_data = {
                "status": "success",
                "conversation_id": conversation_id,
                "topic": conversation.topic,
                "context": conversation.context,
                "status": conversation.status,
                "messages": history,
                "total_messages": len(history),
                "message": f"找到 {len(history)} 条对话消息"
            }
        else:
            response_data = {
                "status": "error",
                "conversation_id": conversation_id,
                "message": "对话不存在"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "conversation_id": conversation_id,
            "message": f"获取对话历史失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def get_all_conversations() -> str:
    """获取所有对话列表"""
    try:
        conversations = conversation_manager.get_all_conversations()
        
        conversation_list = []
        for conv in conversations:
            conversation_list.append({
                "id": conv.id,
                "topic": conv.topic,
                "context": conv.context,
                "status": conv.status,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
                "message_count": len(conv.messages)
            })
        
        response_data = {
            "status": "success",
            "conversations": conversation_list,
            "total_count": len(conversation_list),
            "active_count": len([c for c in conversation_list if c["status"] == "active"]),
            "message": f"找到 {len(conversation_list)} 个对话"
        }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "message": f"获取对话列表失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def test_popup() -> str:
    """测试弹窗功能"""
    try:
        result = show_popup_dialog(
            "这是一个测试弹窗，你觉得这个设计怎么样？",
            "这是测试上下文，用来验证弹窗的显示效果。"
        )
        
        if result:
            response_data = {
                "status": "success",
                "test_result": result,
                "message": "弹窗测试成功"
            }
        else:
            response_data = {
                "status": "cancelled",
                "message": "用户取消了测试"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "message": f"测试失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


@mcp.tool()
def check_dependencies() -> str:
    """检查依赖"""
    try:
        import PySide6
        response_data = {
            "status": "available",
            "pyside6_version": PySide6.__version__,
            "message": "PySide6 可用，弹窗功能正常"
        }
    except ImportError:
        response_data = {
            "status": "unavailable",
            "message": "PySide6 不可用，请安装: uv add pyside6"
        }
    
    return json.dumps(response_data, ensure_ascii=False)


@mcp.tool()
def save_conversations() -> str:
    """保存所有对话到文件"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            output_file = f.name
        
        success = conversation_manager.save_to_file(output_file)
        
        if success:
            response_data = {
                "status": "success",
                "output_file": output_file,
                "message": f"对话已保存到: {output_file}"
            }
        else:
            response_data = {
                "status": "error",
                "message": "保存对话失败"
            }
        
        return json.dumps(response_data, ensure_ascii=False)
    
    except Exception as e:
        error_data = {
            "status": "error",
            "message": f"保存对话失败: {str(e)}"
        }
        return json.dumps(error_data, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
