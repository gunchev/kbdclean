# kbdclean

A Linux keyboard cleaning utility. Grabs all keyboard devices at the kernel (evdev) level so you can physically clean your keys without triggering anything.

> Vibe-coded using [Claude Sonnet 4.6](https://www.anthropic.com/claude).

## How it works

- Discovers all keyboard devices under `/dev/input/`
- Grabs them exclusively via `EVIOCGRAB` — no keystrokes reach any application
- Shows a fullscreen window with an ASCII art keyboard and a live key counter
- Releases all keyboards on exit

## Exit

- Click the **Done** button, or
- Type `keyboard cleaned`

## Requirements

- Linux
- Python 3.11+
- `evdev` and `PyQt6` (system packages or virtualenv)
- User must be in the `input` group (or run as root)

```bash
sudo usermod -aG input $USER
# log out and back in
```

## Usage

```bash
uv run kbdclean
```

Or install and run directly:

```bash
uv tool install .
kbdclean
```

## License

The Unlicense — public domain. See [LICENSE](LICENSE).
