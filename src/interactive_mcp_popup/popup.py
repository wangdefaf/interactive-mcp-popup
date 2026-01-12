"""
现代化 Qt 弹窗对话框模块

提供简洁美观的弹窗界面，支持问题文本、上下文和用户输入。
"""

import sys
import json
import tempfile
import os
from typing import Dict, Optional, Any

try:
    from PySide6.QtWidgets import (
        QApplication, QDialog, QVBoxLayout, QLabel, 
        QTextEdit, QPushButton, QWidget, QFrame
    )
    from PySide6.QtCore import Qt, QTimer, QPoint, QSize, QRect
    from PySide6.QtGui import QFont, QPalette, QColor, QCursor, QMouseEvent
except ImportError as e:
    raise ImportError(f"PySide6 is required: {e}")


class ModernPopupDialog(QDialog):
    """现代化的弹窗对话框 - 支持移动和调整大小"""
    
    def __init__(self, question: str, context: str = "", parent=None):
        super().__init__(parent)
        self.question = question
        self.context = context
        self.result = None
        
        # 拖拽相关变量
        self._drag_position = None
        self._resize_edges = None
        self._edge_margin = 8  # 边缘检测范围
        
        # 窗口设置
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint)
        self.setFixedSize(600, 500)  # 默认大小
        self.setMinimumSize(400, 300)  # 最小大小
        self.setMaximumSize(1200, 800)  # 最大大小
        
        # 设置鼠标追踪
        self.setMouseTracking(True)
        
        self.setup_ui()
        self.setup_style()
        self.load_window_settings()
        
    def load_window_settings(self):
        """加载窗口设置"""
        try:
            import json
            settings_file = os.path.join(tempfile.gettempdir(), "popup_settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # 恢复窗口大小和位置
                if "geometry" in settings:
                    self.restoreGeometry(settings["geometry"])
        except:
            pass  # 如果加载失败，使用默认设置
    
    def save_window_settings(self):
        """保存窗口设置"""
        try:
            import json
            settings_file = os.path.join(tempfile.gettempdir(), "popup_settings.json")
            settings = {
                "geometry": self.saveGeometry().data()
            }
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False)
        except:
            pass  # 忽略保存错误
        
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle("用户反馈")
        # 移除固定大小设置，允许调整
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint)
        
        # 主布局
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 问题文本
        question_label = QLabel("问题:")
        question_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(question_label)
        
        # 显示问题内容
        question_text = QLabel(self.question)
        question_text.setWordWrap(True)
        question_text.setFont(QFont("Arial", 10))
        layout.addWidget(question_text)
        
        # 如果有上下文，显示上下文
        if self.context:
            context_label = QLabel("上下文:")
            context_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            layout.addWidget(context_label)
            
            context_text = QLabel(self.context)
            context_text.setWordWrap(True)
            context_text.setFont(QFont("Arial", 9))
            layout.addWidget(context_text)
        
        # 输入框
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("请输入你的回答...")
        self.input_field.setMinimumHeight(100)
        layout.addWidget(self.input_field)
        
        # 提交按钮
        self.submit_button = QPushButton("提交回答")
        self.submit_button.setMinimumHeight(40)
        self.submit_button.clicked.connect(self.submit_answer)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)
        
        # 聚焦到输入框
        QTimer.singleShot(100, self.input_field.setFocus)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self._resize_edges = self._get_resize_edges(event.position().toPoint())
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self._resize_edges:
                # 调整大小
                self._resize_window(event.globalPosition().toPoint())
            elif self._drag_position:
                # 移动窗口
                new_pos = event.globalPosition().toPoint() - self._drag_position
                self.move(new_pos)
            event.accept()
        else:
            # 更新鼠标光标
            edges = self._get_resize_edges(event.position().toPoint())
            self._update_cursor(edges)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = None
            self._resize_edges = None
            self.save_window_settings()
            event.accept()
    
    def _get_resize_edges(self, pos: QPoint) -> Optional[str]:
        """获取调整大小的边缘"""
        rect = self.rect()
        edges = []
        
        # 检查各个边缘
        if pos.x() <= self._edge_margin:
            edges.append("left")
        elif pos.x() >= rect.width() - self._edge_margin:
            edges.append("right")
        
        if pos.y() <= self._edge_margin:
            edges.append("top")
        elif pos.y() >= rect.height() - self._edge_margin:
            edges.append("bottom")
        
        return "_".join(edges) if edges else None
    
    def _update_cursor(self, edges: Optional[str]):
        """更新鼠标光标"""
        if not edges:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        elif edges in ["left", "right"]:
            self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        elif edges in ["top", "bottom"]:
            self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        elif edges in ["left_top", "right_bottom"]:
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        elif edges in ["right_top", "left_bottom"]:
            self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        else:
            self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))
    
    def _resize_window(self, global_pos: QPoint):
        """调整窗口大小"""
        if not self._resize_edges:
            return
        
        rect = self.frameGeometry()
        new_rect = QRect(rect)
        
        edges = self._resize_edges.split("_")
        
        if "left" in edges:
            new_rect.setLeft(global_pos.x())
        if "right" in edges:
            new_rect.setRight(global_pos.x())
        if "top" in edges:
            new_rect.setTop(global_pos.y())
        if "bottom" in edges:
            new_rect.setBottom(global_pos.y())
        
        # 检查最小和最大大小
        min_size = self.minimumSize()
        max_size = self.maximumSize()
        
        if new_rect.width() >= min_size.width() and new_rect.height() >= min_size.height():
            if new_rect.width() <= max_size.width() and new_rect.height() <= max_size.height():
                self.setGeometry(new_rect)
        
    def setup_style(self):
        """设置现代化样式"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 12px;
            }
            QLabel {
                color: #2c3e50;
                background-color: transparent;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                padding: 12px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
    def submit_answer(self):
        """提交回答"""
        answer = self.input_field.toPlainText().strip()
        if answer:
            self.result = {
                "question": self.question,
                "context": self.context,
                "answer": answer,
                "status": "answered"
            }
            self.accept()
        else:
            # 如果没有输入，不关闭窗口
            pass
    
    def get_result(self) -> Optional[Dict[str, Any]]:
        """获取结果"""
        return self.result


def show_popup_dialog(question: str, context: str = "") -> Optional[Dict[str, Any]]:
    """显示弹窗对话框
    
    Args:
        question: 要问用户的问题
        context: 上下文信息（可选）
        
    Returns:
        包含用户回答的字典，如果用户取消则返回 None
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    dialog = ModernPopupDialog(question, context)
    
    # 居中显示
    if dialog.parent():
        dialog.setParent(dialog.parent(), Qt.WindowType.Dialog)
    else:
        screen = app.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = (geometry.width() - dialog.width()) // 2
            y = (geometry.height() - dialog.height()) // 2
            dialog.move(x, y)
    
    result = dialog.exec()
    
    if result == QDialog.Accepted:
        return dialog.get_result()
    else:
        return None


def save_result_to_file(result: Dict[str, Any], output_file: str) -> bool:
    """保存结果到文件
    
    Args:
        result: 要保存的结果字典
        output_file: 输出文件路径
        
    Returns:
        保存是否成功
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存结果失败: {e}")
        return False


def test_popup():
    """测试弹窗功能"""
    result = show_popup_dialog(
        "这是一个测试问题，你觉得这个弹窗设计怎么样？",
        "这是测试上下文，用来验证弹窗的显示效果。"
    )
    
    if result:
        print("用户回答:", result["answer"])
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            output_file = f.name
        
        if save_result_to_file(result, output_file):
            print(f"结果已保存到: {output_file}")
        
        return result
    else:
        print("用户取消了回答")
        return None


if __name__ == "__main__":
    test_popup()
