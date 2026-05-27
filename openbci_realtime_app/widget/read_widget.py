from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


SENTENCES = [
    "今天天气真不错，出去走走吧。",
    "你吃了吗？没吃一起吃点。",
    "这电影挺好看的，推荐你去看。",
    "最近工作怎么样？还顺利吗？",
    "周末有空吗？一起聚聚。",
    "这个东西挺好用的，你可以试试。",
    "路上小心点，注意安全。",
    "别太累了，注意休息。",
    "这事儿就这么定了，没问题。",
    "有空常联系，别断了消息。",
]


class ReadWidget(QWidget):
    def __init__(self, sentences: list[str] | None = None, parent: QWidget | None = None):
        super().__init__(parent)

        self._sentences = sentences if sentences is not None else SENTENCES
        self._index = 0
        self._tick = 0
        self._countdown = 10

        font = QFont()
        font.setPointSize(30)
        font.setBold(True)

        self._upper_label = QLabel()
        self._upper_label.setFont(font)
        self._upper_label.setAlignment(Qt.AlignCenter)
        self._upper_label.setWordWrap(True)
        self._upper_label.setStyleSheet("background-color: white; color: black;")

        self._countdown_label = QLabel(self._upper_label)
        countdown_font = QFont()
        countdown_font.setPointSize(14)
        countdown_font.setBold(True)
        self._countdown_label.setFont(countdown_font)
        self._countdown_label.setStyleSheet("background-color: transparent; color: red;")
        self._countdown_label.move(8, 8)
        self._countdown_label.setText(str(self._countdown))

        self._lower_label = QLabel()
        self._lower_label.setFont(font)
        self._lower_label.setAlignment(Qt.AlignCenter)
        self._lower_label.setStyleSheet("background-color: gray; color: black;")
 

        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._upper_label, stretch=1)
        layout.addWidget(self._lower_label, stretch=1)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_sentence)
        self._timer.start(10000)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._tick_countdown)
        self._countdown_timer.start(1000)

        self._update_sentence()

    def _update_sentence(self):
        sentence = self._sentences[self._index]
        if self._tick % 2 == 0:
            self._upper_label.setText(sentence)
            self._lower_label.clear()
        else:
            self._lower_label.setText(sentence)
            self._upper_label.clear()
        self._tick += 1
        if self._tick % 2 == 0:
            self._index = (self._index + 1) % len(self._sentences)
        self._countdown = 10
        self._countdown_label.setText(str(self._countdown))

    def _tick_countdown(self):
        self._countdown -= 1
        if self._countdown <= 0:
            self._countdown = 10
        self._countdown_label.setText(str(self._countdown))

    def set_sentences(self, sentences: list[str]):
        self._sentences = sentences
        self._index = 0
        self._tick = 0
        self._update_sentence()

    def set_text_lower(self, text: str):
        self._lower_label.setText(text)

    def pause(self):
        self._timer.stop()
        self._countdown_timer.stop()

    def resume(self):
        self._countdown = 10
        self._countdown_label.setText(str(self._countdown))
        self._timer.start(10000)
        self._countdown_timer.start(1000)
