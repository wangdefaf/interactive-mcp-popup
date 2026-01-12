# 使用示例

## 基础使用

### 简单弹窗提问

```python
from interactive_mcp_popup import ask_user_popup

# 基础提问
result = ask_user_popup(
    question="你觉得这个功能怎么样？"
)

if result["status"] == "answered":
    print(f"用户回答: {result['answer']}")
else:
    print("用户取消了回答")
```

### 带上下文的弹窗

```python
result = ask_user_popup(
    question="这个设计是否满足你的需求？",
    context="我们正在讨论用户界面的设计方案"
)

if result["status"] == "answered":
    print(f"上下文: {result['context']}")
    print(f"回答: {result['answer']}")
```

## 持续对话

### 基础对话流程

```python
from interactive_mcp_popup import (
    start_conversation,
    continue_conversation,
    end_conversation
)

# 1. 开始对话
conv_result = start_conversation(
    topic="项目规划讨论",
    context="讨论新项目的设计方案和实施计划"
)

if conv_result["status"] == "conversation_started":
    conv_id = conv_result["conversation_id"]
    print(f"对话已开始，ID: {conv_id}")
    
    # 2. 继续对话
    response = continue_conversation(
        conversation_id=conv_id,
        message="你觉得这个设计方案怎么样？"
    )
    
    if response["status"] == "replied":
        print(f"用户回复: {response['user_reply']}")
        
        # 3. 更多对话
        response = continue_conversation(
            conversation_id=conv_id,
            message="有什么改进建议吗？"
        )
        
        if response["status"] == "replied":
            print(f"用户建议: {response['user_reply']}")
    
    # 4. 结束对话
    end_result = end_conversation(
        conversation_id=conv_id,
        summary="讨论了设计方案，收集了用户反馈"
    )
    
    if end_result["status"] == "conversation_ended":
        print("对话已结束")
```

### 对话历史查看

```python
from interactive_mcp_popup import get_conversation_history

# 获取对话历史
history_result = get_conversation_history(conv_id)

if history_result["status"] == "success":
    messages = history_result["messages"]
    for msg in messages:
        print(f"{msg['sender']}: {msg['content']}")
```

## 高级使用

### 错误处理

```python
def safe_ask_question(question, context=""):
    try:
        result = ask_user_popup(question, context)
        
        if result["status"] == "answered":
            return result["answer"]
        elif result["status"] == "cancelled":
            print("用户取消了回答")
            return None
        elif result["status"] == "error":
            print(f"错误: {result['message']}")
            return None
        else:
            print(f"未知状态: {result['status']}")
            return None
            
    except Exception as e:
        print(f"异常: {e}")
        return None

# 使用示例
answer = safe_ask_question("你觉得这个功能怎么样？")
if answer:
    print(f"用户回答: {answer}")
```

### 批量处理

```python
def batch_ask_questions(questions):
    """批量提问"""
    results = []
    
    for i, question in enumerate(questions):
        result = ask_user_popup(
            question=f"问题 {i+1}: {question}",
            context=f"批量处理 - 第 {i+1} 个问题"
        )
        
        results.append({
            "question": question,
            "result": result
        })
    
    return results

# 使用示例
questions = [
    "你觉得这个功能怎么样？",
    "有什么改进建议吗？",
    "愿意推荐给其他人吗？"
]

results = batch_ask_questions(questions)
for item in results:
    print(f"问题: {item['question']}")
    if item["result"]["status"] == "answered":
        print(f"回答: {item['result']['answer']}")
    print("---")
```

### 对话管理

```python
from interactive_mcp_popup import get_all_conversations, save_conversations

# 获取所有对话
all_conv = get_all_conversations()

if all_conv["status"] == "success":
    conversations = all_conv["conversations"]
    
    # 显示活跃对话
    active_convs = [c for c in conversations if c["status"] == "active"]
    print(f"活跃对话数: {len(active_convs)}")
    
    for conv in active_convs:
        print(f"- {conv['topic']} ({conv['message_count']} 条消息)")

# 保存所有对话
save_result = save_conversations()
if save_result["status"] == "success":
    print(f"对话已保存到: {save_result['output_file']}")
```

## 实际应用场景

### 代码审查反馈

```python
def get_code_review_feedback(file_path, code_content):
    """获取代码审查反馈"""
    
    # 开始代码审查对话
    conv_id = start_conversation(
        topic=f"代码审查: {file_path}",
        context=f"审查以下代码文件的内容和结构"
    )["conversation_id"]
    
    # 询问整体印象
    response = continue_conversation(
        conversation_id=conv_id,
        message=f"请审查以下代码：\n\n{code_content[:500]}...\n\n整体印象如何？"
    )
    
    if response["status"] == "replied":
        impression = response["user_reply"]
        
        # 询问具体问题
        response = continue_conversation(
            conversation_id=conv_id,
            message="有什么具体的改进建议吗？"
        )
        
        if response["status"] == "replied":
            suggestions = response["user_reply"]
    
    # 结束对话
    end_conversation(conv_id, f"代码审查完成。印象: {impression}, 建议: {suggestions}")
    
    return {
        "impression": impression,
        "suggestions": suggestions
    }
```

### 用户调研

```python
def conduct_user_survey():
    """进行用户调研"""
    
    survey_id = start_conversation(
        topic="用户体验调研",
        context="收集用户对产品的反馈和建议"
    )["conversation_id"]
    
    questions = [
        "你最喜欢产品的哪个功能？",
        "有什么功能你觉得需要改进？",
        "愿意推荐给朋友吗？",
        "还有什么其他建议？"
    ]
    
    responses = {}
    
    for question in questions:
        response = continue_conversation(
            conversation_id=survey_id,
            message=question
        )
        
        if response["status"] == "replied":
            responses[question] = response["user_reply"]
    
    end_conversation(survey_id, "用户调研完成")
    
    return responses
```

### 技术支持

```python
def technical_support_session(user_issue):
    """技术支持会话"""
    
    support_id = start_conversation(
        topic="技术支持",
        context=f"用户报告的问题: {user_issue}"
    )["conversation_id"]
    
    # 诊断问题
    response = continue_conversation(
        conversation_id=support_id,
        message="我正在帮你解决这个问题。能提供更多详细信息吗？"
    )
    
    if response["status"] == "replied":
        details = response["user_reply"]
        
        # 提供解决方案
        response = continue_conversation(
            conversation_id=support_id,
            message="根据你提供的信息，我建议以下解决方案..."
        )
        
        if response["status"] == "replied":
            feedback = response["user_reply"]
    
    end_conversation(support_id, f"技术支持完成。问题: {user_issue}, 解决方案已提供")
    
    return {
        "details": details,
        "feedback": feedback
    }
```

## 最佳实践

### 1. 上下文使用

```python
# 好的做法：提供清晰的上下文
result = ask_user_popup(
    question="这个算法的时间复杂度合适吗？",
    context="我们正在优化数据处理模块的性能"
)

# 避免：缺乏上下文
result = ask_user_popup("时间复杂度合适吗？")
```

### 2. 对话主题

```python
# 好的做法：明确具体的主题
conv_id = start_conversation(
    topic="数据库查询优化",
    context="讨论 SQL 查询的性能优化方案"
)

# 避免：模糊的主题
conv_id = start_conversation("讨论问题")
```

### 3. 错误处理

```python
# 好的做法：完整的错误处理
def robust_popup_interaction(question, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = ask_user_popup(question)
            if result["status"] == "answered":
                return result["answer"]
            elif result["status"] == "cancelled":
                return None
        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt == max_retries - 1:
                raise
    return None
```

### 4. 资源管理

```python
# 好的做法：及时清理资源
import atexit
from interactive_mcp_popup import save_conversations

def cleanup():
    save_conversations()

atexit.register(cleanup)
```

## 集成示例

### 与现有 MCP 工具集成

```python
def enhanced_mcp_workflow():
    """增强的 MCP 工作流程"""
    
    # 1. 使用弹窗确认操作
    confirmation = ask_user_popup(
        "是否继续执行这个操作？",
        "这将修改多个文件，请确认"
    )
    
    if confirmation["status"] != "answered" or confirmation["answer"].lower() != "yes":
        return "操作已取消"
    
    # 2. 开始操作对话
    conv_id = start_conversation(
        topic="操作执行",
        context="正在执行文件修改操作"
    )
    
    # 3. 执行操作并反馈
    try:
        # 执行操作...
        response = continue_conversation(
            conversation_id=conv_id,
            message="操作已完成，结果如下..."
        )
        
        if response["status"] == "replied":
            feedback = response["user_reply"]
            print(f"用户反馈: {feedback}")
    
    finally:
        end_conversation(conv_id, "操作执行完成")
    
    return "操作成功完成"
```

这些示例展示了如何在实际场景中使用 Interactive MCP Popup 的各种功能。
