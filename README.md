# Interactive MCP Popup

一个现代化的 MCP (Model Context Protocol) 交互服务，支持 Qt 弹窗和持续对话功能。

## 特性

- 🎨 **现代化 Qt 弹窗** - 直接在 IDE 内显示，无需切换浏览器
- 💬 **持续对话** - 支持多轮对话直到用户选择结束
- 🌍 **跨平台支持** - 支持 Windows 和 macOS
- 🎯 **简洁设计** - 统一的现代化界面风格
- ⚡ **易于集成** - 简单的 MCP 配置

## 安装

### 前置要求

- Python 3.11+
- uv (Python 包管理器)

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/wangdefaf/interactive-mcp-popup.git
cd interactive-mcp-popup
```

2. 安装依赖
```bash
uv sync
```

3. 配置 MCP

在你的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "interactive-mcp-popup": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/interactive-mcp-popup",
        "run",
        "src/interactive_mcp_popup/server.py"
      ],
      "timeout": 600,
      "autoApprove": [
        "ask_user_popup",
        "start_conversation",
        "continue_conversation",
        "end_conversation",
        "get_conversation_history",
        "test_popup",
        "check_dependencies"
      ]
    }
  }
}
```

## 使用方法

### 配置规则
1. 在任何流程、任务、对话进行时，无论是询问、回复、或完成阶段性任务，皆必须调用 MCP interactive-mcp-popup。
2. 每当收到用户反馈，若反馈内容非空，必须再次调用 MCP interactive-mcp-popup，并根据反馈内容调整行为。
3. 仅当用户明确表示「结束」或「不再需要交互」时，才可停止调用 MCP interactive-mcp-popup，流程才算结束。
4. 除非收到结束指令，否则所有步骤都必须重复调用 MCP interactive-mcp-popup。
5. 完成任务前，必须使用 MCP interactive-mcp-popup 工具向用户询问反馈。

### 基础弹窗提问

```python
from interactive_mcp_popup import ask_user_popup

result = ask_user_popup(
    question="你觉得这个功能怎么样？",
    context="这是一个测试问题"
)
```

### 持续对话

```python
from interactive_mcp_popup import (
    start_conversation,
    continue_conversation,
    end_conversation
)

# 开始对话
conv_id = start_conversation("项目规划讨论")

# 继续对话
response = continue_conversation(conv_id, "你觉得这个设计怎么样？")

# 结束对话
end_conversation(conv_id, "讨论完成")
```

## 项目结构

```
interactive-mcp-popup/
├── src/
│   └── interactive_mcp_popup/
│       ├── __init__.py
│       ├── server.py          # 主 MCP 服务器
│       ├── popup.py            # Qt 弹窗实现
│       ├── conversation.py     # 持续对话管理
│       └── utils.py            # 工具函数
├── docs/
│   ├── api.md                 # API 文档
│   ├── configuration.md       # 配置说明
│   └── examples.md            # 使用示例
├── examples/
│   ├── basic_usage.py         # 基础使用示例
│   └── advanced_usage.py      # 高级使用示例
├── tests/
│   ├── test_popup.py          # 弹窗测试
│   └── test_conversation.py   # 对话测试
├── pyproject.toml             # 项目配置
├── README.md                  # 项目说明
├── LICENSE                    # MIT 许可证
└── .gitignore                 # Git 忽略文件
```

## API 参考

### 弹窗工具

- `ask_user_popup(question, context)` - 弹窗提问
- `test_popup()` - 测试弹窗功能
- `check_dependencies()` - 检查依赖

### 对话工具

- `start_conversation(topic, context)` - 开始对话
- `continue_conversation(conv_id, message)` - 继续对话
- `end_conversation(conv_id, summary)` - 结束对话
- `get_conversation_history(conv_id)` - 获取历史

## 开发

### 本地开发

```bash
# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run black src/
uv run isort src/
```

### 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

本项目思想借鉴了 [interactive-feedback-mcp](https://github.com/noopstudios/interactive-feedback-mcp) 项目，但代码完全独立实现。

## 支持

如果你遇到问题或有建议，请：

1. 查看 [文档](docs/)
2. 搜索 [Issues](https://github.com/wangdefaf/interactive-mcp-popup/issues)
3. 创建新的 Issue

---

**让 MCP 交互更简单、更直观！** 🚀
