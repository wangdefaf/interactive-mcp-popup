"""
工具函数模块

提供通用的辅助函数和工具类。
"""

import os
import sys
import json
import tempfile
from typing import Dict, Any, Optional, List
from pathlib import Path


def get_temp_dir() -> Path:
    """获取临时目录
    
    Returns:
        临时目录路径
    """
    return Path(tempfile.gettempdir()) / "interactive_mcp_popup"


def ensure_temp_dir() -> Path:
    """确保临时目录存在
    
    Returns:
        临时目录路径
    """
    temp_dir = get_temp_dir()
    temp_dir.mkdir(exist_ok=True)
    return temp_dir


def save_json(data: Dict[str, Any], filename: str) -> Optional[str]:
    """保存数据到 JSON 文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
        
    Returns:
        文件路径，如果失败则返回 None
    """
    try:
        temp_dir = ensure_temp_dir()
        file_path = temp_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(file_path)
    except Exception as e:
        print(f"保存 JSON 失败: {e}")
        return None


def load_json(file_path: str) -> Optional[Dict[str, Any]]:
    """从 JSON 文件加载数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        加载的数据，如果失败则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载 JSON 失败: {e}")
        return None


def format_timestamp(timestamp: str) -> str:
    """格式化时间戳
    
    Args:
        timestamp: 时间戳字符串
        
    Returns:
        格式化后的时间字符串
    """
    try:
        from datetime import datetime
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return timestamp


def truncate_text(text: str, max_length: int = 100) -> str:
    """截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def validate_conversation_id(conversation_id: str) -> bool:
    """验证对话ID格式
    
    Args:
        conversation_id: 对话ID
        
    Returns:
        是否有效
    """
    try:
        import uuid
        uuid.UUID(conversation_id)
        return True
    except:
        return False


def get_project_root() -> Path:
    """获取项目根目录
    
    Returns:
        项目根目录路径
    """
    current = Path(__file__).parent
    while current.parent != current:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return current


def get_config_path() -> Path:
    """获取配置文件路径
    
    Returns:
        配置文件路径
    """
    config_dir = Path.home() / ".interactive_mcp_popup"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config() -> Dict[str, Any]:
    """加载配置
    
    Returns:
        配置字典
    """
    config_path = get_config_path()
    if config_path.exists():
        return load_json(str(config_path)) or {}
    return {}


def save_config(config: Dict[str, Any]) -> bool:
    """保存配置
    
    Args:
        config: 配置字典
        
    Returns:
        是否成功
    """
    config_path = get_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def cleanup_temp_files(max_age_hours: int = 24) -> int:
    """清理临时文件
    
    Args:
        max_age_hours: 最大保留时间（小时）
        
    Returns:
        清理的文件数量
    """
    import time
    from datetime import datetime, timedelta
    
    temp_dir = get_temp_dir()
    if not temp_dir.exists():
        return 0
    
    cleaned_count = 0
    cutoff_time = time.time() - (max_age_hours * 3600)
    
    for file_path in temp_dir.glob("*.json"):
        if file_path.stat().st_mtime < cutoff_time:
            try:
                file_path.unlink()
                cleaned_count += 1
            except:
                pass
    
    return cleaned_count


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.config = load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值"""
        self.config[key] = value
        save_config(self.config)
    
    def get_popup_config(self) -> Dict[str, Any]:
        """获取弹窗配置"""
        return self.get("popup", {
            "width": 500,
            "height": 400,
            "theme": "modern",
            "auto_center": True
        })
    
    def get_conversation_config(self) -> Dict[str, Any]:
        """获取对话配置"""
        return self.get("conversation", {
            "max_messages": 100,
            "auto_save": True,
            "cleanup_days": 7
        })


# 全局配置管理器
config_manager = ConfigManager()


if __name__ == "__main__":
    # 测试工具函数
    print("临时目录:", get_temp_dir())
    print("项目根目录:", get_project_root())
    print("配置文件路径:", get_config_path())
    
    # 测试配置管理器
    config_manager.set("test", "value")
    print("测试配置:", config_manager.get("test"))
    
    # 测试清理
    cleaned = cleanup_temp_files()
    print(f"清理了 {cleaned} 个临时文件")
