from unittest.mock import MagicMock, patch

import pytest
from evdev import ecodes

from kbdclean.grabber import KeyboardGrabber, KbdCleanPermissionError, _REQUIRED_KEYS


def _make_device(keys=None, has_ev_key=True):
    """Return a mock evdev.InputDevice with the given key capabilities."""
    dev = MagicMock()
    if has_ev_key:
        dev.capabilities.return_value = {ecodes.EV_KEY: list(keys or _REQUIRED_KEYS)}
    else:
        dev.capabilities.return_value = {}
    return dev


class TestDiscover:
    def test_permission_denied_via_os_access(self):
        """When os.access reports no read permission, raise KbdCleanPermissionError."""
        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=False):
            g = KeyboardGrabber()
            with pytest.raises(KbdCleanPermissionError, match="input"):
                g.discover()

    def test_permission_error_on_open(self):
        """When InputDevice raises PermissionError, raise KbdCleanPermissionError."""
        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=True), \
             patch("evdev.list_devices", return_value=["/dev/input/event0"]), \
             patch("evdev.InputDevice", side_effect=PermissionError):
            g = KeyboardGrabber()
            with pytest.raises(KbdCleanPermissionError, match="input"):
                g.discover()

    def test_no_event_files_no_error(self):
        """If /dev/input/event* is empty, discover() succeeds with no devices."""
        with patch("glob.glob", return_value=[]), \
             patch("evdev.list_devices", return_value=[]):
            g = KeyboardGrabber()
            g.discover()
            assert g.devices == []

    def test_device_without_ev_key_skipped(self):
        """Devices that lack EV_KEY capability are ignored."""
        dev = _make_device(has_ev_key=False)
        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=True), \
             patch("evdev.list_devices", return_value=["/dev/input/event0"]), \
             patch("evdev.InputDevice", return_value=dev):
            g = KeyboardGrabber()
            g.discover()
            assert g.devices == []
            dev.close.assert_called_once()

    def test_device_missing_required_keys_skipped(self):
        """Devices that don't have the full required key set are ignored."""
        dev = _make_device(keys=[ecodes.KEY_A])  # missing most required keys
        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=True), \
             patch("evdev.list_devices", return_value=["/dev/input/event0"]), \
             patch("evdev.InputDevice", return_value=dev):
            g = KeyboardGrabber()
            g.discover()
            assert g.devices == []
            dev.close.assert_called_once()

    def test_valid_keyboard_discovered(self):
        """A device with all required keys is added to devices."""
        dev = _make_device()
        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=True), \
             patch("evdev.list_devices", return_value=["/dev/input/event0"]), \
             patch("evdev.InputDevice", return_value=dev):
            g = KeyboardGrabber()
            g.discover()
            assert g.devices == [dev]

    def test_multiple_devices_only_keyboards_kept(self):
        """Mixed devices: only full keyboards are kept."""
        kbd = _make_device()
        mouse = _make_device(has_ev_key=False)
        partial = _make_device(keys=[ecodes.KEY_A, ecodes.KEY_B])

        def make_device(path):
            return {"/dev/input/event0": kbd,
                    "/dev/input/event1": mouse,
                    "/dev/input/event2": partial}[path]

        with patch("glob.glob", return_value=["/dev/input/event0"]), \
             patch("os.access", return_value=True), \
             patch("evdev.list_devices",
                   return_value=["/dev/input/event0", "/dev/input/event1",
                                 "/dev/input/event2"]), \
             patch("evdev.InputDevice", side_effect=make_device):
            g = KeyboardGrabber()
            g.discover()
            assert g.devices == [kbd]


class TestGrabUngrab:
    def _grabber_with_devices(self, devs):
        g = KeyboardGrabber()
        g._devices = devs
        return g

    def test_grab_all_calls_grab_on_each(self):
        devs = [MagicMock(), MagicMock()]
        g = self._grabber_with_devices(devs)
        g.grab_all()
        for dev in devs:
            dev.grab.assert_called_once()

    def test_ungrab_all_calls_ungrab_on_each(self):
        devs = [MagicMock(), MagicMock()]
        g = self._grabber_with_devices(devs)
        g.ungrab_all()
        for dev in devs:
            dev.ungrab.assert_called_once()

    def test_ungrab_all_continues_after_exception(self):
        """ungrab_all must release all devices even if one raises."""
        dev1 = MagicMock()
        dev1.ungrab.side_effect = OSError("busy")
        dev2 = MagicMock()
        g = self._grabber_with_devices([dev1, dev2])
        g.ungrab_all()  # must not raise
        dev2.ungrab.assert_called_once()
