# kbdclean — Implementation Plan

## Context
A Linux keyboard cleaning utility. Grabs all keyboard devices at the kernel (evdev) level so the user can physically clean keys without triggering anything. Exits via mouse click on "Done" button or typing "keyboard cleaned". Fullscreen PyQt6 window with ASCII art centerpiece and live key counter.

## Project Layout
```
kbdclean/
├── pyproject.toml
├── LICENSE                          (The Unlicense)
└── src/
    └── kbdclean/
        ├── __init__.py              (__version__ = "0.1.0")
        ├── __main__.py              (from kbdclean.app import main; main())
        ├── app.py                   (main() entry point, bootstrap & cleanup)
        ├── window.py                (MainWindow: fullscreen PyQt6 window)
        ├── grabber.py               (KeyboardGrabber: evdev discovery + EVIOCGRAB)
        ├── worker.py                (KeyboardWorker: QThread per device)
        ├── phrase.py                (PhraseDetector: thread-safe "keyboard cleaned" buffer)
        └── ascii_art.py             (KEYBOARD_ART constant)
```

## pyproject.toml
```toml
[project]
name = "kbdclean"
version = "0.1.0"
description = "Grab all keyboards for safe physical cleaning"
readme = "README.md"
license = { text = "Unlicense" }
requires-python = ">=3.11"
dependencies = ["evdev>=1.7.0", "PyQt6>=6.6.0"]

[project.scripts]
kbdclean = "kbdclean.app:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/kbdclean"]
```

Install and run with uv:
```bash
uv run kbdclean
```

## Component Details

### grabber.py — KeyboardGrabber
- `discover()`: iterate `evdev.list_devices()`, open each, check `EV_KEY` capability + required key subset (A, Z, Space, Enter, Backspace, 0, 1). Catch `PermissionError` → raise `KbdCleanPermissionError` with message: `"Cannot open /dev/input/event* — add your user to the 'input' group:\n  sudo usermod -aG input $USER\nThen log out and back in."`
- `grab_all()`: call `device.grab()` on each discovered device
- `ungrab_all()`: call `device.ungrab()` on each, wrapped in try/except so all devices are released even if one fails

### phrase.py — PhraseDetector
- Shared across all worker threads; protected by `threading.Lock`
- `_SCANCODE_TO_CHAR`: module-level dict mapping evdev key codes → lowercase chars + space
- `feed(scancode) -> bool`: append char to sliding buffer (max 16 chars = len("keyboard cleaned")); KEY_BACKSPACE (14) truncates; non-mapped scancodes silently ignored; returns True when buffer matches target
- Shift/modifier keys have no scancodes in the map → silently ignored (correct, phrase is all lowercase)

### worker.py — KeyboardWorker(QThread)
- Signals: `key_pressed`, `phrase_matched`, `error_occurred`
- `run()`: `select()` loop with 0.1s timeout (allows clean stop); on `EV_KEY` + `value==1` (key-down): emit `key_pressed`, call `detector.feed()`, if True emit `phrase_matched` and return
- `stop()`: sets `_running = False`

### window.py — MainWindow(QWidget)
Layout (QVBoxLayout):
1. `QLabel` — KEYBOARD_ART, monospace font size 11, centered, expands vertically
2. `QLabel` — "Keys pressed: 0", bold size 24, centered
3. `QLabel` — instructions text, size 12, centered
4. `QHBoxLayout` — stretch + "Done" QPushButton (120×40) + stretch

Window flags: `FramelessWindowHint | WindowStaysOnTopHint | Tool`, then `showFullScreen()`
Style: dark background `#1a1a2e`, light text `#e0e0e0`; Done button `#4a9eff` with hover state

`_do_exit()`: stop all workers → `worker.wait(2000)` each → `QApplication.quit()`
`closeEvent`: calls `_do_exit()` as safety net

### app.py — main()
1. Create `QApplication`
2. `grabber.discover()` → on error show `QMessageBox` and return
3. `grabber.grab_all()`
4. Create `PhraseDetector` (shared)
5. Create `KeyboardWorker` per device
6. Show `MainWindow`
7. Start all workers
8. `app.exec()` — blocks
9. `grabber.ungrab_all()`
10. `sys.exit()`

## Threading Model
```
Main thread (Qt event loop)
  MainWindow slots: _on_key_pressed, _on_phrase_matched, _on_done_clicked
     ↑ queued signals (PyQt6 AutoConnection, cross-thread safe)
KeyboardWorker threads (one per device)
  select() loop → emit signals
```
`PhraseDetector` shared across worker threads, protected by `threading.Lock`.

## Exit Sequence
- **Done button**: `_on_done_clicked` → `_do_exit()`
- **Type "keyboard cleaned"**: any worker's `feed()` returns True → `phrase_matched` signal → `_on_phrase_matched` → `_do_exit()`

## Development Commands
```bash
uv run kbdclean
```

## Verification
1. Run `kbdclean` — fullscreen window appears with ASCII art keyboard
2. Press keys freely — counter increments, no other app receives input
3. Click "Done" — window closes, keyboard works normally again
4. Repeat, type "keyboard cleaned" — same result
5. Test permission error: run as user not in `input` group — helpful error dialog appears
6. Test with two keyboards connected — both are grabbed simultaneously
