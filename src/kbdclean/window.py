from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)

from kbdclean.ascii_art import KEYBOARD_ART
from kbdclean.worker import KeyboardWorker


class MainWindow(QWidget):
    def __init__(self, workers: list[KeyboardWorker]) -> None:
        super().__init__()
        self._workers = workers
        self._key_count = 0
        self._exiting = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setStyleSheet("background-color: #1a1a2e; color: #e0e0e0;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # ASCII art
        art_label = QLabel(KEYBOARD_ART)
        art_font = QFont("Monospace", 11)
        art_font.setStyleHint(QFont.StyleHint.Monospace)
        art_label.setFont(art_font)
        art_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        art_label.setSizePolicy(
            art_label.sizePolicy().horizontalPolicy(),
            art_label.sizePolicy().verticalPolicy(),
        )
        layout.addWidget(art_label, stretch=1)

        # Key counter
        self._counter_label = QLabel("Keys pressed: 0")
        counter_font = QFont()
        counter_font.setBold(True)
        counter_font.setPointSize(24)
        self._counter_label.setFont(counter_font)
        self._counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._counter_label)

        # Instructions
        instructions = QLabel(
            "Your keyboard is locked. Clean away!\n"
            'Click "Done" or type "keyboard cleaned" to unlock.'
        )
        instr_font = QFont()
        instr_font.setPointSize(12)
        instructions.setFont(instr_font)
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

        # Done button row
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._done_btn = QPushButton("Done")
        self._done_btn.setFixedSize(120, 40)
        self._done_btn.setStyleSheet(
            "QPushButton {"
            "  background-color: #4a9eff; color: #ffffff;"
            "  border: none; border-radius: 6px; font-size: 14px;"
            "}"
            "QPushButton:hover { background-color: #6ab4ff; }"
            "QPushButton:pressed { background-color: #2a7edd; }"
        )
        self._done_btn.clicked.connect(self._on_done_clicked)
        btn_row.addWidget(self._done_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Connect worker signals
        for worker in self._workers:
            worker.key_pressed.connect(self._on_key_pressed)
            worker.phrase_matched.connect(self._on_phrase_matched)

        self.showFullScreen()

    def _on_key_pressed(self) -> None:
        self._key_count += 1
        self._counter_label.setText(f"Keys pressed: {self._key_count}")

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
