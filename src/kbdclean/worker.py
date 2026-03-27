import select
import evdev
from evdev import ecodes
from PyQt6.QtCore import QThread, pyqtSignal

from kbdclean.phrase import PhraseDetector


class KeyboardWorker(QThread):
    key_pressed = pyqtSignal(int)   # emitted on key-down; carries evdev key code
    key_released = pyqtSignal(int)  # emitted on key-up;   carries evdev key code
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
                    if event.type != ecodes.EV_KEY:
                        continue
                    if event.value == 1:  # key-down
                        self.key_pressed.emit(event.code)
                        if self._detector.feed(event.code):
                            self.phrase_matched.emit()
                            return
                    elif event.value == 0:  # key-up
                        self.key_released.emit(event.code)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self) -> None:
        self._running = False
