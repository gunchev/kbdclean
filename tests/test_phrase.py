import threading

import pytest
from evdev import ecodes

from kbdclean.phrase import PhraseDetector, _TARGET


def _type(detector, text):
    """Helper: feed a string into the detector character by character."""
    key_map = {v: k for k, v in {
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
    }.items()}
    results = []
    for ch in text:
        results.append(detector.feed(key_map[ch]))
    return results


class TestPhraseDetector:
    def test_unknown_scancode_ignored(self):
        d = PhraseDetector()
        assert d.feed(9999) is False

    def test_modifier_keys_ignored(self):
        d = PhraseDetector()
        for code in (ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT,
                     ecodes.KEY_LEFTCTRL, ecodes.KEY_LEFTALT):
            assert d.feed(code) is False

    def test_single_char_no_match(self):
        d = PhraseDetector()
        assert d.feed(ecodes.KEY_K) is False

    def test_partial_phrase_no_match(self):
        d = PhraseDetector()
        results = _type(d, "keyboard")
        assert all(r is False for r in results)

    def test_full_phrase_matches(self):
        d = PhraseDetector()
        results = _type(d, _TARGET)
        assert results[-1] is True
        assert all(r is False for r in results[:-1])

    def test_phrase_only_matches_at_end(self):
        d = PhraseDetector()
        # extra chars before the phrase
        results = _type(d, "xxx" + _TARGET)
        assert results[-1] is True

    def test_sliding_window_drops_old_chars(self):
        d = PhraseDetector()
        # overflow the buffer so old chars are dropped
        _type(d, "z" * 20)
        assert d.feed(ecodes.KEY_A) is False

    def test_backspace_removes_last_char(self):
        # _TARGET = "keys are clean"; type all but last char, backspace, wrong char → no match
        d = PhraseDetector()
        _type(d, _TARGET[:-1])          # "keys are clea"
        d.feed(ecodes.KEY_BACKSPACE)    # removes 'a', buffer = "keys are cle"
        result = d.feed(ecodes.KEY_N)   # "keys are clen" — no match
        assert result is False

    def test_backspace_then_retype_matches(self):
        d = PhraseDetector()
        _type(d, _TARGET[:-1])           # "keys are clea"
        d.feed(ecodes.KEY_BACKSPACE)     # removes 'a', buffer = "keys are cle"
        result = d.feed(ecodes.KEY_N)    # "keys are clen" — no match
        assert result is False
        # correct it
        d2 = PhraseDetector()
        _type(d2, _TARGET[:-1])          # "keys are clea"
        d2.feed(ecodes.KEY_BACKSPACE)    # "keys are cle"
        d2.feed(ecodes.KEY_A)            # "keys are clea"
        result = d2.feed(ecodes.KEY_N)   # "keys are clean" — match!
        assert result is True

    def test_backspace_on_empty_buffer_is_safe(self):
        d = PhraseDetector()
        assert d.feed(ecodes.KEY_BACKSPACE) is False
        assert d.feed(ecodes.KEY_BACKSPACE) is False

    def test_space_key_mapped(self):
        d = PhraseDetector()
        assert d.feed(ecodes.KEY_SPACE) is False  # just a space, no match

    def test_thread_safety(self):
        """Multiple threads feeding concurrently must not crash or corrupt state."""
        d = PhraseDetector()
        errors = []

        def worker():
            try:
                for _ in range(500):
                    _type(d, "ab")
                    d.feed(ecodes.KEY_BACKSPACE)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
