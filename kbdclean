#!/usr/bin/env python3

"""
A Linux keyboard cleaning utility.

Grabs all keyboard devices at the kernel (evdev) level so you can physically clean your keys without triggering anything.
"""

from typing import Optional, Union
from pathlib import Path
import sys


def main() -> Optional[Union[int, str]]:
    """The main and only."""
    sys.path.insert(0, str(Path(__file__).parent / 'src'))
    from kbdclean.app import main as kbdclean_main
    return kbdclean_main()


if __name__ == "__main__":
    sys.exit(main())
