"""
Interactive MCP Popup

现代化的 MCP 交互服务，支持 Qt 弹窗和持续对话功能。
"""

__version__ = "0.1.0"
__author__ = "Interactive MCP Popup Team"
__email__ = "contact@example.com"

from .popup import ModernPopupDialog, show_popup_dialog
from .conversation import ConversationManager
from .server import mcp

__all__ = [
    "ModernPopupDialog",
    "show_popup_dialog", 
    "ConversationManager",
    "mcp",
]
