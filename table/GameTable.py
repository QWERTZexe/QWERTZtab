from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor

from table.MonitorSelectionWindow import MonitorSelectionWindow
from gui.MainMenu import MainMenu

class GameTable(QWidget):
    def __init__(self):
        super().__init__()
        self.monitor_windows = []
        self.selected_screen = None
        self.initUI()

    def initUI(self):
        self.create_monitor_selection_windows()

    def create_monitor_selection_windows(self):
        for screen in QApplication.screens():
            window = MonitorSelectionWindow(screen, self.select_monitor)
            self.monitor_windows.append(window)
            window.show()

    def select_monitor(self, screen):
        self.selected_screen = screen
        for window in self.monitor_windows:
            window.close()
        self.monitor_windows.clear()
        self.show_fullscreen_game()

    def show_fullscreen_game(self):
        self.setGeometry(self.selected_screen.geometry())
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setStyleSheet("background-color: black;")

        # Create layout
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Create initial message label
        self.initial_message = QLabel(f"Game Table\nRunning on Screen: {self.selected_screen.name()}", self)
        self.initial_message.setStyleSheet("color: white; font-size: 48px;")
        self.initial_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.initial_message)

        # Create MainMenu widget (hidden initially)
        self.main_menu = MainMenu()
        self.main_menu.hide()
        layout.addWidget(self.main_menu)

        self.show()

        # Set up fade-out animation
        self.fade_animation = QPropertyAnimation(self.initial_message, b"color")
        self.fade_animation.setDuration(2000)  # 2 seconds
        self.fade_animation.setStartValue(QColor(255, 255, 255, 255))
        self.fade_animation.setEndValue(QColor(255, 255, 255, 0))
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.finished.connect(self.show_main_menu)

        # Start fade-out after 2 seconds
        QTimer.singleShot(2000, self.fade_animation.start)

    def show_main_menu(self):
        self.initial_message.hide()
        self.setStyleSheet("")  # Remove black background
        self.main_menu.show()