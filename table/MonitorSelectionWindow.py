from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class MonitorSelectionWindow(QWidget):
    def __init__(self, screen, on_ok_callback):
        super().__init__()
        self.screen = screen
        self.on_ok_callback = on_ok_callback
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Monitor Selection')
        
        # Set window size and position
        window_width = 300
        window_height = 150
        screen_geometry = self.screen.geometry()
        x = (screen_geometry.width() - window_width) // 2 + screen_geometry.x()
        y = (screen_geometry.height() - window_height) // 2 + screen_geometry.y()
        self.setGeometry(x, y, window_width, window_height)
        
        layout = QVBoxLayout()
        
        label = QLabel(f'Use this screen?\n(Screen {self.screen.name()})', self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        ok_button = QPushButton('OK', self)
        ok_button.clicked.connect(self.on_ok_clicked)
        layout.addWidget(ok_button)
        
        self.setLayout(layout)

    def on_ok_clicked(self):
        self.on_ok_callback(self.screen)
