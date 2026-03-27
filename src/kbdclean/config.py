"""Constants: colors, sizes, exit phrase, app identity."""

from kbdclean import __version__ as _version

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
EXIT_PHRASE: str = "keys are clean"
APP_TITLE: str = f"kbdclean  v{_version}"
APP_DESCRIPTION: str = "Lock your keyboard, wipe it clean."

# ---------------------------------------------------------------------------
# Layout geometry  (reference resolution 1920×1080; renderer scales these)
# ---------------------------------------------------------------------------
KEY_UNIT: int = 54      # width of one "1u" key in px at reference res
KEY_HEIGHT: int = 50    # height of all keys (tall keys use height multiplier)
KEY_GAP: int = 4        # gap between keys
KEY_FONT_SIZE: int = 11  # key-label font size in pt at reference scale

# ---------------------------------------------------------------------------
# Colors  (hex strings accepted by QColor)
# ---------------------------------------------------------------------------
COLOR_BG: str = "#121212"
COLOR_KEY_NORMAL: str = "#37373c"
COLOR_KEY_PRESSED: str = "#50b4ff"
COLOR_KEY_BORDER: str = "#5a5a5f"
COLOR_KEY_TEXT: str = "#dcdcdc"
COLOR_KEY_TEXT_PRESSED: str = "#0a0a14"
COLOR_COUNTER_TEXT: str = "#c8c8c8"
COLOR_TITLE_TEXT: str = "#dcdcff"
COLOR_DESC_TEXT: str = "#8c8ca0"
COLOR_HELP_TEXT: str = "#828290"
COLOR_DONE_BG: str = "#288c3c"
COLOR_DONE_BG_HOVER: str = "#3cc850"
COLOR_DONE_TEXT: str = "#ffffff"
