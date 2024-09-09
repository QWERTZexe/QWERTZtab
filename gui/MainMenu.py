import os
import importlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from gui.SmoothScrollArea import SmoothScrollArea
from gui.GameButton import GameButton
from gui.GameScreen import GameScreen

from util.sound import load_sound, play_sound

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.games = self.load_games()
        self.current_game = None
        self.initUI()
        load_sound("game_select", "presets/select.wav")

    def load_games(self):
        games = []
        games_dir = 'games'
        for game_folder in os.listdir(games_dir):
            if os.path.isdir(os.path.join(games_dir, game_folder)):
                module = importlib.import_module(f'games.{game_folder}.Game')
                game = module.Game()
                games.append(game)
        return games
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Banner
        banner = QLabel("QWERTZ Table")
        banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner.setStyleSheet("font-size: 36px; font-weight: bold; color: #2c3e50; background-color: #ecf0f1;")
        banner.setFixedHeight(60)
        main_layout.addWidget(banner)

        # Game description and thumbnail
        self.game_info = QWidget()
        game_info_layout = QVBoxLayout(self.game_info)
        game_info_layout.setSpacing(10)  # Add some spacing between elements
        game_info_layout.setContentsMargins(20, 20, 20, 20)  # Add margins around the game info
        
        self.game_name = QLabel("Select a game")
        self.game_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.game_name.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        self.game_name.setFixedHeight(40)  # Set a fixed height for the game name
        game_info_layout.addWidget(self.game_name)

        thumbnail_and_description = QHBoxLayout()
        
        self.game_thumbnail = QLabel()
        self.game_thumbnail.setFixedSize(640, 360)  # Increased size
        self.game_thumbnail.setStyleSheet("background-color: #bdc3c7; border-radius: 10px;")
        thumbnail_and_description.addWidget(self.game_thumbnail)
        
        self.game_description = QLabel("Select a game to see its description")
        self.game_description.setWordWrap(True)
        self.game_description.setStyleSheet("font-size: 20px; color: #34495e; padding: 20px;")  # Increased font size
        thumbnail_and_description.addWidget(self.game_description)
        
        game_info_layout.addLayout(thumbnail_and_description, 10)
        main_layout.addWidget(self.game_info, 1)

        # Add spacing between game info and carousel
        main_layout.addSpacing(20)

        # Game carousel
        self.carousel = SmoothScrollArea()
        self.carousel.setStyleSheet("background-color: #3498db;")
        
        carousel_content = QWidget()
        carousel_layout = QHBoxLayout(carousel_content)
        carousel_layout.setSpacing(20)
        carousel_layout.setContentsMargins(10, 10, 10, 10)
        
        for game in self.games:
            game_button = GameButton(game)
            game_button.gameSelected.connect(self.update_game_info)
            carousel_layout.addWidget(game_button)
        
        self.carousel.setWidget(carousel_content)
        self.carousel.setFixedHeight(200)
        main_layout.addWidget(self.carousel)

        # Enable smooth scrolling for the carousel and all its child widgets
        self.carousel.installEventFilter(self.carousel)
        carousel_content.installEventFilter(self.carousel)
        for i in range(carousel_layout.count()):
            widget = carousel_layout.itemAt(i).widget()
            if widget is not None:
                widget.installEventFilter(self.carousel)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        # Add Start Button (initially hidden)
        self.start_button = QPushButton("Start Game")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        self.start_button.hide()
        game_info_layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)


    def update_game_info(self, game):
        self.current_game = game
        self.game_name.setText(game.get_name())
        self.game_thumbnail.setPixmap(QPixmap(game.get_thumbnail()).scaled(640, 360, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.game_description.setText(game.get_description())
        self.start_button.show()
        play_sound("game_select")
    def start_game(self):
        if self.current_game:
            self.game_screen = GameScreen(self.current_game, self)
            self.game_screen.showFullScreen()
            self.hide()

    def showEvent(self, event):
        super().showEvent(event)
        # Refresh the carousel when the main menu is shown again
        if hasattr(self, 'carousel'):
            self.carousel.setWidget(self.carousel.widget())