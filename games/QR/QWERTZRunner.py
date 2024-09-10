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
        self.jump_strength = -20
        self.game_speed = 5
        self.score = 0
        self.obstacles = []
        self.platforms = []
        self.game_started = False

        # Set ground level near the bottom of the screen
        self.ground_y = self.height() - 50 if self.height() > 0 else 550
        self.player_y = self.ground_y - self.player_size

        # Load textures
        self.player_texture = QPixmap("games/QR/player.png")
        self.spike_texture = QPixmap("games/QR/spike.png")
        self.platform_texture = QPixmap("games/QJ/pipe.jpg")
        if self.player_texture.isNull() or self.spike_texture.isNull() or self.platform_texture.isNull():
            print("Failed to load textures")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(16)  # ~60 FPS

        self.last_obstacle_x = 0
        print(f"Initial last_obstacle_x: {self.last_obstacle_x}")

    def updateGame(self):
        if not self.game_started:
            return

        # Update player position
        self.player_velocity += self.gravity
        self.player_y += self.player_velocity

        # Keep player above ground and platforms
        self.checkPlayerCollisions()

        # Move spawn point and objects
        self.moveSpawnPoint()

        # Remove off-screen objects
        self.obstacles = [obs for obs in self.obstacles if obs['x'] > -50]
        self.platforms = [plat for plat in self.platforms if plat['x'] > -100]

        # Spawn new obstacles and platforms
        print(f"Width: {self.width()}, last_obstacle_x: {self.last_obstacle_x}")
        if self.last_obstacle_x < self.width():
            print("Spawning new area")
            self.spawnArea()
        else:
            print("Not spawning new area")

        # Check for collisions with spikes
        if self.checkSpikeCollisions():
            self.gameOver()

        # Increase score
        self.score += 1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBackground(painter)
        self.drawPlatforms(painter)
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
        if self.player_velocity == 0:  # Only jump if on a surface
            self.player_velocity = self.jump_strength

    def spawnArea(self):
        area_type = random.choice(["ground", "platform", "gap"])
        
        if area_type == "ground":
            length = self.spawnGroundArea()
        elif area_type == "platform":
            length = self.spawnPlatformArea()
        else:
            length = self.spawnGap()
        
        self.last_obstacle_x += length
        print(f"Spawned {area_type}. New last_obstacle_x: {self.last_obstacle_x}")

    def spawnGroundArea(self):
        length = random.randint(200, 400)
        a = 0
        for x in range(int(self.last_obstacle_x), int(self.last_obstacle_x + length), 50):
            a +=1
            if a == 3:
                a = 0
                if random.random() < 0.5:  # 50% chance to spawn a spike
                    self.spawnObstacle(x)
        return length

    def spawnPlatformArea(self):
        platform_y = random.randint(int(self.ground_y - 150), int(self.ground_y - 50))
        length = random.randint(100, 300)
        self.platforms.append({
            'x': self.last_obstacle_x,
            'y': platform_y,
            'width': length,
            'height': 20
        })
        return length

    def spawnGap(self):
        gap_length = random.randint(100, 200)
        return gap_length

    def spawnObstacle(self, x):
        obstacle = {
            'x': x,
            'y': self.ground_y - 30,
            'width': 30,
            'height': 30
        }
        self.obstacles.append(obstacle)

    def moveSpawnPoint(self):
        move_distance = self.game_speed
        self.last_obstacle_x -= move_distance
        for obstacle in self.obstacles:
            obstacle['x'] -= move_distance
        for platform in self.platforms:
            platform['x'] -= move_distance

    def checkPlayerCollisions(self):
        player_rect = QRectF(self.player_x, self.player_y + 1, self.player_size, self.player_size)
        
        # Check ground collision
        if self.player_y > self.ground_y - self.player_size:
            self.player_y = self.ground_y - self.player_size
            self.player_velocity = 0
            return

        # Check platform collisions
        for platform in self.platforms:
            platform_rect = QRectF(platform['x'], platform['y'], platform['width'], platform['height'])
            if player_rect.intersects(platform_rect) and self.player_velocity >= 0:
                self.player_y = platform['y'] - self.player_size
                self.player_velocity = 0
                return

        # If no collision, player is in air
        self.player_velocity += self.gravity

    def checkSpikeCollisions(self):
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

    def drawPlatforms(self, painter):
        for platform in self.platforms:
            if not self.platform_texture.isNull():
                painter.drawPixmap(
                    int(platform['x']),
                    int(platform['y']),
                    platform['width'],
                    platform['height'],
                    self.platform_texture
                )
            else:
                painter.fillRect(
                    int(platform['x']),
                    int(platform['y']),
                    platform['width'],
                    platform['height'],
                    QColor(150, 75, 0)
                )

    def drawHUD(self, painter):
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont('Arial', 20))
        painter.drawText(10, 30, f"Score: {self.score}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update ground level when window is resized
        self.ground_y = self.height() - 50
        self.player_y = min(self.player_y, self.ground_y - self.player_size)
        print(f"Window resized. New width: {self.width()}, New height: {self.height()}")