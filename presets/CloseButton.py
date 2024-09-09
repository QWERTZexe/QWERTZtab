from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

class CloseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setIcon(QIcon('path/to/close_icon.png'))  # Replace with path to your close icon
        self.setIconSize(QSize(32, 32))
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """)