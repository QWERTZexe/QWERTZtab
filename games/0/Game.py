import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QPixmap, QColor

class QwertzJumpGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initGame()

    def initGame(self):
        self.bird_y = 200.0
        self.bird_velocity = 0.0
        self.gravity = 0.5
        self.jump_strength = -10
        self.pipe_x = 800.0
        self.pipe_gap = 200
        self.pipe_width = 80
        self.pipe_height = random.randint(100, 400)
        
        self.bird_pixmap = QPixmap("path/to/bird_texture.png")
        self.pipe_pixmap = QPixmap("path/to/pipe_texture.png")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)  # ~60 FPS

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), QColor(135, 206, 235))  # Sky blue background

        # Draw bird
        painter.drawPixmap(QRect(100, int(self.bird_y), 40, 40), self.bird_pixmap)

        # Draw pipes
        painter.drawPixmap(QRect(int(self.pipe_x), 0, self.pipe_width, self.pipe_height), self.pipe_pixmap)
        painter.drawPixmap(QRect(int(self.pipe_x), self.pipe_height + self.pipe_gap, self.pipe_width, self.height() - (self.pipe_height + self.pipe_gap)), self.pipe_pixmap)

    def update_game(self):
        # Update bird position
        self.bird_velocity += self.gravity
        self.bird_y += self.bird_velocity

        # Move pipe
        self.pipe_x -= 5
        if self.pipe_x < -self.pipe_width:
            self.pipe_x = 800
            self.pipe_height = random.randint(100, 400)

        # Check for collisions
        if self.check_collision():
            self.reset_game()

        self.update()

    def check_collision(self):
        bird_rect = QRect(100, int(self.bird_y), 40, 40)
        upper_pipe_rect = QRect(int(self.pipe_x), 0, self.pipe_width, self.pipe_height)
        lower_pipe_rect = QRect(int(self.pipe_x), self.pipe_height + self.pipe_gap, self.pipe_width, self.height() - (self.pipe_height + self.pipe_gap))

        return bird_rect.intersects(upper_pipe_rect) or bird_rect.intersects(lower_pipe_rect) or self.bird_y > self.height() or self.bird_y < 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.bird_velocity = self.jump_strength
            event.accept()  # Prevent event from propagating
        else:
            super().keyPressEvent(event)

    def reset_game(self):
        self.bird_y = 200.0
        self.bird_velocity = 0.0
        self.pipe_x = 800.0
        self.pipe_height = random.randint(100, 400)


class Game:
    def __init__(self):
        self.name = "QWERTZ Jump"
        self.description = "Jump through the pipes and avoid being hit by them!"
        self.thumbnail_path = "games/0/thumbnail.png"
        self.title_image_path = "games/0/title.png"

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_thumbnail(self):
        return self.thumbnail_path

    def get_title_image(self):
        return self.title_image_path

    def create_game_widget(self):
        return QwertzJumpGame()