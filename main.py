import sys
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QTextEdit, QPushButton, QLabel,
                               QMessageBox, QProgressBar, QSplitter)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QColor


class SortingThread(QThread):
    """排序线程，防止界面卡顿"""
    finished = Signal(str)
    progress = Signal(int)

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        self.progress.emit(50)
        sorted_text = sort_adguard_rules(self.text)
        self.progress.emit(100)
        self.finished.emit(sorted_text)


def get_adguard_sort_key(rule):
    """
    为Adguard规则生成排序键
    忽略*, ||, @@, ! 等特殊字符，从实际内容开始排序
    """
    if not rule:
        return ""

    # 注释行保持原样排序
    if rule.startswith('!'):
        return rule.lower()

    # 处理各种Adguard前缀
    sort_key = rule

    # 移除常见前缀，但不改变原始规则
    prefixes = [r'^\*+', r'^\|\|', r'^@@\|\|', r'^@@']
    for prefix in prefixes:
        match = re.match(prefix, rule)
        if match:
            sort_key = rule[match.end():]
            break

    return sort_key.lower()


def sort_adguard_rules(text):
    """
    智能排序Adguard拦截规则
    正确处理Adguard语法，保持特殊字符不变
    """
    # 按行分割并过滤空行
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # 如果没有内容，返回空字符串
    if not lines:
        return ""

    # 直接对所有行进行排序，使用Adguard专用的排序键
    sorted_lines = sorted(lines, key=get_adguard_sort_key)

    return '\n'.join(sorted_lines)


class AdguardSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Adguard 规则排序器 🐋")
        self.setGeometry(100, 100, 900, 700)

        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
            QLabel {
                color: #ffffff;
                padding: 5px;
            }
            QProgressBar {
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0d6efd;
                border-radius: 4px;
            }
        """)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel("Adguard 规则智能排序工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # 创建分割器
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)

        # 输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        input_label = QLabel("输入规则:")
        input_layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "请在此处粘贴您的 Adguard 规则...\n例如：\n*sohu.com###ad\n||example.com##.banner\n! 注释行")
        input_layout.addWidget(self.input_text)

        # 输出区域
        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)

        output_label = QLabel("排序结果:")
        output_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("排序后的规则将显示在这里...")
        output_layout.addWidget(self.output_text)

        # 添加到分割器
        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        splitter.setSizes([350, 350])

        # 按钮区域
        button_layout = QHBoxLayout()

        self.sort_btn = QPushButton("开始排序")
        self.sort_btn.clicked.connect(self.start_sorting)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_text)

        self.copy_btn = QPushButton("复制结果")
        self.copy_btn.clicked.connect(self.copy_result)

        button_layout.addWidget(self.sort_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.copy_btn)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("就绪")
        layout.addWidget(self.status_label)

        # 初始化排序线程
        self.sorting_thread = None

    def start_sorting(self):
        """开始排序"""
        input_text = self.input_text.toPlainText().strip()

        if not input_text:
            QMessageBox.warning(self, "警告", "请输入要排序的规则！")
            return

        # 禁用按钮，显示进度条
        self.set_ui_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在排序...")

        # 创建并启动排序线程
        self.sorting_thread = SortingThread(input_text)
        self.sorting_thread.progress.connect(self.progress_bar.setValue)
        self.sorting_thread.finished.connect(self.sorting_finished)
        self.sorting_thread.start()

    def sorting_finished(self, sorted_text):
        """排序完成"""
        self.output_text.setPlainText(sorted_text)
        self.set_ui_enabled(True)
        self.progress_bar.setVisible(False)

        # 统计信息
        input_lines = len([line for line in self.input_text.toPlainText().split('\n') if line.strip()])
        output_lines = len([line for line in sorted_text.split('\n') if line.strip()])

        self.status_label.setText(f"排序完成！输入: {input_lines} 行, 输出: {output_lines} 行")

        # 显示完成消息
        QMessageBox.information(self, "完成", "规则排序完成！")

    def clear_text(self):
        """清空文本"""
        self.input_text.clear()
        self.output_text.clear()
        self.status_label.setText("已清空")

    def copy_result(self):
        """复制结果到剪贴板"""
        result_text = self.output_text.toPlainText()
        if result_text:
            QApplication.clipboard().setText(result_text)
            self.status_label.setText("结果已复制到剪贴板")
        else:
            QMessageBox.warning(self, "警告", "没有可复制的内容！")

    def set_ui_enabled(self, enabled):
        """设置UI启用状态"""
        self.sort_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.copy_btn.setEnabled(enabled)
        self.input_text.setEnabled(enabled)


def main():
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("Adguard Rule Sorter")
    app.setApplicationVersion("1.0")

    window = AdguardSorterApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()