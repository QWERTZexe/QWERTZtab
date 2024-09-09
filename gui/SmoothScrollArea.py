from PyQt6.QtWidgets import QScrollArea, QWidget
from PyQt6.QtCore import Qt, QEvent, QPoint

class SmoothScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrolling = False
        self.last_pos = QPoint()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.scrolling = True
            self.last_pos = event.position().toPoint()
            return True
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.scrolling = False
            return True
        elif event.type() == QEvent.Type.MouseMove and self.scrolling:
            dx = event.position().x() - self.last_pos.x()
            self.last_pos = event.position().toPoint()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dx)
            return True
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        # Disable vertical scrolling
        if event.angleDelta().y() != 0:
            event.ignore()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):
        self.scrolling = True
        self.last_pos = event.position().toPoint()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.scrolling = False
        event.accept()

    def mouseMoveEvent(self, event):
        if self.scrolling:
            dx = event.position().x() - self.last_pos.x()
            self.last_pos = event.position().toPoint()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - dx)
        event.accept()