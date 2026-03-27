"""ISO 105-key keyboard layout definitions.

Adapted from keyclean — pygame keycodes replaced with evdev keycodes.

Each KeyDef describes one physical key:
  - key_id:   unique string identifier
  - label:    text shown on the key (may be multi-line with '\\n')
  - col:      left edge in grid units
  - row:      top edge in grid units
  - width:    key width in units  (1.0 = standard key)
  - height:   key height in units
  - evdev_key: evdev ecodes.KEY_* constant, or None for unmapped keys
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from evdev import ecodes


@dataclass(frozen=True)
class KeyDef:
    """Definition of a single physical key."""
    key_id: str
    label: str
    col: float
    row: float
    width: float = 1.0
    height: float = 1.0
    evdev_key: Optional[int] = None


_NAV_OFFSET: float = 15.5

# ---------------------------------------------------------------------------
# Row 0 — Escape + F-keys + system keys
# ---------------------------------------------------------------------------
_ROW0: List[KeyDef] = [
    KeyDef("esc",    "Esc",      +0.0, 0, 1.0, 1.0, ecodes.KEY_ESC),
    KeyDef("f1",     "F1",       +2.0, 0, 1.0, 1.0, ecodes.KEY_F1),
    KeyDef("f2",     "F2",       +3.0, 0, 1.0, 1.0, ecodes.KEY_F2),
    KeyDef("f3",     "F3",       +4.0, 0, 1.0, 1.0, ecodes.KEY_F3),
    KeyDef("f4",     "F4",       +5.0, 0, 1.0, 1.0, ecodes.KEY_F4),
    KeyDef("f5",     "F5",       +6.5, 0, 1.0, 1.0, ecodes.KEY_F5),
    KeyDef("f6",     "F6",       +7.5, 0, 1.0, 1.0, ecodes.KEY_F6),
    KeyDef("f7",     "F7",       +8.5, 0, 1.0, 1.0, ecodes.KEY_F7),
    KeyDef("f8",     "F8",       +9.5, 0, 1.0, 1.0, ecodes.KEY_F8),
    KeyDef("f9",     "F9",       11.0, 0, 1.0, 1.0, ecodes.KEY_F9),
    KeyDef("f10",    "F10",      12.0, 0, 1.0, 1.0, ecodes.KEY_F10),
    KeyDef("f11",    "F11",      13.0, 0, 1.0, 1.0, ecodes.KEY_F11),
    KeyDef("f12",    "F12",      14.0, 0, 1.0, 1.0, ecodes.KEY_F12),
    KeyDef("prtsc",  "PrtSc",    _NAV_OFFSET + 0.0, 0, 1.0, 1.0, ecodes.KEY_SYSRQ),
    KeyDef("scrlk",  "ScrLk",    _NAV_OFFSET + 1.0, 0, 1.0, 1.0, ecodes.KEY_SCROLLLOCK),
    KeyDef("pause",  "Pause",    _NAV_OFFSET + 2.0, 0, 1.0, 1.0, ecodes.KEY_PAUSE),
]

# ---------------------------------------------------------------------------
# Row 1 — Number row
# ---------------------------------------------------------------------------
_ROW1: List[KeyDef] = [
    KeyDef("grave",  "`\n~",      +0.0, 1.5, 1.0, 1.0, ecodes.KEY_GRAVE),
    KeyDef("1",      "1\n!",      +1.0, 1.5, 1.0, 1.0, ecodes.KEY_1),
    KeyDef("2",      "2\n@",      +2.0, 1.5, 1.0, 1.0, ecodes.KEY_2),
    KeyDef("3",      "3\n#",      +3.0, 1.5, 1.0, 1.0, ecodes.KEY_3),
    KeyDef("4",      "4\n$",      +4.0, 1.5, 1.0, 1.0, ecodes.KEY_4),
    KeyDef("5",      "5\n%",      +5.0, 1.5, 1.0, 1.0, ecodes.KEY_5),
    KeyDef("6",      "6\n^",      +6.0, 1.5, 1.0, 1.0, ecodes.KEY_6),
    KeyDef("7",      "7\n&",      +7.0, 1.5, 1.0, 1.0, ecodes.KEY_7),
    KeyDef("8",      "8\n*",      +8.0, 1.5, 1.0, 1.0, ecodes.KEY_8),
    KeyDef("9",      "9\n(",      +9.0, 1.5, 1.0, 1.0, ecodes.KEY_9),
    KeyDef("0",      "0\n)",      10.0, 1.5, 1.0, 1.0, ecodes.KEY_0),
    KeyDef("minus",  "-\n_",      11.0, 1.5, 1.0, 1.0, ecodes.KEY_MINUS),
    KeyDef("equals", "=\n+",      12.0, 1.5, 1.0, 1.0, ecodes.KEY_EQUAL),
    KeyDef("bspace", "Backspace", 13.0, 1.5, 2.0, 1.0, ecodes.KEY_BACKSPACE),
]

# ---------------------------------------------------------------------------
# Row 2 — QWERTY row
# ---------------------------------------------------------------------------
_ROW2: List[KeyDef] = [
    KeyDef("tab",       "Tab",    +0.0, 2.5, 1.5, 1.0, ecodes.KEY_TAB),
    KeyDef("q",         "Q",      +1.5, 2.5, 1.0, 1.0, ecodes.KEY_Q),
    KeyDef("w",         "W",      +2.5, 2.5, 1.0, 1.0, ecodes.KEY_W),
    KeyDef("e",         "E",      +3.5, 2.5, 1.0, 1.0, ecodes.KEY_E),
    KeyDef("r",         "R",      +4.5, 2.5, 1.0, 1.0, ecodes.KEY_R),
    KeyDef("t",         "T",      +5.5, 2.5, 1.0, 1.0, ecodes.KEY_T),
    KeyDef("y",         "Y",      +6.5, 2.5, 1.0, 1.0, ecodes.KEY_Y),
    KeyDef("u",         "U",      +7.5, 2.5, 1.0, 1.0, ecodes.KEY_U),
    KeyDef("i",         "I",      +8.5, 2.5, 1.0, 1.0, ecodes.KEY_I),
    KeyDef("o",         "O",      +9.5, 2.5, 1.0, 1.0, ecodes.KEY_O),
    KeyDef("p",         "P",      10.5, 2.5, 1.0, 1.0, ecodes.KEY_P),
    KeyDef("lbrace",    "[\n{",   11.5, 2.5, 1.0, 1.0, ecodes.KEY_LEFTBRACE),
    KeyDef("rbrace",    "]\n}",   12.5, 2.5, 1.0, 1.0, ecodes.KEY_RIGHTBRACE),
    KeyDef("backslash", "\\\n|",  13.5, 2.5, 1.5, 1.0, ecodes.KEY_BACKSLASH),
]

# ---------------------------------------------------------------------------
# Row 3 — Home row
# ---------------------------------------------------------------------------
_ROW3: List[KeyDef] = [
    KeyDef("caps",      "Caps Lock", +0.00, 3.5, 1.75, 1.0, ecodes.KEY_CAPSLOCK),
    KeyDef("a",         "A",         +1.75, 3.5, 1.00, 1.0, ecodes.KEY_A),
    KeyDef("s",         "S",         +2.75, 3.5, 1.00, 1.0, ecodes.KEY_S),
    KeyDef("d",         "D",         +3.75, 3.5, 1.00, 1.0, ecodes.KEY_D),
    KeyDef("f",         "F",         +4.75, 3.5, 1.00, 1.0, ecodes.KEY_F),
    KeyDef("g",         "G",         +5.75, 3.5, 1.00, 1.0, ecodes.KEY_G),
    KeyDef("h",         "H",         +6.75, 3.5, 1.00, 1.0, ecodes.KEY_H),
    KeyDef("j",         "J",         +7.75, 3.5, 1.00, 1.0, ecodes.KEY_J),
    KeyDef("k",         "K",         +8.75, 3.5, 1.00, 1.0, ecodes.KEY_K),
    KeyDef("l",         "L",         +9.75, 3.5, 1.00, 1.0, ecodes.KEY_L),
    KeyDef("semi",      ";\n:",      10.75, 3.5, 1.00, 1.0, ecodes.KEY_SEMICOLON),
    KeyDef("quote",     "'\n\"",     11.75, 3.5, 1.00, 1.0, ecodes.KEY_APOSTROPHE),
    KeyDef("enter",     "Enter",     12.75, 3.5, 2.25, 1.0, ecodes.KEY_ENTER),
]

# ---------------------------------------------------------------------------
# Row 4 — Bottom row
# ---------------------------------------------------------------------------
_ROW4: List[KeyDef] = [
    KeyDef("lshift", "Shift",    +0.00, 4.5, 2.25, 1.0, ecodes.KEY_LEFTSHIFT),
    KeyDef("z",      "Z",        +2.25, 4.5, 1.00, 1.0, ecodes.KEY_Z),
    KeyDef("x",      "X",        +3.25, 4.5, 1.00, 1.0, ecodes.KEY_X),
    KeyDef("c",      "C",        +4.25, 4.5, 1.00, 1.0, ecodes.KEY_C),
    KeyDef("v",      "V",        +5.25, 4.5, 1.00, 1.0, ecodes.KEY_V),
    KeyDef("b",      "B",        +6.25, 4.5, 1.00, 1.0, ecodes.KEY_B),
    KeyDef("n",      "N",        +7.25, 4.5, 1.00, 1.0, ecodes.KEY_N),
    KeyDef("m",      "M",        +8.25, 4.5, 1.00, 1.0, ecodes.KEY_M),
    KeyDef("comma",  ",\n<",     +9.25, 4.5, 1.00, 1.0, ecodes.KEY_COMMA),
    KeyDef("period", ".\n>",     10.25, 4.5, 1.00, 1.0, ecodes.KEY_DOT),
    KeyDef("slash",  "/\n?",     11.25, 4.5, 1.00, 1.0, ecodes.KEY_SLASH),
    KeyDef("rshift", "Shift",    12.25, 4.5, 2.75, 1.0, ecodes.KEY_RIGHTSHIFT),
]

# ---------------------------------------------------------------------------
# Row 5 — Space bar row
# ---------------------------------------------------------------------------
_ROW5: List[KeyDef] = [
    KeyDef("lctrl",  "Ctrl",     +0.00, 5.5, 1.25, 1.0, ecodes.KEY_LEFTCTRL),
    KeyDef("lmeta",  "Meta",     +1.25, 5.5, 1.25, 1.0, ecodes.KEY_LEFTMETA),
    KeyDef("lalt",   "Alt",      +2.50, 5.5, 1.25, 1.0, ecodes.KEY_LEFTALT),
    KeyDef("space",  "",         +3.75, 5.5, 6.25, 1.0, ecodes.KEY_SPACE),
    KeyDef("ralt",   "Alt",      10.00, 5.5, 1.25, 1.0, ecodes.KEY_RIGHTALT),
    KeyDef("rmeta",  "Meta",     11.25, 5.5, 1.25, 1.0, ecodes.KEY_RIGHTMETA),
    KeyDef("menu",   "Menu",     12.50, 5.5, 1.25, 1.0, ecodes.KEY_COMPOSE),
    KeyDef("rctrl",  "Ctrl",     13.75, 5.5, 1.25, 1.0, ecodes.KEY_RIGHTCTRL),
]

# ---------------------------------------------------------------------------
# Navigation cluster
# ---------------------------------------------------------------------------
_NAV: List[KeyDef] = [
    KeyDef("insert", "Ins",      _NAV_OFFSET + 0.0, 1.5, 1.0, 1.0, ecodes.KEY_INSERT),
    KeyDef("home",   "Home",     _NAV_OFFSET + 1.0, 1.5, 1.0, 1.0, ecodes.KEY_HOME),
    KeyDef("pgup",   "PgUp",     _NAV_OFFSET + 2.0, 1.5, 1.0, 1.0, ecodes.KEY_PAGEUP),
    KeyDef("delete", "Del",      _NAV_OFFSET + 0.0, 2.5, 1.0, 1.0, ecodes.KEY_DELETE),
    KeyDef("end",    "End",      _NAV_OFFSET + 1.0, 2.5, 1.0, 1.0, ecodes.KEY_END),
    KeyDef("pgdn",   "PgDn",     _NAV_OFFSET + 2.0, 2.5, 1.0, 1.0, ecodes.KEY_PAGEDOWN),
    KeyDef("up",     "\u25b3\nUp",    _NAV_OFFSET + 1.0, 4.5, 1.0, 1.0, ecodes.KEY_UP),
    KeyDef("left",   "Left\n\u25c1",  _NAV_OFFSET + 0.0, 5.5, 1.0, 1.0, ecodes.KEY_LEFT),
    KeyDef("down",   "Down\n\u25bd",  _NAV_OFFSET + 1.0, 5.5, 1.0, 1.0, ecodes.KEY_DOWN),
    KeyDef("right",  "Right\n\u25b7", _NAV_OFFSET + 2.0, 5.5, 1.0, 1.0, ecodes.KEY_RIGHT),
]

# ---------------------------------------------------------------------------
# Numpad
# ---------------------------------------------------------------------------
_NP_OFFSET: float = 19.0

_NUMPAD: List[KeyDef] = [
    KeyDef("np_lock",  "Num\nLock", _NP_OFFSET + 0.0, 1.5, 1.0, 1.0, ecodes.KEY_NUMLOCK),
    KeyDef("np_slash", "/",         _NP_OFFSET + 1.0, 1.5, 1.0, 1.0, ecodes.KEY_KPSLASH),
    KeyDef("np_star",  "*",         _NP_OFFSET + 2.0, 1.5, 1.0, 1.0, ecodes.KEY_KPASTERISK),
    KeyDef("np_minus", "-",         _NP_OFFSET + 3.0, 1.5, 1.0, 1.0, ecodes.KEY_KPMINUS),
    KeyDef("np_7",     "7",         _NP_OFFSET + 0.0, 2.5, 1.0, 1.0, ecodes.KEY_KP7),
    KeyDef("np_8",     "8",         _NP_OFFSET + 1.0, 2.5, 1.0, 1.0, ecodes.KEY_KP8),
    KeyDef("np_9",     "9",         _NP_OFFSET + 2.0, 2.5, 1.0, 1.0, ecodes.KEY_KP9),
    KeyDef("np_plus",  "+",         _NP_OFFSET + 3.0, 2.5, 1.0, 2.0, ecodes.KEY_KPPLUS),
    KeyDef("np_4",     "4",         _NP_OFFSET + 0.0, 3.5, 1.0, 1.0, ecodes.KEY_KP4),
    KeyDef("np_5",     "5",         _NP_OFFSET + 1.0, 3.5, 1.0, 1.0, ecodes.KEY_KP5),
    KeyDef("np_6",     "6",         _NP_OFFSET + 2.0, 3.5, 1.0, 1.0, ecodes.KEY_KP6),
    KeyDef("np_1",     "1",         _NP_OFFSET + 0.0, 4.5, 1.0, 1.0, ecodes.KEY_KP1),
    KeyDef("np_2",     "2",         _NP_OFFSET + 1.0, 4.5, 1.0, 1.0, ecodes.KEY_KP2),
    KeyDef("np_3",     "3",         _NP_OFFSET + 2.0, 4.5, 1.0, 1.0, ecodes.KEY_KP3),
    KeyDef("np_enter", "Enter",     _NP_OFFSET + 3.0, 4.5, 1.0, 2.0, ecodes.KEY_KPENTER),
    KeyDef("np_0",     "0",         _NP_OFFSET + 0.0, 5.5, 2.0, 1.0, ecodes.KEY_KP0),
    KeyDef("np_dot",   ".",         _NP_OFFSET + 2.0, 5.5, 1.0, 1.0, ecodes.KEY_KPDOT),
]

# ---------------------------------------------------------------------------
# Full layout
# ---------------------------------------------------------------------------
KEYS: List[KeyDef] = _ROW0 + _ROW1 + _ROW2 + _ROW3 + _ROW4 + _ROW5 + _NAV + _NUMPAD

# Pre-computed bounds (used by KeyboardWidget to avoid recomputing each frame)
MAX_COL: float = max(k.col + k.width for k in KEYS)
MAX_ROW: float = max(k.row + k.height for k in KEYS)

# Mapping from evdev key code → KeyDef (for fast lookup)
EVDEV_KEY_MAP: dict[int, KeyDef] = {
    key.evdev_key: key
    for key in KEYS
    if key.evdev_key is not None
}
