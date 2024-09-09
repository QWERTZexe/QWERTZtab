from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont

from presets.LoadingAnimation import LoadingAnimation
from presets.CloseButton import CloseButton

class GameScreen(QWidget):
    def __init__(self, game, main_menu):
        super().__init__()
        self.game = game
        self.main_menu = main_menu
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")
        self.layout = QVBoxLayout(self)
        
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Loading screen
        self.loading_screen = LoadingAnimation(5000)
        self.stacked_widget.addWidget(self.loading_screen)

        # Game widget
        self.game_widget = self.game.create_game_widget()
        self.stacked_widget.addWidget(self.game_widget)

        # Close button
        self.close_button = CloseButton(self)
        self.close_button.clicked.connect(self.return_to_main_menu)
        self.close_button.hide()

        # Start with loading screen
        self.stacked_widget.setCurrentWidget(self.loading_screen)
        QTimer.singleShot(5000, self.show_game)

    def show_game(self):
        self.stacked_widget.setCurrentWidget(self.game_widget)
        self.close_button.show()

    def return_to_main_menu(self):
        self.main_menu.show()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.return_to_main_menu()

# ... (rest of the file remains the same)

class BasicGameWidget(QWidget):
    def __init__(self, game_name):
        super().__init__()
        self.game_name = game_name
        self.x = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw game name
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont('Arial', 24))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, f"Playing: {self.game_name}")

        # Draw moving rectangle
        painter.setBrush(QColor(0, 255, 0))
        painter.drawRect(self.x, self.height() // 2, 50, 50)

    def update(self):
        self.x = (self.x + 5) % self.width()
        super().update()