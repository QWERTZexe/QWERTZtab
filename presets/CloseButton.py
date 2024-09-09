from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

class CloseButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # <a href="https://www.flaticon.com/free-icons/close" title="close icons">Close icons created by Pixel perfect - Flaticon</a>
        self.setIcon(QIcon('presets/close.png'))
        self.setIconSize(QSize(40, 40))
        self.setFixedSize(50, 50)
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 120);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 180);
            }
        """)