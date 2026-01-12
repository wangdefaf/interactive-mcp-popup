# API 文档

## 概述

Interactive MCP Popup 提供了一套完整的 MCP 工具，支持 Qt 弹窗和持续对话功能。

## 弹窗工具

### ask_user_popup

使用 Qt 弹窗向用户提问并等待回答。

**参数：**
- `question` (str): 要问用户的问题
- `context` (str, 可选): 上下文信息

**返回：**
```json
{
  "status": "answered",
  "question": "问题内容",
  "context": "上下文信息",
  "answer": "用户回答",
  "output_file": "临时文件路径",
  "message": "状态信息"
}
```

**示例：**
```python
result = ask_user_popup(
    question="你觉得这个功能怎么样？",
    context="这是一个测试问题"
)
```

### test_popup

测试弹窗功能。

**参数：**
无

**返回：**
```json
{
  "status": "success",
  "test_result": {
    "question": "测试问题",
    "answer": "用户回答",
    "status": "answered"
  },
  "message": "弹窗测试成功"
}
```

### check_dependencies

检查依赖是否可用。

**参数：**
无

**返回：**
```json
{
  "status": "available",
  "pyside6_version": "6.8.2.1",
  "message": "PySide6 可用，弹窗功能正常"
}
```

## 对话工具

### start_conversation

开始一个持续对话。

**参数：**
- `topic` (str): 对话主题
- `context` (str, 可选): 上下文信息

**返回：**
```json
{
  "status": "conversation_started",
  "conversation_id": "uuid",
  "topic": "对话主题",
  "context": "上下文信息",
  "message": "对话已开始",
  "instructions": "使用说明"
}
```

**示例：**
```python
conv_id = start_conversation("项目规划讨论", "讨论新项目的设计方案")
```

### continue_conversation

继续对话，发送消息并等待用户回复。

**参数：**
- `conversation_id` (str): 对话ID
- `message` (str): 你的消息

**返回：**
```json
{
  "status": "replied",
  "conversation_id": "uuid",
  "your_message": "你的消息",
  "user_reply": "用户回复",
  "message": "用户已回复，可以继续对话"
}
```

**示例：**
```python
response = continue_conversation(conv_id, "你觉得这个设计怎么样？")
```

### end_conversation

结束对话。

**参数：**
- `conversation_id` (str): 对话ID
- `summary` (str, 可选): 对话总结

**返回：**
```json
{
  "status": "conversation_ended",
  "conversation_id": "uuid",
  "summary": "对话总结",
  "message": "对话已结束"
}
```

### get_conversation_history

获取对话历史。

**参数：**
- `conversation_id` (str): 对话ID

**返回：**
```json
{
  "status": "success",
  "conversation_id": "uuid",
  "topic": "对话主题",
  "context": "上下文信息",
  "status": "active",
  "messages": [
    {
      "id": "uuid",
      "conversation_id": "uuid",
      "timestamp": "2025-01-12 10:00:00",
      "sender": "assistant",
      "content": "消息内容",
      "message_type": "question"
    }
  ],
  "total_messages": 5,
  "message": "找到 5 条对话消息"
}
```

### get_all_conversations

获取所有对话列表。

**参数：**
无

**返回：**
```json
{
  "status": "success",
  "conversations": [
    {
      "id": "uuid",
      "topic": "对话主题",
      "context": "上下文信息",
      "status": "active",
      "created_at": "2025-01-12 10:00:00",
      "updated_at": "2025-01-12 10:30:00",
      "message_count": 5
    }
  ],
  "total_count": 2,
  "active_count": 1,
  "message": "找到 2 个对话"
}
```

### save_conversations

保存所有对话到文件。

**参数：**
无

**返回：**
```json
{
  "status": "success",
  "output_file": "临时文件路径",
  "message": "对话已保存到: /path/to/file.json"
}
```

## 错误处理

所有工具都遵循统一的错误处理格式：

```json
{
  "status": "error",
  "message": "错误描述",
  "error_details": "详细错误信息"
}
```

常见错误状态：
- `error`: 操作失败
- `cancelled`: 用户取消
- `unavailable`: 依赖不可用
- `timeout`: 操作超时

## 使用示例

### 基础弹窗使用

```python
# 简单提问
result = ask_user_popup("你觉得这个功能怎么样？")
if result["status"] == "answered":
    print(f"用户回答: {result['answer']}")
```

### 持续对话使用

```python
# 开始对话
conv_id = start_conversation("项目讨论")

# 多轮对话
response = continue_conversation(conv_id, "你觉得这个设计怎么样？")
print(f"用户回复: {response['user_reply']}")

response = continue_conversation(conv_id, "有什么改进建议吗？")
print(f"用户回复: {response['user_reply']}")

# 结束对话
end_conversation(conv_id, "讨论完成")
```

### 错误处理

```python
result = ask_user_popup("测试问题")
if result["status"] == "error":
    print(f"错误: {result['message']}")
elif result["status"] == "cancelled":
    print("用户取消了回答")
```

## 配置选项

项目支持通过配置文件自定义行为：

```json
{
  "popup": {
    "width": 500,
    "height": 400,
    "theme": "modern",
    "auto_center": true
  },
  "conversation": {
    "max_messages": 100,
    "auto_save": true,
    "cleanup_days": 7
  }
}
```

配置文件位置：`~/.interactive_mcp_popup/config.json`
