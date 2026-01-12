#!/usr/bin/env python3
"""
高级使用示例

演示 Interactive MCP Popup 的高级功能和实际应用场景。
"""

import sys
import os
import json
import time
from typing import List, Dict, Any

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from interactive_mcp_popup import (
    ask_user_popup, 
    start_conversation, 
    continue_conversation, 
    end_conversation,
    get_conversation_history,
    get_all_conversations,
    save_conversations
)


class CodeReviewHelper:
    """代码审查助手"""
    
    def __init__(self):
        self.review_sessions = []
    
    def review_code(self, file_path: str, code_content: str):
        """进行代码审查"""
        print(f"🔍 开始审查代码文件: {file_path}")
        
        # 开始代码审查对话
        conv_id = start_conversation(
            topic=f"代码审查: {file_path}",
            context=f"审查以下代码文件的内容、结构和质量"
        )["conversation_id"]
        
        review_result = {
            "file_path": file_path,
            "conversation_id": conv_id,
            "feedback": {}
        }
        
        # 整体印象
        response = continue_conversation(
            conversation_id=conv_id,
            message=f"请审查以下代码（前500字符）:\n\n{code_content[:500]}...\n\n整体印象如何？代码质量如何？"
        )
        
        if response["status"] == "replied":
            review_result["feedback"]["overall"] = response["user_reply"]
            
            # 具体问题
            response = continue_conversation(
                conversation_id=conv_id,
                message="有什么具体的改进建议吗？比如性能、可读性、安全性等方面？"
            )
            
            if response["status"] == "replied":
                review_result["feedback"]["suggestions"] = response["user_reply"]
                
                # 优先级评估
                response = continue_conversation(
                    conversation_id=conv_id,
                    message="哪些改进建议最重要？请按优先级排序。"
                )
                
                if response["status"] == "replied":
                    review_result["feedback"]["priority"] = response["user_reply"]
        
        # 结束审查
        end_conversation(conv_id, f"代码审查完成: {file_path}")
        
        self.review_sessions.append(review_result)
        return review_result
    
    def get_review_summary(self):
        """获取审查总结"""
        if not self.review_sessions:
            return "没有审查记录"
        
        summary = f"已完成 {len(self.review_sessions)} 个代码审查:\n\n"
        
        for i, session in enumerate(self.review_sessions, 1):
            summary += f"{i}. {session['file_path']}\n"
            summary += f"   整体印象: {session['feedback'].get('overall', 'N/A')}\n"
            summary += f"   建议: {session['feedback'].get('suggestions', 'N/A')}\n\n"
        
        return summary


class UserSurveyManager:
    """用户调研管理器"""
    
    def __init__(self):
        self.surveys = {}
    
    def conduct_survey(self, survey_name: str, questions: List[str]) -> Dict[str, str]:
        """进行用户调研"""
        print(f"📊 开始用户调研: {survey_name}")
        
        survey_id = start_conversation(
            topic=f"用户调研: {survey_name}",
            context=f"收集用户对 {survey_name} 的反馈和建议"
        )["conversation_id"]
        
        responses = {}
        
        for i, question in enumerate(questions, 1):
            print(f"提问 {i}/{len(questions)}: {question}")
            
            response = continue_conversation(
                conversation_id=survey_id,
                message=question
            )
            
            if response["status"] == "replied":
                responses[question] = response["user_reply"]
            else:
                responses[question] = "未回答"
        
        # 结束调研
        end_conversation(survey_id, f"用户调研完成: {survey_name}")
        
        self.surveys[survey_name] = {
            "conversation_id": survey_id,
            "questions": questions,
            "responses": responses,
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return responses
    
    def analyze_survey(self, survey_name: str) -> str:
        """分析调研结果"""
        if survey_name not in self.surveys:
            return f"调研 {survey_name} 不存在"
        
        survey = self.surveys[survey_name]
        responses = survey["responses"]
        
        analysis = f"调研分析: {survey_name}\n"
        analysis += f"完成时间: {survey['completed_at']}\n"
        analysis += f"问题数量: {len(responses)}\n\n"
        
        for question, answer in responses.items():
            analysis += f"问题: {question}\n"
            analysis += f"回答: {answer}\n\n"
        
        return analysis


class TechnicalSupportSession:
    """技术支持会话"""
    
    def __init__(self):
        self.sessions = []
    
    def handle_support_request(self, user_issue: str, user_details: Dict[str, str] = None) -> Dict[str, Any]:
        """处理技术支持请求"""
        print(f"🛠️ 处理技术支持请求: {user_issue}")
        
        support_id = start_conversation(
            topic="技术支持",
            context=f"用户问题: {user_issue}\n用户详情: {user_details or '无'}"
        )["conversation_id"]
        
        session_data = {
            "support_id": support_id,
            "user_issue": user_issue,
            "user_details": user_details or {},
            "conversation_log": [],
            "resolution": None
        }
        
        # 收集更多信息
        response = continue_conversation(
            conversation_id=support_id,
            message="我正在帮你解决这个问题。能提供更多详细信息吗？比如错误消息、操作步骤等。"
        )
        
        if response["status"] == "replied":
            session_data["conversation_log"].append({
                "type": "info_request",
                "content": "请求更多信息",
                "response": response["user_reply"]
            })
            
            details = response["user_reply"]
            
            # 提供解决方案
            response = continue_conversation(
                conversation_id=support_id,
                message=f"根据你提供的信息，我建议以下解决方案：\n1. 检查配置文件\n2. 重启服务\n3. 清理缓存\n\n你希望我详细说明哪一步？"
            )
            
            if response["status"] == "replied":
                session_data["conversation_log"].append({
                    "type": "solution_offer",
                    "content": "提供解决方案",
                    "response": response["user_reply"]
                })
                
                # 确认解决
                response = continue_conversation(
                    conversation_id=support_id,
                    message="问题解决了吗？如果还有其他问题，请告诉我。"
                )
                
                if response["status"] == "replied":
                    session_data["conversation_log"].append({
                        "type": "resolution_check",
                        "content": "确认解决状态",
                        "response": response["user_reply"]
                    })
                    
                    session_data["resolution"] = response["user_reply"]
        
        # 结束支持会话
        end_conversation(support_id, f"技术支持会话完成: {user_issue}")
        
        self.sessions.append(session_data)
        return session_data
    
    def get_support_summary(self) -> str:
        """获取支持会话总结"""
        if not self.sessions:
            return "没有支持会话记录"
        
        summary = f"技术支持会话总结:\n"
        summary += f"总会话数: {len(self.sessions)}\n\n"
        
        for i, session in enumerate(self.sessions, 1):
            summary += f"{i}. 问题: {session['user_issue']}\n"
            summary += f"   解决状态: {session['resolution'] or '未解决'}\n"
            summary += f"   对话轮数: {len(session['conversation_log'])}\n\n"
        
        return summary


def batch_processing_example():
    """批量处理示例"""
    print("🔄 批量处理示例")
    
    questions = [
        "你觉得这个功能怎么样？",
        "有什么改进建议吗？",
        "愿意推荐给其他人吗？",
        "最满意哪个方面？"
    ]
    
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"处理问题 {i}/{len(questions)}")
        
        result = ask_user_popup(
            question=f"批量问题 {i}: {question}",
            context=f"批量反馈收集 - 第 {i} 个问题"
        )
        
        results.append({
            "question_number": i,
            "question": question,
            "result": result
        })
    
    # 分析结果
    answered_count = sum(1 for r in results if r["result"]["status"] == "answered")
    
    print(f"\n📊 批量处理结果:")
    print(f"总问题数: {len(questions)}")
    print(f"已回答: {answered_count}")
    print(f"回答率: {answered_count/len(questions)*100:.1f}%")
    
    return results


def conversation_management_example():
    """对话管理示例"""
    print("💬 对话管理示例")
    
    # 创建多个对话
    conversations = []
    
    topics = [
        ("UI设计讨论", "讨论用户界面的设计方案"),
        ("性能优化", "讨论系统性能优化方案"),
        ("功能规划", "讨论新功能开发计划")
    ]
    
    for topic, context in topics:
        conv_id = start_conversation(topic, context)["conversation_id"]
        conversations.append(conv_id)
        print(f"创建对话: {topic} (ID: {conv_id})")
    
    # 获取所有对话
    all_conv = get_all_conversations()
    
    if all_conv["status"] == "success":
        print(f"\n📋 所有对话:")
        for conv in all_conv["conversations"]:
            status_icon = "🟢" if conv["status"] == "active" else "🔴"
            print(f"{status_icon} {conv['topic']} ({conv['message_count']} 条消息)")
    
    # 保存对话
    save_result = save_conversations()
    if save_result["status"] == "success":
        print(f"\n💾 对话已保存到: {save_result['output_file']}")
    
    return conversations


def real_world_scenario_example():
    """真实世界场景示例"""
    print("🌍 真实世界场景示例")
    
    # 场景1: 代码审查
    print("\n📝 场景1: 代码审查")
    reviewer = CodeReviewHelper()
    
    code_sample = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
"""
    
    review_result = reviewer.review_code("calculate_total.py", code_sample)
    print(f"审查完成: {review_result['file_path']}")
    
    # 场景2: 用户调研
    print("\n📊 场景2: 用户调研")
    survey_manager = UserSurveyManager()
    
    survey_questions = [
        "你最喜欢产品的哪个功能？",
        "有什么功能你觉得需要改进？",
        "愿意推荐给朋友吗？",
        "还有什么其他建议？"
    ]
    
    survey_responses = survey_manager.conduct_survey("产品满意度调研", survey_questions)
    print(f"调研完成，收到 {len(survey_responses)} 个回答")
    
    # 场景3: 技术支持
    print("\n🛠️ 场景3: 技术支持")
    support_agent = TechnicalSupportSession()
    
    support_result = support_agent.handle_support_request(
        "应用启动时崩溃",
        {"操作系统": "Windows 11", "版本": "2.1.0"}
    )
    print(f"支持会话完成: {support_result['support_id']}")
    
    return {
        "code_review": review_result,
        "survey": survey_responses,
        "support": support_result
    }


def main():
    """主函数"""
    print("🚀 Interactive MCP Popup 高级使用示例")
    print("=" * 60)
    
    try:
        # 批量处理
        batch_processing_example()
        
        # 对话管理
        conversation_management_example()
        
        # 真实世界场景
        real_world_scenario_example()
        
        print("\n✨ 所有高级示例完成！")
        
    except Exception as e:
        print(f"❌ 示例执行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
