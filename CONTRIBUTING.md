# Contributing to Interactive MCP Popup

感谢你对 Interactive MCP Popup 项目的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题

1. 搜索现有的 [Issues](https://github.com/your-username/interactive-mcp-popup/issues) 确保问题没有重复
2. 创建新的 Issue，使用清晰的标题和描述
3. 提供详细的重现步骤和环境信息
4. 添加相关的标签（bug、enhancement、question 等）

### 提交代码

1. **Fork** 项目到你的 GitHub 账户
2. **Clone** 你的 fork 到本地：
   ```bash
   git clone https://github.com/your-username/interactive-mcp-popup.git
   cd interactive-mcp-popup
   ```
3. **创建** 新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **进行** 你的更改
5. **测试** 你的更改：
   ```bash
   uv sync --dev
   uv run pytest
   ```
6. **提交** 你的更改：
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```
7. **推送** 到你的 fork：
   ```bash
   git push origin feature/your-feature-name
   ```
8. **创建** Pull Request

## 📋 开发环境设置

### 前置要求

- Python 3.11+
- uv (Python 包管理器)
- PySide6 (用于 GUI 功能)

### 安装开发依赖

```bash
# 克隆项目
git clone https://github.com/your-username/interactive-mcp-popup.git
cd interactive-mcp-popup

# 安装依赖
uv sync --dev

# 运行测试
uv run pytest
```

### 代码规范

我们使用以下工具来保持代码质量：

- **Black** - 代码格式化
- **isort** - 导入排序
- **ruff** - 代码检查
- **mypy** - 类型检查

```bash
# 格式化代码
uv run black src/
uv run isort src/

# 检查代码
uv run ruff check src/
uv run mypy src/
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试
uv run pytest tests/test_popup.py

# 运行测试并显示覆盖率
uv run pytest --cov=src tests/
```

### 手动测试

```bash
# 运行手动交互测试
uv run python tests/__init__.py --manual

# 运行功能演示
uv run python tests/__init__.py --demo
```

## 📝 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 示例

```bash
git commit -m "feat: 添加弹窗拖拽移动功能"
git commit -m "fix: 修复对话历史保存问题"
git commit -m "docs: 更新 API 文档"
```

## 🎯 开发指南

### 项目结构

```
interactive-mcp-popup/
├── src/interactive_mcp_popup/     # 主要源代码
├── docs/                         # 文档
├── examples/                     # 使用示例
├── tests/                        # 测试代码
├── pyproject.toml               # 项目配置
└── README.md                    # 项目说明
```

### 添加新功能

1. 在 `src/interactive_mcp_popup/` 中添加新代码
2. 在 `tests/` 中添加相应的测试
3. 更新 `docs/api.md` 中的 API 文档
4. 在 `examples/` 中添加使用示例

### 修复 Bug

1. 在 `tests/` 中添加重现 bug 的测试
2. 修复代码
3. 确保测试通过
4. 更新相关文档

## 📚 文档贡献

我们欢迎文档贡献：

- **API 文档** - 更新 `docs/api.md`
- **使用指南** - 更新 `docs/examples.md`
- **配置说明** - 更新 `docs/configuration.md`
- **README** - 更新项目说明

## 🏷️ 标签指南

### Issue 标签

- `bug` - 错误报告
- `enhancement` - 功能增强
- `question` - 问题咨询
- `documentation` - 文档相关
- `good first issue` - 适合新贡献者
- `help wanted` - 需要帮助

### PR 标签

- `ready for review` - 准备审查
- `work in progress` - 开发中
- `do not merge` - 不要合并
- `blocked` - 被阻塞

## 🎉 发布流程

1. 更新版本号（`pyproject.toml`）
2. 更新 `CHANGELOG.md`
3. 创建 Release Tag
4. 自动构建和发布

## 💬 社区

- [GitHub Discussions](https://github.com/your-username/interactive-mcp-popup/discussions) - 一般讨论
- [GitHub Issues](https://github.com/your-username/interactive-mcp-popup/issues) - 问题报告和功能请求

## 📄 许可证

通过贡献代码，你同意你的贡献将在 [MIT License](LICENSE) 下发布。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

如果你有任何问题，请随时通过 Issue 或 Discussion 联系我们。
