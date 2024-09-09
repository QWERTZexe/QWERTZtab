import os
from PyQt6.QtCore import QObject, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class SoundManager(QObject):
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.players = {}
        self.audio_outputs = {}

    def load_sound(self, name, path):
        if not os.path.exists(path):
            print(f"Sound file not found: {path}")
            return

        url = QUrl.fromLocalFile(path)
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        player.setSource(url)

        self.sounds[name] = url
        self.players[name] = player
        self.audio_outputs[name] = audio_output

        print(f"Sound '{name}' loaded successfully")

    def play_sound(self, name):
        if name in self.players:
            player = self.players[name]
            player.setPosition(0)  # Reset to start of the sound
            QTimer.singleShot(0, player.play)  # Schedule playback for the next event loop iteration
        else:
            print(f"Sound '{name}' not found")

# Global instance of SoundManager
sound_manager = SoundManager()

def load_sound(name, path):
    sound_manager.load_sound(name, path)

def play_sound(name):
    sound_manager.play_sound(name)