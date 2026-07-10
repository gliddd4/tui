#!/usr/bin/env python3
"""
TUI Demo - Interactive demonstration of the tui library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tui

ui = tui.TUIHelper("tui-demo", "v1.0.0", "blue", "gliddd4")

def main():
    while True:
        choice = ui.show_menu(
            information=[
                "TUI Library Demo",
                "Each option showcases a different feature",
            ],
            menu_items=[
                ("[1] Simple menu", '1'),
                ("[2] Menu with info", '2'),
                ("[3] Commands list", '3'),
                ("[4] Text input", '4'),
                ("[5] Notifications", '5'),
                ("[6] Countdown", '6'),
                ("[q] Quit", 'q'),
            ],
            quit_presses=3,
        )

        if choice == 'q':
            break
        elif choice == '1':
            demo_simple_menu()
        elif choice == '2':
            demo_menu_with_info()
        elif choice == '3':
            demo_commands_list()
        elif choice == '4':
            demo_text_input()
        elif choice == '5':
            demo_notifications()
        elif choice == '6':
            demo_countdown()


def demo_simple_menu():
    """Simple arrow-key navigable menu"""
    choice = ui.show_menu(
        information=["Pick an option to see what happens"],
        menu_items=[
            ("[a] Option A", 'a'),
            ("[b] Option B", 'b'),
            ("[c] Option C", 'c'),
        ],
    )
    if choice != 'q':
        ui.show_info(f"You picked {choice.upper()}!", timeout=1.5)


def demo_menu_with_info():
    """Menu with live status info"""
    choice = ui.show_menu(
        information=[
            "Status: Ready",
            "Items: 3/5 configured",
            "Uptime: 12h 34m",
        ],
        menu_items=[
            ("[r] Record", 'r'),
            ("[t] Test connection", 't'),
            ("[s] Settings", 's'),
        ],
    )
    if choice != 'q':
        ui.show_info(f"Selected: {choice}", timeout=1)


def demo_commands_list():
    """Read-only command palette demo"""
    ui.show_menu(
        information=[
            "edit <file>    Open file in editor",
            "run <file>     Execute script",
            "test           Run all tests",
            "deploy         Push to production",
            "clean          Remove temporary files",
        ],
        prompt="❯  Press q to go back",
        menu_items=[
            ("[q] Go back", 'q'),
        ],
    )


def demo_text_input():
    """Text input prompt demo"""
    name = ui.show_input(
        prompt="Enter your name:",
        information=["Type your name and press enter"],
    )
    if name and name != 'q':
        ui.show_info(f"Hello, {name}!", timeout=2)


def demo_notifications():
    """Error, info, and confirmation notifications"""
    ui.show_info("This is an info message", timeout=1.5)

    choice = ui.show_confirmation("Would you like to see an error?")
    if choice == 'y':
        ui.show_error("Something went wrong!\nError code: 42", timeout=2)

    ui.show_goodbye()


def demo_countdown():
    """Countdown timer demo"""
    ui.show_countdown(
        title="Launching in",
        seconds=3,
        extra_info=["Get ready!"],
    )
    ui.show_info("Blast off!", timeout=1.5)


if __name__ == "__main__":
    main()
