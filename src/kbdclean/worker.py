import select
import evdev
from evdev import ecodes
from PyQt6.QtCore import QThread, pyqtSignal

from kbdclean.phrase import PhraseDetector


class KeyboardWorker(QThread):
    key_pressed = pyqtSignal()
    phrase_matched = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, device: evdev.InputDevice, detector: PhraseDetector) -> None:
        super().__init__()
        self._device = device
        self._detector = detector
        self._running = True

    def run(self) -> None:
        try:
            while self._running:
                r, _, _ = select.select([self._device.fd], [], [], 0.1)
                if not r:
                    continue
                for event in self._device.read():
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        self.key_pressed.emit()
                        if self._detector.feed(event.code):
                            self.phrase_matched.emit()
                            return
        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self) -> None:
        self._running = False
