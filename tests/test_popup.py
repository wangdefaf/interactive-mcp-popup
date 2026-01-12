#!/usr/bin/env python3
"""
弹窗功能测试

测试 Qt 弹窗的各种功能和边界情况。
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from typing import Optional

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from interactive_mcp_popup.popup import ModernPopupDialog, show_popup_dialog, save_result_to_file
    from PySide6.QtWidgets import QApplication
    PY_SIDE6_AVAILABLE = True
except ImportError:
    PY_SIDE6_AVAILABLE = False
    print("警告: PySide6 不可用，跳过弹窗测试")


class TestModernPopupDialog(unittest.TestCase):
    """测试现代弹窗对话框"""
    
    def setUp(self):
        """设置测试环境"""
        if not PY_SIDE6_AVAILABLE:
            self.skipTest("PySide6 不可用")
        
        # 创建 QApplication（如果不存在）
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
    
    def test_dialog_creation(self):
        """测试弹窗创建"""
        dialog = ModernPopupDialog(
            question="测试问题",
            context="测试上下文"
        )
        
        self.assertEqual(dialog.question, "测试问题")
        self.assertEqual(dialog.context, "测试上下文")
        self.assertIsNone(dialog.result)
    
    def test_dialog_ui_setup(self):
        """测试弹窗 UI 设置"""
        dialog = ModernPopupDialog("测试问题")
        
        # 检查窗口属性
        self.assertEqual(dialog.windowTitle(), "用户反馈")
        self.assertTrue(dialog.width() > 0)
        self.assertTrue(dialog.height() > 0)
        
        # 检查组件
        self.assertIsNotNone(dialog.input_field)
        self.assertIsNotNone(dialog.submit_button)
    
    def test_submit_answer(self):
        """测试提交回答"""
        dialog = ModernPopupDialog("测试问题")
        
        # 设置输入内容
        dialog.input_field.setText("测试回答")
        
        # 模拟点击提交按钮
        dialog.submit_answer()
        
        # 检查结果
        self.assertIsNotNone(dialog.result)
        self.assertEqual(dialog.result["answer"], "测试回答")
        self.assertEqual(dialog.result["status"], "answered")
    
    def test_submit_empty_answer(self):
        """测试提交空回答"""
        dialog = ModernPopupDialog("测试问题")
        
        # 不设置输入内容
        dialog.input_field.setText("")
        
        # 尝试提交
        dialog.submit_answer()
        
        # 检查结果（应该为 None，因为输入为空）
        self.assertIsNone(dialog.result)
    
    def test_dialog_with_context(self):
        """测试带上下文的弹窗"""
        context = "这是测试上下文"
        dialog = ModernPopupDialog("测试问题", context)
        
        self.assertEqual(dialog.context, context)
        
        # 检查上下文标签是否存在
        labels = dialog.findChildren(type(dialog).__subclasses__()[0])
        context_labels = [label for label in labels if "上下文" in label.text()]
        self.assertTrue(len(context_labels) > 0)


class TestPopupFunctions(unittest.TestCase):
    """测试弹窗函数"""
    
    def setUp(self):
        """设置测试环境"""
        if not PY_SIDE6_AVAILABLE:
            self.skipTest("PySide6 不可用")
        
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
    
    @patch('interactive_mcp_popup.popup.ModernPopupDialog.exec')
    def test_show_popup_dialog_success(self, mock_exec):
        """测试成功显示弹窗"""
        # 模拟用户点击确定
        mock_exec.return_value = 1  # QDialog.Accepted
        
        # 创建模拟的对话框
        mock_dialog = MagicMock()
        mock_dialog.get_result.return_value = {
            "question": "测试问题",
            "context": "测试上下文",
            "answer": "测试回答",
            "status": "answered"
        }
        
        with patch('interactive_mcp_popup.popup.ModernPopupDialog', return_value=mock_dialog):
            result = show_popup_dialog("测试问题", "测试上下文")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["answer"], "测试回答")
        self.assertEqual(result["status"], "answered")
    
    @patch('interactive_mcp_popup.popup.ModernPopupDialog.exec')
    def test_show_popup_dialog_cancelled(self, mock_exec):
        """测试用户取消弹窗"""
        # 模拟用户点击取消
        mock_exec.return_value = 0  # QDialog.Rejected
        
        mock_dialog = MagicMock()
        mock_dialog.get_result.return_value = None
        
        with patch('interactive_mcp_popup.popup.ModernPopupDialog', return_value=mock_dialog):
            result = show_popup_dialog("测试问题")
        
        self.assertIsNone(result)
    
    def test_save_result_to_file(self):
        """测试保存结果到文件"""
        result = {
            "question": "测试问题",
            "answer": "测试回答",
            "status": "answered"
        }
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            success = save_result_to_file(result, temp_file)
            self.assertTrue(success)
            
            # 验证文件内容
            import json
            with open(temp_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            self.assertEqual(saved_data, result)
        finally:
            # 清理临时文件
            os.unlink(temp_file)
    
    def test_save_result_to_file_error(self):
        """测试保存到无效路径"""
        result = {"test": "data"}
        invalid_path = "/invalid/path/that/does/not/exist/file.json"
        
        success = save_result_to_file(result, invalid_path)
        self.assertFalse(success)


class TestPopupIntegration(unittest.TestCase):
    """测试弹窗集成功能"""
    
    def setUp(self):
        """设置测试环境"""
        if not PY_SIDE6_AVAILABLE:
            self.skipTest("PySide6 不可用")
    
    def test_popup_workflow(self):
        """测试完整的弹窗工作流程"""
        # 这个测试需要实际的 GUI，在 CI 环境中可能跳过
        if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
            self.skipTest("跳过 GUI 测试在 CI 环境")
        
        # 测试实际弹窗（需要用户交互）
        print("这个测试需要用户交互，请手动测试")
        print("将显示一个测试弹窗，请输入回答并点击提交")
        
        result = show_popup_dialog(
            "这是一个集成测试，请输入任意文字并提交",
            "集成测试上下文"
        )
        
        if result:
            self.assertEqual(result["status"], "answered")
            self.assertIsInstance(result["answer"], str)
            self.assertTrue(len(result["answer"]) > 0)
        else:
            self.fail("用户取消了测试")


class TestPopupErrorHandling(unittest.TestCase):
    """测试弹窗错误处理"""
    
    def test_missing_py_side6(self):
        """测试缺少 PySide6 的错误处理"""
        # 模拟 PySide6 不可用的情况
        with patch.dict('sys.modules', {'PySide6': None}):
            with patch('interactive_mcp_popup.popup.PySide6', None):
                with self.assertRaises(ImportError):
                    from interactive_mcp_popup.popup import ModernPopupDialog


def run_manual_tests():
    """运行需要手动交互的测试"""
    if not PY_SIDE6_AVAILABLE:
        print("PySide6 不可用，无法运行手动测试")
        return
    
    print("🧪 手动测试模式")
    print("=" * 40)
    
    # 测试1: 基础弹窗
    print("\n测试1: 基础弹窗")
    result1 = show_popup_dialog(
        "这是一个基础测试弹窗",
        "请输入任意文字并点击提交"
    )
    print(f"结果: {result1}")
    
    # 测试2: 带上下文的弹窗
    print("\n测试2: 带上下文的弹窗")
    result2 = show_popup_dialog(
        "你觉得这个弹窗设计怎么样？",
        "我们正在测试弹窗的显示效果和用户交互体验"
    )
    print(f"结果: {result2}")
    
    # 测试3: 长文本弹窗
    print("\n测试3: 长文本弹窗")
    long_question = "这是一个很长的问题文本，用来测试弹窗在处理长文本时的显示效果。" * 3
    result3 = show_popup_dialog(long_question, "长文本测试")
    print(f"结果: {result3}")
    
    print("\n✅ 手动测试完成")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        run_manual_tests()
    else:
        unittest.main()
