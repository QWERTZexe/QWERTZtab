from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

class GameButton(QPushButton):
    gameSelected = pyqtSignal(object)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.setFixedSize(180, 180)
        layout = QVBoxLayout(self)
        
        title_image = QLabel()
        pixmap = QPixmap(game.get_title_image()).scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        title_image.setPixmap(pixmap)
        layout.addWidget(title_image, alignment=Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.gameSelected.emit(self.game)
        event.accept()