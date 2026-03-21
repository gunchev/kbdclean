import threading
from evdev import ecodes

_TARGET = "keyboard cleaned"

# Map evdev key codes to lowercase characters
_SCANCODE_TO_CHAR: dict[int, str] = {
    ecodes.KEY_A: "a", ecodes.KEY_B: "b", ecodes.KEY_C: "c",
    ecodes.KEY_D: "d", ecodes.KEY_E: "e", ecodes.KEY_F: "f",
    ecodes.KEY_G: "g", ecodes.KEY_H: "h", ecodes.KEY_I: "i",
    ecodes.KEY_J: "j", ecodes.KEY_K: "k", ecodes.KEY_L: "l",
    ecodes.KEY_M: "m", ecodes.KEY_N: "n", ecodes.KEY_O: "o",
    ecodes.KEY_P: "p", ecodes.KEY_Q: "q", ecodes.KEY_R: "r",
    ecodes.KEY_S: "s", ecodes.KEY_T: "t", ecodes.KEY_U: "u",
    ecodes.KEY_V: "v", ecodes.KEY_W: "w", ecodes.KEY_X: "x",
    ecodes.KEY_Y: "y", ecodes.KEY_Z: "z",
    ecodes.KEY_SPACE: " ",
}

_MAX_LEN = len(_TARGET)


class PhraseDetector:
    def __init__(self) -> None:
        self._buf = ""
        self._lock = threading.Lock()

    def feed(self, scancode: int) -> bool:
        with self._lock:
            if scancode == ecodes.KEY_BACKSPACE:
                self._buf = self._buf[:-1]
                return False
            ch = _SCANCODE_TO_CHAR.get(scancode)
            if ch is None:
                return False
            self._buf = (self._buf + ch)[-_MAX_LEN:]
            return self._buf == _TARGET
