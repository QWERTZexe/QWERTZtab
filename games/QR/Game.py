from games.QR.QWERTZRunner import QWERTZRunner

class Game:
    def __init__(self):
        self.name = "QWERTZ Runner"
        self.description = "A side-scrolling endless runner where the player controls a character that automatically runs forward."
        self.thumbnail_path = "games/QR/thumbnail.png"
        self.title_image_path = "games/QR/title.jpg"

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_thumbnail(self):
        return self.thumbnail_path

    def get_title_image(self):
        return self.title_image_path

    def create_game_widget(self):
        return QWERTZRunner()