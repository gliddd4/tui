# tui

A Python library for terminal based programs. Includes menus, text prompts, banners, and animated gradients that can be used in any Python script.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/gliddd4/tui/main/tui.sh | sh
```

Run the demo:

```bash
tui
```

## Library usage

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.tui"))
import tui

ui = tui.TUIHelper("myapp", "v1.0.0", "blue", "gliddd4")

choice = ui.show_menu(
    information=["Select an option"],
    menu_items=[("[1] Do thing", '1'), ("[q] Quit", 'q')],
)

name = ui.show_input(prompt="Enter your name:")

ui.show_info("Done!")
```

Or use `Window` directly for full control:

```python
import sys
sys.path.insert(0, os.path.expanduser("~/.tui"))
import tui

blocks = {
    'menu': ["Menu:", "[1] Option 1", "[q] Quit"],
    'select_ui': ("SELECT_PROMPT", "❯  Select:"),
    'menu_items': [("[1] Option 1", '1'), ("[q] Quit", 'q')],
    'valid_keys': ['1', 'q'],
}

window = tui.Window("myapp", "v1.0.0", "blue", "gliddd4")
choice = window.show(blocks)
```

## Features

- Animated gradient branding
- Arrow key menu navigation
- `?` help overlay
- Auto-resizing banner
- Text input mode
- Multiple color themes (blue, red, green)
