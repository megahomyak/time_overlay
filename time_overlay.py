from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from datetime import datetime

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M")


class TimeIndicator(QMainWindow):
    def show_time(self, time):
        self.background = TIMES_TO_IMAGES[time]
        screen_size = app.primaryScreen().size()
        pixel_ratio = app.devicePixelRatio() ** -1
        width = int(self.background.width() * pixel_ratio)
        height = int(self.background.height() * pixel_ratio)
        x = 0
        y = screen_size.height() - height
        self.setGeometry(x, y, width, height)

        self.show()
        QTimer.singleShot(5000, self.hide)

    def check_time(self):
        last_time = get_current_time()
        if (
                last_time != self.last_time
                and last_time in TIMES_TO_IMAGES
        ):
            self.show_time(last_time)
        self.last_time = last_time

    def __init__(self):
        super().__init__()

        self.last_time = get_current_time()

        self.setWindowOpacity(1)

        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_time)
        self.check_timer.start(5000)

        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.WindowTransparentForInput
            | Qt.WindowType.X11BypassWindowManagerHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

app = QApplication([])

TIMES_TO_IMAGES = {
    i: QPixmap("battery.png")
    for i in ["21:00", "22:00"]
}

window = TimeIndicator()
app.exec()
