from games.QJ.QWERTZJump import QWERTZJump

class Game:
    def __init__(self):
        self.name = "QWERTZ Jump"
        self.description = "Jump through the pipes and avoid being hit by them!"
        self.thumbnail_path = "games/QJ/thumbnail.png"
        self.title_image_path = "games/QJ/title.png"

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_thumbnail(self):
        return self.thumbnail_path

    def get_title_image(self):
        return self.title_image_path

    def create_game_widget(self):
        return QWERTZJump()