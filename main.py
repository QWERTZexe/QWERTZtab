import sys
from PyQt6.QtWidgets import QApplication

from table.GameTable import GameTable

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_table = GameTable()
    sys.exit(app.exec())