#!/usr/bin/env python3
"""
Test script for gliddd library
"""

import tui

def test_simple_menu():
    """Test: Simple menu with options"""
    print("\n=== Test 1: Simple Menu ===")
    
    blocks = {
        'menu': [
            "Menu:",
            "[1] First option",
            "[2] Second option",
            "[3] Third option",
            "[q] Quit",
        ],
        'select_ui': ("SELECT_PROMPT", "❯  Select an option:"),
        'menu_items': [
            ("[1] First option", '1'),
            ("[2] Second option", '2'),
            ("[3] Third option", '3'),
            ("[q] Quit", 'q'),
        ],
        'valid_keys': ['1', '2', '3', 'q'],
    }
    
    choice = tui.show_menu("test", "v1.0.0", blocks, theme="blue")
    print(f"✓ Selected: {choice}")
    return choice


def test_menu_with_info():
    """Test: Menu with information block"""
    print("\n=== Test 2: Menu with Information ===")
    
    blocks = {
        'menu': [
            "Menu:",
            "[r] Record",
            "[t] Test",
            "[q] Quit",
        ],
        'information': [
            "Status: Ready",
            "Config: /Users/jb/config",
            "Buttons: 5/8 configured",
        ],
        'select_ui': ("SELECT_PROMPT", "❯  Select an option:"),
        'menu_items': [
            ("[r] Record", 'r'),
            ("[t] Test", 't'),
            ("[q] Quit", 'q'),
        ],
        'valid_keys': ['r', 't', 'q'],
    }
    
    choice = tui.show_menu("remote", "v1.0.0", blocks, theme="red")
    print(f"✓ Selected: {choice}")
    return choice


def test_commands_list():
    """Test: Commands list (like dev.sh help)"""
    print("\n=== Test 3: Commands List ===")
    
    blocks = {
        'menu': [
            "Commands:",
            "edit <file> - Edit with syntax check",
            "run <file>  - Execute script",
            "test        - Run all tests",
        ],
        'select_ui': ("SELECT_PROMPT", "❯  Press q to exit"),
        'menu_items': [],
        'valid_keys': ['q'],
    }
    
    choice = tui.show_menu("dev", "v1.0.0", blocks, theme="blue")
    print(f"✓ Exited")
    return choice


def test_input():
    """Test: Input prompt"""
    print("\n=== Test 4: Input Prompt ===")
    
    result = tui.show_input("test", "v1.0.0", "Enter your name:", theme="green")
    print(f"✓ You entered: {result}")
    return result


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("tui Library Tests")
    print("=" * 50)
    
    tests = [
        test_simple_menu,
        test_menu_with_info,
        test_commands_list,
        test_input,
    ]
    
    for test in tests:
        try:
            result = test()
            if result == 'q':
                print("Exited test")
                break
        except KeyboardInterrupt:
            print("\n\nTests interrupted by user")
            break
        except Exception as e:
            print(f"✗ Test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Tests complete!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()