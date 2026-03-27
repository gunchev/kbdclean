import sys
from unittest.mock import MagicMock, patch

import pytest
from evdev import ecodes
from PyQt6.QtWidgets import QApplication

from kbdclean.phrase import PhraseDetector
from kbdclean.worker import KeyboardWorker


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


def _make_event(type_, code, value):
    ev = MagicMock()
    ev.type = type_
    ev.code = code
    ev.value = value
    return ev


def _run_worker_with_events(device, events, detector=None):
    """
    Run a KeyboardWorker synchronously by mocking select.select to return
    ready once (delivering events) then stop the worker on the next call.
    """
    if detector is None:
        detector = PhraseDetector()

    device.read.return_value = events
    worker = KeyboardWorker(device, detector)

    # Collect emitted signals
    pressed = []
    matched = []
    errors = []
    worker.key_pressed.connect(lambda code: pressed.append(code))
    worker.phrase_matched.connect(lambda: matched.append(1))
    worker.error_occurred.connect(errors.append)

    call_count = 0

    def fake_select(rlist, wlist, xlist, timeout):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return rlist, [], []
        # Events have been processed; stop the worker so run() exits cleanly.
        worker.stop()
        return [], [], []

    with patch("select.select", side_effect=fake_select):
        worker.run()

    return pressed, matched, errors, worker


class TestKeyboardWorker:
    def test_key_down_emits_key_pressed(self, qapp):
        device = MagicMock()
        device.fd = 5
        event = _make_event(ecodes.EV_KEY, ecodes.KEY_A, 1)
        pressed, matched, errors, _ = _run_worker_with_events(device, [event])
        assert pressed == [ecodes.KEY_A]
        assert matched == []
        assert errors == []

    def test_key_up_emits_key_released(self, qapp):
        device = MagicMock()
        device.fd = 5
        event = _make_event(ecodes.EV_KEY, ecodes.KEY_A, 0)  # value=0 is key-up

        worker = KeyboardWorker(device, PhraseDetector())
        released = []
        pressed = []
        worker.key_released.connect(lambda code: released.append(code))
        worker.key_pressed.connect(lambda code: pressed.append(code))
        device.read.return_value = [event]

        call_count = 0

        def fake_select(rlist, wlist, xlist, timeout):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return rlist, [], []
            worker.stop()
            return [], [], []

        with patch("select.select", side_effect=fake_select):
            worker.run()

        assert released == [ecodes.KEY_A]
        assert pressed == []

    def test_key_repeat_does_not_emit(self, qapp):
        device = MagicMock()
        device.fd = 5
        event = _make_event(ecodes.EV_KEY, ecodes.KEY_A, 2)  # value=2 is repeat
        pressed, matched, errors, _ = _run_worker_with_events(device, [event])
        assert pressed == []

    def test_non_key_event_ignored(self, qapp):
        device = MagicMock()
        device.fd = 5
        event = _make_event(ecodes.EV_SYN, 0, 0)
        pressed, matched, errors, _ = _run_worker_with_events(device, [event])
        assert pressed == []

    def test_phrase_match_emits_phrase_matched(self, qapp):
        device = MagicMock()
        device.fd = 5

        detector = MagicMock(spec=PhraseDetector)
        detector.feed.return_value = True  # phrase matched immediately

        event = _make_event(ecodes.EV_KEY, ecodes.KEY_A, 1)

        call_count = 0

        def fake_select(rlist, wlist, xlist, timeout):
            nonlocal call_count
            call_count += 1
            return rlist, [], []

        device.read.return_value = [event]

        worker = KeyboardWorker(device, detector)
        matched = []
        worker.phrase_matched.connect(lambda: matched.append(1))

        with patch("select.select", side_effect=fake_select):
            worker.run()  # should return after phrase matched

        assert len(matched) == 1

    def test_exception_emits_error_occurred(self, qapp):
        device = MagicMock()
        device.fd = 5
        device.read.side_effect = OSError("device disconnected")

        def fake_select(rlist, wlist, xlist, timeout):
            return rlist, [], []

        worker = KeyboardWorker(device, PhraseDetector())
        errors = []
        worker.error_occurred.connect(errors.append)

        with patch("select.select", side_effect=fake_select):
            worker.run()

        assert len(errors) == 1
        assert "device disconnected" in errors[0]

    def test_stop_prevents_run(self, qapp):
        device = MagicMock()
        device.fd = 5

        calls = []

        def fake_select(rlist, wlist, xlist, timeout):
            calls.append(1)
            return [], [], []  # no events

        worker = KeyboardWorker(device, PhraseDetector())
        worker.stop()

        with patch("select.select", side_effect=fake_select):
            worker.run()

        # With _running=False from the start, the loop exits immediately
        assert calls == []

    def test_multiple_events_in_one_read(self, qapp):
        device = MagicMock()
        device.fd = 5
        events = [
            _make_event(ecodes.EV_KEY, ecodes.KEY_A, 1),
            _make_event(ecodes.EV_KEY, ecodes.KEY_B, 1),
            _make_event(ecodes.EV_KEY, ecodes.KEY_C, 1),
        ]
        pressed, _, errors, _ = _run_worker_with_events(device, events)
        assert pressed == [ecodes.KEY_A, ecodes.KEY_B, ecodes.KEY_C]
        assert errors == []
