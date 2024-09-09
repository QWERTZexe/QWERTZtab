import random
import subprocess
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtGui import QPainter, QPixmap, QColor, QFont
from games.QJ.Pipe import Pipe

from util.sound import play_sound, load_sound

class QWERTZJump(QWidget):
    def __init__(self):
        super().__init__()
        self.initGame()
        load_sound("score", "presets/score.wav")
    def initGame(self):
        self.bird_x = 100  # Fixed x-position of the bird
        self.bird_y = 200.0
        self.bird_velocity = 0.0
        self.gravity = 0.5
        self.jump_strength = -10
        self.pipes = []
        self.score = 0
        self.pipe_spacing = 400  # Space between pipes
        self.pipe_speed = 5  # Pixels per frame the pipes move
        self.distance_moved = 0  # Track total distance moved
        
        try:
            self.bird_pixmap = QPixmap("games/QJ/qwertz.png")
            self.pipe_pixmap = QPixmap("games/QJ/pipe.jpg")
            self.tunnel_pixmap = QPixmap("games/QJ/pipe.jpg")
            if self.bird_pixmap.isNull() or self.pipe_pixmap.isNull() or self.tunnel_pixmap.isNull():
                print("Failed to load textures")
        except Exception as e:
            print(f"Error loading textures: {e}")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(16)  # ~60 FPS

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.generate_pipes()

    def generate_pipes(self):
        self.pipes.clear()
        num_pipes = self.width() // self.pipe_spacing + 2  # Ensure we have enough pipes to fill the screen
        x = self.width()
        for _ in range(num_pipes):
            height = random.randint(50, self.height() - 150)  # Allow full height range
            gap = random.randint(150, 250)
            pipe_type = random.choice(['normal', 'triple', 'tunnel'])
            if pipe_type == 'tunnel':
                # Ensure the tunnel opening is a bit larger for easier passage
                gap = min(300, gap + 50)
            pipe = Pipe(x, height, gap, pipe_type)
            self.pipes.append(pipe)
            x += pipe.length + self.pipe_spacing

    def add_pipe(self):
        last_pipe = self.pipes[-1]
        x = last_pipe.x + last_pipe.length + self.pipe_spacing
        height = random.randint(50, self.height() - 150)  # Allow full height range
        gap = random.randint(150, 250)
        pipe_type = random.choice(['normal', 'triple', 'tunnel'])
        if pipe_type == 'tunnel':
            # Ensure the tunnel opening is a bit larger for easier passage
            gap = min(300, gap + 50)
        pipe = Pipe(x, height, gap, pipe_type)
        self.pipes.append(pipe)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw background
            painter.fillRect(self.rect(), QColor(135, 206, 235))  # Sky blue background

            # Draw pipes
            for pipe in self.pipes:
                x = pipe.x - self.distance_moved
                if pipe.type == 'normal':
                    painter.drawPixmap(QRect(x, 0, pipe.width, pipe.height), self.pipe_pixmap)
                    painter.drawPixmap(QRect(x, pipe.height + pipe.gap, pipe.width, self.height() - (pipe.height + pipe.gap)), self.pipe_pixmap)
                elif pipe.type == 'triple':
                    gap_height = (self.height() - 100) // 2  # Height of each gap
                    barrier_height = 50  # Height of the small barrier
                    
                    # Top pipe
                    painter.drawPixmap(QRect(x, 0, pipe.width, self.height() // 2 - gap_height // 2), self.pipe_pixmap)
                    # Middle barrier
                    painter.drawPixmap(QRect(x, self.height() // 2 - barrier_height // 2, pipe.width, barrier_height), self.pipe_pixmap)
                    # Bottom pipe
                    painter.drawPixmap(QRect(x, self.height() // 2 + gap_height // 2 + barrier_height // 2, pipe.width, self.height() // 2 - gap_height // 2), self.pipe_pixmap)
                elif pipe.type == 'tunnel':
                    painter.drawPixmap(QRect(x, 0, pipe.length, pipe.height), self.tunnel_pixmap)
                    painter.drawPixmap(QRect(x, pipe.height + pipe.gap, pipe.length, self.height() - (pipe.height + pipe.gap)), self.tunnel_pixmap)

            # Draw bird
            painter.drawPixmap(QRect(self.bird_x, int(self.bird_y), 40, 40), self.bird_pixmap)

            # Draw score
            painter.setFont(QFont('Arial', 24))
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.score))

        except Exception as e:
            print(f"Error in paintEvent: {e}")

    def update_game(self):
        try:
            # Update bird position
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity

            # Move pipes
            self.distance_moved += self.pipe_speed

            # Check for pipe passing and removal
            for pipe in self.pipes[:]:
                if pipe.x - self.distance_moved + pipe.length < 0:
                    self.pipes.remove(pipe)
                    self.add_pipe()
                elif not pipe.passed and pipe.x - self.distance_moved + pipe.length < self.bird_x:
                    pipe.passed = True
                    self.score += 1
                    # Sound Effect by <a href="https://pixabay.com/users/driken5482-45721595/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=236671">Driken Stan</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=236671">Pixabay</a>
                    play_sound("score")
            # Check for collisions
            if self.check_collision():
                self.reset_game()

            self.update()
        except Exception as e:
            print(f"Error in update_game: {e}")

    def check_collision(self):
        bird_rect = QRect(self.bird_x, int(self.bird_y), 40, 40)
        for pipe in self.pipes:
            x = pipe.x - self.distance_moved
            if pipe.type == 'normal' or pipe.type == 'tunnel':
                upper_pipe_rect = QRect(x, 0, pipe.length, pipe.height)
                lower_pipe_rect = QRect(x, pipe.height + pipe.gap, pipe.length, self.height() - (pipe.height + pipe.gap))
                if bird_rect.intersects(upper_pipe_rect) or bird_rect.intersects(lower_pipe_rect):
                    return True
            elif pipe.type == 'triple':
                gap_height = (self.height() - 100) // 2
                barrier_height = 50
                top_pipe_rect = QRect(x, 0, pipe.width, self.height() // 2 - gap_height // 2)
                middle_barrier_rect = QRect(x, self.height() // 2 - barrier_height // 2, pipe.width, barrier_height)
                bottom_pipe_rect = QRect(x, self.height() // 2 + gap_height // 2 + barrier_height // 2, pipe.width, self.height() // 2 - gap_height // 2)
                if bird_rect.intersects(top_pipe_rect) or bird_rect.intersects(middle_barrier_rect) or bird_rect.intersects(bottom_pipe_rect):
                    return True
        return self.bird_y > self.height() or self.bird_y < 0

    def reset_game(self):
        self.bird_y = 200.0
        self.bird_velocity = 0.0
        self.score = 0
        self.distance_moved = 0
        self.generate_pipes()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.bird_velocity = self.jump_strength
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        event.accept()  # Prevent the event from propagating