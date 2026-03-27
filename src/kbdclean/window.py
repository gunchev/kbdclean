from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from kbdclean import config
from kbdclean.keyboard_layout import KEYS, MAX_COL, MAX_ROW
from kbdclean.worker import KeyboardWorker


class KeyboardWidget(QWidget):
    """Draws the ISO keyboard with live key-pressed highlighting."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._pressed: set[int] = set()

    def set_pressed(self, pressed: set[int]) -> None:
        self._pressed = pressed
        self.update()

    def paintEvent(self, event) -> None:  # pylint: disable=unused-argument
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        h_scale = (w * 0.95) / (MAX_COL * (config.KEY_UNIT + config.KEY_GAP))
        v_scale = (h * 0.95) / (MAX_ROW * (config.KEY_HEIGHT + config.KEY_GAP))
        scale = min(h_scale, v_scale)

        unit = config.KEY_UNIT * scale
        gap = config.KEY_GAP * scale
        key_h = config.KEY_HEIGHT * scale

        kbd_w = MAX_COL * (unit + gap)
        kbd_h = MAX_ROW * (key_h + gap)
        kbd_x = (w - kbd_w) / 2
        kbd_y = (h - kbd_h) / 2

        font = QFont("DejaVu Sans Mono, Menlo, Consolas, Courier New")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSizeF(max(6.0, config.KEY_FONT_SIZE * scale))
        painter.setFont(font)

        border_pen = QPen(QColor(config.COLOR_KEY_BORDER), 1)

        for key in KEYS:
            x = kbd_x + key.col * (unit + gap)
            y = kbd_y + key.row * (key_h + gap)
            kw = key.width * (unit + gap) - gap
            kh = key.height * (key_h + gap) - gap

            pressed = key.evdev_key in self._pressed
            bg = QColor(config.COLOR_KEY_PRESSED if pressed else config.COLOR_KEY_NORMAL)
            text_color = QColor(
                config.COLOR_KEY_TEXT_PRESSED if pressed else config.COLOR_KEY_TEXT
            )

            rect = QRectF(x, y, kw, kh)
            painter.setPen(border_pen)
            painter.setBrush(QBrush(bg))
            painter.drawRoundedRect(rect, 4, 4)

            if key.label:
                painter.setPen(text_color)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, key.label)


class MainWindow(QWidget):
    def __init__(self, workers: list[KeyboardWorker]) -> None:
        super().__init__()
        self._workers = workers
        self._key_count = 0
        self._pressed_keys: set[int] = set()
        self._exiting = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setStyleSheet(
            f"background-color: {config.COLOR_BG}; color: {config.COLOR_KEY_TEXT};"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        # Title
        title_label = QLabel(config.APP_TITLE)
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f"color: {config.COLOR_TITLE_TEXT};")
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(config.APP_DESCRIPTION)
        desc_font = QFont()
        desc_font.setPointSize(11)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(f"color: {config.COLOR_DESC_TEXT};")
        layout.addWidget(desc_label)

        # Keyboard widget
        self._keyboard_widget = KeyboardWidget()
        layout.addWidget(self._keyboard_widget, stretch=1)

        # Counter
        self._counter_label = QLabel("Keys struck: 0")
        counter_font = QFont()
        counter_font.setBold(True)
        counter_font.setPointSize(18)
        self._counter_label.setFont(counter_font)
        self._counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._counter_label.setStyleSheet(f"color: {config.COLOR_COUNTER_TEXT};")
        layout.addWidget(self._counter_label)

        # Help text
        help_label = QLabel(
            f'Type "{config.EXIT_PHRASE}" or click Done to exit'
        )
        help_font = QFont()
        help_font.setPointSize(11)
        help_label.setFont(help_font)
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        help_label.setStyleSheet(f"color: {config.COLOR_HELP_TEXT};")
        layout.addWidget(help_label)

        # Done button row
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._done_btn = QPushButton("Done")
        self._done_btn.setFixedSize(120, 40)
        self._done_btn.setStyleSheet(
            f"QPushButton {{"
            f"  background-color: {config.COLOR_DONE_BG}; color: {config.COLOR_DONE_TEXT};"
            f"  border: none; border-radius: 6px; font-size: 14px;"
            f"}}"
            f"QPushButton:hover {{ background-color: {config.COLOR_DONE_BG_HOVER}; }}"
            f"QPushButton:pressed {{ background-color: {config.COLOR_DONE_BG}; }}"
        )
        self._done_btn.clicked.connect(self._on_done_clicked)
        btn_row.addWidget(self._done_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Connect worker signals
        for worker in self._workers:
            worker.key_pressed.connect(self._on_key_pressed)
            worker.key_released.connect(self._on_key_released)
            worker.phrase_matched.connect(self._on_phrase_matched)

        self.showFullScreen()

    def _on_key_pressed(self, code: int) -> None:
        self._key_count += 1
        self._counter_label.setText(f"Keys struck: {self._key_count:,}")
        self._pressed_keys.add(code)
        self._keyboard_widget.set_pressed(self._pressed_keys)

    def _on_key_released(self, code: int) -> None:
        self._pressed_keys.discard(code)
        self._keyboard_widget.set_pressed(self._pressed_keys)

    def _on_phrase_matched(self) -> None:
        self._do_exit()

    def _on_done_clicked(self) -> None:
        self._do_exit()

    def _do_exit(self) -> None:
        if self._exiting:
            return
        self._exiting = True
        for worker in self._workers:
            worker.stop()
        for worker in self._workers:
            worker.wait(2000)
        QApplication.quit()

    def closeEvent(self, event) -> None:
        self._do_exit()
        event.accept()
