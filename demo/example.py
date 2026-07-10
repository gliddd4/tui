#!/usr/bin/env python3
"""
Example usage of the gliddd TUI library
"""

import tui

# Example 1: Simple menu
def example_menu():
    blocks = {
        'menu': [
            "Menu:",
            "[r] Record",
            "[t] Test",
            "[s] Settings",
            "[q] Quit",
        ],
        'information': [
            "Status: Ready",
            "Version: 1.0.0",
        ],
        'select_ui': ("SELECT_PROMPT", "❯  Select an option:"),
        'menu_items': [
            ("[r] Record", 'r'),
            ("[t] Test", 't'),
            ("[s] Settings", 's'),
            ("[q] Quit", 'q'),
        ],
        'valid_keys': ['r', 't', 's', 'q'],
    }
    
    choice = tui.show_menu("myapp", "v1.0.0", blocks, theme="blue")
    print(f"You selected: {choice}")


# Example 2: Input prompt
def example_input():
    result = tui.show_input("myapp", "v1.0.0", "Enter your name:", theme="green")
    print(f"You entered: {result}")


# Example 3: Using Window class directly
def example_window():
    window = tui.Window("dev", "v1.0.0", theme="red")
    
    blocks = {
        'menu': [
            "Commands:",
            "edit <file> - Edit file",
            "run <file>  - Run file",
            "test        - Run tests",
        ],
        'select_ui': ("SELECT_PROMPT", "❯  Press q to exit"),
        'menu_items': [],
        'valid_keys': ['q'],
    }
    
    window.show(blocks)


if __name__ == "__main__":
    print("Running example menu...")
    example_menu()