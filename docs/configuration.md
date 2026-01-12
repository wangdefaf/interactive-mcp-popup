# 配置说明

## MCP 配置

在你的 MCP 配置文件中添加以下配置：

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
        "get_all_conversations",
        "test_popup",
        "check_dependencies",
        "save_conversations"
      ]
    }
  }
}
```

### 配置参数说明

- `command`: 启动命令，使用 `uv`
- `args`: 启动参数
  - `--directory`: 项目目录路径
  - `run`: 运行命令
  - `src/interactive_mcp_popup/server.py`: 主服务器文件
- `timeout`: 超时时间（秒）
- `autoApprove`: 自动批准的工具列表

## 项目配置

### 弹窗配置

弹窗行为可以通过配置文件自定义：

```json
{
  "popup": {
    "width": 500,
    "height": 400,
    "theme": "modern",
    "auto_center": true,
    "font_family": "Arial",
    "font_size": 10
  }
}
```

**参数说明：**
- `width`: 弹窗宽度（像素）
- `height`: 弹窗高度（像素）
- `theme`: 主题风格（"modern", "classic", "minimal"）
- `auto_center`: 是否自动居中显示
- `font_family`: 字体族
- `font_size`: 字体大小

### 对话配置

```json
{
  "conversation": {
    "max_messages": 100,
    "auto_save": true,
    "cleanup_days": 7,
    "default_context": "",
    "enable_history": true
  }
}
```

**参数说明：**
- `max_messages`: 每个对话的最大消息数
- `auto_save`: 是否自动保存对话
- `cleanup_days`: 自动清理天数
- `default_context`: 默认上下文
- `enable_history`: 是否启用历史记录

### 通用配置

```json
{
  "logging": {
    "level": "ERROR",
    "file": null,
    "max_size": "10MB",
    "backup_count": 5
  },
  "temp": {
    "cleanup_hours": 24,
    "max_files": 100
  }
}
```

**参数说明：**
- `logging.level`: 日志级别（DEBUG, INFO, WARNING, ERROR）
- `logging.file`: 日志文件路径（null 表示不写入文件）
- `logging.max_size`: 日志文件最大大小
- `logging.backup_count`: 备份文件数量
- `temp.cleanup_hours`: 临时文件清理时间（小时）
- `temp.max_files`: 最大临时文件数量

## 配置文件位置

### 用户配置

用户配置文件位置：`~/.interactive_mcp_popup/config.json`

### 项目配置

项目配置文件位置：`<project_root>/config.json`

### 环境变量

支持通过环境变量覆盖配置：

```bash
export INTERACTIVE_MCP_POPUP_WIDTH=600
export INTERACTIVE_MCP_POPUP_HEIGHT=500
export INTERACTIVE_MCP_POPUP_THEME=modern
```

## 环境配置

### 开发环境

开发环境的额外配置：

```json
{
  "development": {
    "debug_mode": true,
    "test_mode": false,
    "mock_popup": false,
    "auto_reload": true
  }
}
```

### 生产环境

生产环境的优化配置：

```json
{
  "production": {
    "debug_mode": false,
    "test_mode": false,
    "mock_popup": false,
    "auto_reload": false,
    "performance_mode": true
  }
}
```

## 平台特定配置

### Windows

```json
{
  "platform": {
    "windows": {
      "font_family": "Microsoft YaHei",
      "dpi_aware": true,
      "native_dialogs": true
    }
  }
}
```

### macOS

```json
{
  "platform": {
    "macos": {
      "font_family": "Helvetica Neue",
      "native_dialogs": true,
      "touch_bar": false
    }
  }
}
```

### Linux

```json
{
  "platform": {
    "linux": {
      "font_family": "DejaVu Sans",
      "native_dialogs": false,
      "gtk_theme": "Adwaita"
    }
  }
}
```

## 配置验证

使用 `check_dependencies` 工具验证配置：

```python
result = check_dependencies()
if result["status"] == "available":
    print("配置正确，依赖可用")
else:
    print("配置有问题，请检查依赖")
```

## 故障排除

### 常见配置问题

1. **弹窗不显示**
   - 检查 PySide6 是否安装
   - 确认显示环境支持 GUI

2. **对话丢失**
   - 检查 `auto_save` 配置
   - 确认临时文件权限

3. **性能问题**
   - 调整 `max_messages` 限制
   - 启用 `cleanup_days` 自动清理

4. **样式问题**
   - 检查平台特定配置
   - 确认字体可用性

### 配置重置

重置配置到默认值：

```bash
rm ~/.interactive_mcp_popup/config.json
```

下次启动时会自动创建默认配置。

## 高级配置

### 自定义主题

```json
{
  "themes": {
    "custom": {
      "background_color": "#f0f0f0",
      "text_color": "#333333",
      "border_color": "#cccccc",
      "button_color": "#007acc",
      "button_hover_color": "#005a9e"
    }
  }
}
```

### 插件配置

```json
{
  "plugins": {
    "enabled": ["emoji", "markdown", "syntax_highlight"],
    "emoji": {
      "enabled": true,
      "set": "default"
    },
    "markdown": {
      "enabled": true,
      "render_links": true
    }
  }
}
```

## 配置模板

### 最小配置

```json
{
  "popup": {
    "width": 500,
    "height": 400
  }
}
```

### 完整配置

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
  },
  "logging": {
    "level": "ERROR"
  },
  "temp": {
    "cleanup_hours": 24
  }
}
```
