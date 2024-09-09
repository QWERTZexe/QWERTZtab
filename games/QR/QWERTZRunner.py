import random
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QPainter, QColor, QBrush, QPixmap, QFont

class QWERTZRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.initGame()

    def initGame(self):
        self.player_x = 100
        self.player_size = 40
        self.player_velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.game_speed = 5
        self.score = 0
        self.obstacles = []
        self.game_started = False

        # Set ground level near the bottom of the screen
        self.ground_y = self.height() - 50 if self.height() > 0 else 550
        self.player_y = self.ground_y - self.player_size

        # Load textures
        self.player_texture = QPixmap("games/QR/player.png")
        self.spike_texture = QPixmap("games/QR/spike.png")
        if self.player_texture.isNull() or self.spike_texture.isNull():
            print("Failed to load textures")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(16)  # ~60 FPS

    def updateGame(self):
        if not self.game_started:
            return

        # Update player position
        self.player_velocity += self.gravity
        self.player_y += self.player_velocity

        # Keep player above ground
        if int(self.player_y) > self.ground_y - self.player_size:
            self.player_y = self.ground_y - self.player_size
            self.player_velocity = 0

        # Move obstacles
        for obstacle in self.obstacles:
            obstacle['x'] -= self.game_speed

        # Remove off-screen obstacles
        self.obstacles = [obs for obs in self.obstacles if obs['x'] > -50]

        # Spawn new obstacles
        if random.randint(1, 100) == 1:  # Adjust spawn rate as needed
            self.spawnObstacle()

        # Check for collisions
        if self.checkCollisions():
            self.gameOver()

        # Increase score
        self.score += 1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBackground(painter)
        self.drawObstacles(painter)
        self.drawPlayer(painter)
        self.drawHUD(painter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.game_started:
                self.jump()
            else:
                self.game_started = True

    def jump(self):
        if int(self.player_y) == self.ground_y - self.player_size:
            self.player_velocity = self.jump_strength

    def spawnObstacle(self):
        obstacle = {
            'x': self.width(),
            'y': self.ground_y - 30,  # Adjust height as needed
            'width': 30,
            'height': 30
        }
        self.obstacles.append(obstacle)

    def checkCollisions(self):
        player_rect = QRectF(self.player_x, self.player_y, self.player_size, self.player_size)
        for obstacle in self.obstacles:
            obstacle_rect = QRectF(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            if player_rect.intersects(obstacle_rect):
                return True
        return False

    def gameOver(self):
        self.timer.stop()
        print(f"Game Over! Score: {self.score}")
        # You can add more game over logic here, like showing a game over screen

    def drawBackground(self, painter):
        painter.fillRect(self.rect(), QColor(135, 206, 235))  # Sky blue background
        painter.fillRect(0, self.ground_y, self.width(), self.height() - self.ground_y, QColor(34, 139, 34))  # Green ground

    def drawPlayer(self, painter):
        if not self.player_texture.isNull():
            painter.drawPixmap(
                int(self.player_x),
                int(self.player_y),
                self.player_size,
                self.player_size,
                self.player_texture
            )
        else:
            painter.fillRect(
                int(self.player_x),
                int(self.player_y),
                self.player_size,
                self.player_size,
                QColor(255, 0, 0)
            )  # Red square if texture fails

    def drawObstacles(self, painter):
        for obstacle in self.obstacles:
            if not self.spike_texture.isNull():
                painter.drawPixmap(
                    int(obstacle['x']),
                    int(obstacle['y']),
                    obstacle['width'],
                    obstacle['height'],
                    self.spike_texture
                )
            else:
                painter.fillRect(
                    int(obstacle['x']),
                    int(obstacle['y']),
                    obstacle['width'],
                    obstacle['height'],
                    QColor(0, 0, 0)
                )

    def drawHUD(self, painter):
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont('Arial', 20))
        painter.drawText(10, 30, f"Score: {self.score}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update ground level when window is resized
        self.ground_y = self.height() - 50
        self.player_y = self.ground_y - self.player_size