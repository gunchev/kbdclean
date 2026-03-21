import evdev
from evdev import ecodes

_REQUIRED_KEYS = {
    ecodes.KEY_A, ecodes.KEY_Z, ecodes.KEY_SPACE,
    ecodes.KEY_ENTER, ecodes.KEY_BACKSPACE,
    ecodes.KEY_0, ecodes.KEY_1,
}


class KbdCleanPermissionError(Exception):
    pass


class KeyboardGrabber:
    def __init__(self) -> None:
        self._devices: list[evdev.InputDevice] = []

    def discover(self) -> None:
        self._devices = []
        for path in evdev.list_devices():
            try:
                dev = evdev.InputDevice(path)
            except PermissionError:
                raise KbdCleanPermissionError(
                    f"Cannot open {path} — add your user to the 'input' group:\n"
                    "  sudo usermod -aG input $USER\n"
                    "Then log out and back in."
                )
            caps = dev.capabilities()
            if ecodes.EV_KEY not in caps:
                dev.close()
                continue
            keys = set(caps[ecodes.EV_KEY])
            if not _REQUIRED_KEYS.issubset(keys):
                dev.close()
                continue
            self._devices.append(dev)

    @property
    def devices(self) -> list[evdev.InputDevice]:
        return self._devices

    def grab_all(self) -> None:
        for dev in self._devices:
            dev.grab()

    def ungrab_all(self) -> None:
        for dev in self._devices:
            try:
                dev.ungrab()
            except Exception:
                pass
