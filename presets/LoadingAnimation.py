from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMovie

class LoadingAnimation(QWidget):
    def __init__(self, duration=5000):
        super().__init__()
        self.duration = duration
        self.initUI("presets/loading.gif")

    def initUI(self, gif_path):
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(self)

        self.movie_label = QLabel(self)
        self.movie = QMovie(gif_path)
        self.movie_label.setMovie(self.movie)
        self.movie.start()

        layout.addWidget(self.movie_label, alignment=Qt.AlignmentFlag.AlignCenter)
        loading_text = QLabel("Loading...")
        loading_text.setStyleSheet("color: white; font-size: 24px;")
        loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(loading_text)
        QTimer.singleShot(self.duration, self.finish_loading)

    def finish_loading(self):
        self.movie.stop()
        self.close()