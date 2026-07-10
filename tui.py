#!/usr/bin/env python3
"""
tui - A unified TUI library for beautiful terminal interfaces
"""

import curses
import time
from typing import List, Tuple, Optional, Callable, Dict, Any


class Theme:
    """Color theme configuration"""
    
    def __init__(self, name: str = "blue"):
        self.name = name
    
    def _init_colors(self):
        """Initialize color pairs based on theme"""
        curses.start_color()
        curses.use_default_colors()
        
        if self.name == "blue":
            curses.init_pair(1, 39, -1)   # Bright blue
            curses.init_pair(2, 33, -1)   # Medium-bright blue
            curses.init_pair(3, 27, -1)   # Medium blue
            curses.init_pair(4, 21, -1)   # Dark blue
            curses.init_pair(5, 19, -1)   # Very dark blue
        elif self.name == "red":
            curses.init_pair(1, 196, -1)  # Bright red
            curses.init_pair(2, 160, -1)  # Medium-bright red
            curses.init_pair(3, 124, -1)  # Medium red
            curses.init_pair(4, 88, -1)   # Dark red
            curses.init_pair(5, 52, -1)   # Very dark red
        elif self.name == "green":
            curses.init_pair(1, 46, -1)   # Bright green
            curses.init_pair(2, 40, -1)   # Medium-bright green
            curses.init_pair(3, 34, -1)   # Medium green
            curses.init_pair(4, 28, -1)   # Dark green
            curses.init_pair(5, 22, -1)   # Very dark green
        
        # Utility colors
        curses.init_pair(11, 241, -1)  # Gray (separators)
        curses.init_pair(12, 179, -1)  # Yellow (highlight)
        curses.init_pair(13, 15, -1)   # White (logs)
        curses.init_pair(14, 196, -1)  # Red (errors)
        curses.init_pair(15, 15, -1)   # White



class Banner:
    """Animated banner component"""
    
    def __init__(self, title: str = "tui", version: str = "v1.0.0", short: bool = True):
        self.title = title
        self.version = version
        self.short = short
    
    def render(self, stdscr) -> List[Tuple[str, int]]:
        """Render banner lines with color pairs"""
        height, width = stdscr.getmaxyx()
        
        def center(text):
            padding = (width - 2 - len(text)) // 2
            return " " * padding + text + " " * (width - 2 - len(text) - padding)
        
        display_text = f"{self.title} {self.version}"
        
        if self.short:
            # 3-line banner
            return [
                ("╭" + "─" * (width - 2) + "╮", 1),
                ("│" + center(display_text) + "│", 3),
                ("╰" + "─" * (width - 2) + "╯", 5),
            ]
        else:
            # 5-line banner
            return [
                ("╭" + "─" * (width - 2) + "╮", 1),
                ("│" + " " * (width - 2) + "│", 2),
                ("│" + center(display_text) + "│", 3),
                ("│" + " " * (width - 2) + "│", 4),
                ("╰" + "─" * (width - 2) + "╯", 5),
            ]
    
    def draw(self, stdscr, y: int = 0):
        """Draw banner at specified y position"""
        lines = self.render(stdscr)
        for i, (line, color_pair) in enumerate(lines):
            try:
                stdscr.addstr(y + i, 0, line, curses.color_pair(color_pair))
            except:
                pass
        return len(lines)


class AnimatedGradient:
    """Animated gradient text component"""
    
    def __init__(self, text: str = "gliddd4"):
        self.text = text
        self.offset = 0
        self.last_update = time.time()
        self.update_interval = 0.1  # 100ms
    
    def update(self):
        """Update animation state"""
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.offset = (self.offset + 1) % 10
            self.last_update = current_time
            return True
        return False
    
    def draw(self, stdscr, y: int, x: int):
        """Draw animated gradient text at position"""
        for i, char in enumerate(self.text):
            color_idx = 1 + ((i + self.offset) % 5)
            try:
                stdscr.addstr(y, x + i, char, curses.color_pair(color_idx))
            except:
                pass


class SelectUI:
    """Bottom sticky select UI component"""
    
    def __init__(self, prompt: str = "❯  Select an option:", show_help: bool = True, branding: str = "gliddd4"):
        self.prompt = prompt
        self.show_help = show_help
        self.selected_key = None
        self.gradient = AnimatedGradient(branding)
    
    def draw(self, stdscr, show_help_mode: bool = False):
        """Draw select UI at bottom of screen"""
        height, width = stdscr.getmaxyx()
        separator = "─" * width
        bottom_y = height - 4
        
        try:
            # Top separator
            stdscr.addstr(bottom_y, 0, separator, curses.color_pair(11))
            
            # Prompt with optional selected key
            prompt_text = self.prompt
            stdscr.addstr(bottom_y + 1, 0, prompt_text)
            
            if self.selected_key:
                key_x = len(prompt_text) + 1
                stdscr.addstr(bottom_y + 1, key_x, self.selected_key, curses.color_pair(12))
            
            # Bottom separator
            stdscr.addstr(bottom_y + 2, 0, separator, curses.color_pair(11))
            
            # Help hint with animated gradient
            if self.show_help:
                if show_help_mode:
                    stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                    stdscr.addstr(bottom_y + 3, 1, "[?] to exit", curses.color_pair(12))
                    stdscr.addstr(bottom_y + 3, 12, " · [q] Quit ", curses.color_pair(15))
                    x_offset = 12 + len(" · [q] Quit ")
                else:
                    stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                    stdscr.addstr(bottom_y + 3, 1, "[?] help", curses.color_pair(15))
                    x_offset = 1 + len("[?] help") + 3
                
                self.gradient.draw(stdscr, bottom_y + 3, x_offset)

        except:
            pass


class Menu:
    """Menu component with sections and items"""
    
    def __init__(self):
        self.sections: List[Dict[str, Any]] = []
    
    def add_section(self, title: Optional[str] = None, items: Optional[List[Tuple[str, str]]] = None):
        """Add a menu section
        
        Args:
            title: Section title (e.g., "Menu:", "Commands:")
            items: List of (display_text, return_value) tuples
        """
        self.sections.append({
            "title": title,
            "items": items or []
        })
    
    def add_text(self, text: str):
        """Add plain text line"""
        if not self.sections or self.sections[-1].get("items"):
            self.sections.append({"title": None, "items": [], "text": [text]})
        else:
            if "text" not in self.sections[-1]:
                self.sections[-1]["text"] = []
            self.sections[-1]["text"].append(text)
    
    def render(self) -> Tuple[List[str], List[Tuple[str, str]], List[str]]:
        """Render menu to display lines, menu items, and valid keys"""
        display_lines = []
        menu_items = []
        valid_keys = []
        
        for section in self.sections:
            # Add section title
            if section.get("title"):
                display_lines.append(section["title"])
            
            # Add section items
            for item_text, return_value in section.get("items", []):
                display_lines.append(item_text)
                menu_items.append((item_text, return_value))
                valid_keys.append(return_value)
            
            # Add plain text
            for text in section.get("text", []):
                display_lines.append(text)
            
            # Add spacing between sections
            if section != self.sections[-1]:
                display_lines.append("")
        
        return display_lines, menu_items, valid_keys


class Window:
    """Main window component that manages the TUI"""
    
    def __init__(self, title: str = "tui", version: str = "v1.0.0", theme: str = "blue", branding: str = "gliddd4"):
        self.title = title
        self.version = version
        self.theme = Theme(theme)
        self.banner = Banner(title, version, short=True)
        self.select_ui = SelectUI(branding=branding)
        self.show_help_mode = False
        self.gradient_offset = 0
        self.last_gradient_time = time.time()
    
    def show(self, blocks: Dict[str, Any], input_mode: bool = False, display_only: bool = False, auto_timeout: float = 0, quit_presses: int = 3) -> Optional[str]:
        """Show window with content blocks
        
        Args:
            blocks: Dict with keys:
                - 'information': List of info text lines
                - 'menu': List of menu item lines
                - 'select_ui': Tuple of ("SELECT_PROMPT", "❯  Prompt text:")
                - 'menu_items': List of (display_text, return_value) tuples
                - 'valid_keys': List of valid key characters
            input_mode: Enable text input mode
            display_only: If True, returns immediately without waiting for input (for countdowns, etc)
            auto_timeout: If > 0, automatically returns after this many seconds
            quit_presses: Number of q presses required to quit (default 3 for main menu, 1 for submenus unless in input mode)
        
        Returns:
            Selected key or input text
        """
        return curses.wrapper(lambda stdscr: self._run(stdscr, blocks, input_mode, display_only, auto_timeout, quit_presses))
    
    def show_countdown(self, title: str, seconds: int, extra_info: list = None):
        """Show countdown in a single curses session (no flicker)

        Args:
            title: Countdown title
            seconds: Number of seconds to count down
            extra_info: Extra information lines
        """
        info_base = [title, ""]
        if extra_info:
            info_base.extend(extra_info)

        def _countdown(stdscr):
            curses.use_default_colors()
            self.theme._init_colors()
            for i in range(seconds, 0, -1):
                blocks = {
                    'information': info_base + [f"{i} seconds..."],
                    'menu': [],
                    'select_ui': ("SELECT_PROMPT", "❯"),
                    'menu_items': [],
                    'valid_keys': []
                }
                self._run(stdscr, blocks, input_mode=False, display_only=True)
                time.sleep(1)

        curses.wrapper(_countdown)

    def show_goodbye(self, timeout: float = 1.0):
        """Show goodbye message
        
        Args:
            timeout: How long to show the message (default 1.0 seconds for main menu, 0.5 for submenus)
        """
        blocks = {
            'information': [],
            'menu': [],
            'select_ui': ("SELECT_PROMPT", "❯  Goodbye!"),
            'menu_items': [],
            'valid_keys': []
        }
        self.show(blocks, display_only=True, auto_timeout=timeout)
    
    def _run(self, stdscr, blocks: Dict[str, Any], input_mode: bool, display_only: bool = False, auto_timeout: float = 0, quit_presses: int = 3):
        """Internal curses main loop"""
        curses.use_default_colors()
        curses.curs_set(0)  # Always start with cursor hidden
        stdscr.clear()
        
        # Track start time for auto_timeout
        start_time = time.time() if auto_timeout > 0 else None
        
        # Initialize theme colors now that we are in curses context
        self.theme._init_colors()
        
        # Extract data from blocks
        information = blocks.get('information', [])
        menu = blocks.get('menu', [])
        select_prompt = blocks.get('select_ui', ("SELECT_PROMPT", "❯  Select an option:"))
        menu_items = blocks.get('menu_items', [])
        valid_keys = blocks.get('valid_keys', [])
        
        if isinstance(select_prompt, tuple):
            self.select_ui.prompt = select_prompt[1]
        
        # Build display lines
        display_lines = []
        if menu:
            for line in menu:
                display_lines.append(line)
        
        if information:
            if display_lines:
                display_lines.append("")
            for line in information:
                display_lines.append(line)
        
        # Input/selection state
        input_buffer = []
        selected_index = -1
        selected_key = None
        
        q_press_count = 0
        # For non-input mode, submenus only need 1 press
        q_press_max = quit_presses if input_mode else 1 if quit_presses < 3 else quit_presses
        q_last_press_time = None
        q_countdown_interval = 0.8  # Time between countdown steps (seconds)
        q_debounce_time = 0.15  # Ignore q presses within 150ms of each other (prevents key repeat)

        
        needs_redraw = True
        last_size = (0, 0)
        last_scroll_time = 0
        scroll_delay = 0.15
        
        # Save original blocks for help mode
        original_blocks = dict(blocks)

        
        while True:
            current_size = stdscr.getmaxyx()
            
            # Update gradient animation
            current_time = time.time()
            if current_time - self.last_gradient_time >= 0.1:
                self.gradient_offset = (self.gradient_offset + 1) % 10
                self.last_gradient_time = current_time
                self.select_ui.gradient.update()
                needs_redraw = True
            
            # Check if we should auto-quit after final q press
            if q_press_count == q_press_max and q_last_press_time is not None:
                if current_time - q_last_press_time >= 0.10:
                    # 0.10 seconds passed since final press - quit
                    return 'q'
            
            # Countdown q_press_count if user stops pressing (for multi-press scenarios)
            if q_press_count > 0 and q_press_count < q_press_max and q_press_max > 1 and q_last_press_time is not None:
                if current_time - q_last_press_time >= q_countdown_interval:
                    q_press_count -= 1
                    if q_press_count == 0:
                        q_last_press_time = None
                    else:
                        q_last_press_time = current_time  # Reset timer for next countdown
                    needs_redraw = True

            
            if current_size != last_size:
                needs_redraw = True
                last_size = current_size
            
            if needs_redraw:
                height, width = stdscr.getmaxyx()
                stdscr.erase()
                
                # Prepare blocks for display
                current_blocks = dict(original_blocks)
                
                # Replace menu block and select_ui if showing help
                if self.show_help_mode:
                    current_blocks['menu'] = [
                        "Help Menu:",
                        "spacebar        select",
                        "enter           select",
                        "letter          select",
                        "scroll          change selection",
                        "arrow key       change selection"
                    ]
                    current_blocks['select_ui'] = ("SELECT_PROMPT", "❯")
                
                # Build display_lines from current blocks
                current_display_lines = []
                if current_blocks.get('menu'):
                    for line in current_blocks['menu']:
                        current_display_lines.append(line)
                
                if current_blocks.get('information') and not self.show_help_mode:
                    if current_display_lines:
                        current_display_lines.append("")
                    for line in current_blocks['information']:
                        current_display_lines.append(line)
                
                # Draw banner
                y = self.banner.draw(stdscr, 0)
                y += 1  # Add spacing after banner
                
                # Draw content
                menu_item_index = 0
                for i, line in enumerate(current_display_lines):
                    if y + i < height - 4:
                        try:
                            # Check if this is a menu item
                            is_menu_item = False
                            if menu_items and isinstance(line, str) and line.startswith("[") and not self.show_help_mode:
                                is_menu_item = menu_item_index < len(menu_items)
                                is_selected = is_menu_item and menu_item_index == selected_index
                                if is_menu_item:
                                    menu_item_index += 1
                            else:
                                is_selected = False
                            
                            # Check if line is a section header
                            is_header = isinstance(line, str) and (line.strip().endswith(":") or line.strip() in ["Menu:", "Help:", "About:"])
                            
                            if is_selected:
                                stdscr.addstr(y + i, 0, line, curses.color_pair(12))
                            elif is_header:
                                stdscr.addstr(y + i, 0, line, curses.A_BOLD)
                            else:
                                stdscr.addstr(y + i, 0, line)
                        except:
                            pass
                
                # Draw select UI
                bottom_y = height - 4
                separator = "─" * width
                
                try:
                    # Top separator
                    stdscr.addstr(bottom_y, 0, separator, curses.color_pair(11))
                    
                    # Prompt with input buffer or selected key
                    if current_blocks.get('select_ui'):
                        select_ui = current_blocks['select_ui']
                        if isinstance(select_ui, tuple) and select_ui[0] == "SELECT_PROMPT":
                            prompt_text = select_ui[1]
                            stdscr.addstr(bottom_y + 1, 0, prompt_text)
                            
                            # Display selected key (not highlighted) or input buffer
                            if selected_key and not input_mode and q_press_count == 0:
                                key_x = len(prompt_text) + 1
                                stdscr.addstr(bottom_y + 1, key_x, selected_key)
                            elif input_mode and q_press_count == 0:
                                input_x = len(prompt_text) + 1
                                stdscr.addstr(bottom_y + 1, input_x, "".join(input_buffer))

                    # Bottom separator
                    stdscr.addstr(bottom_y + 2, 0, separator, curses.color_pair(11))
                    
                    # Help line with [?] help, [q] Quit, and animated gradient
                    if self.show_help_mode:
                        stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                        stdscr.addstr(bottom_y + 3, 1, "[?] to exit", curses.color_pair(12))
                        stdscr.addstr(bottom_y + 3, 12, " · [q] Quit ", curses.color_pair(15))
                        x_offset = 12 + len(" · [q] Quit ")
                    else:
                        # Draw help line components
                        x_pos = 1
                        
                        # [?] help
                        stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                        stdscr.addstr(bottom_y + 3, x_pos, "[?] help", curses.color_pair(15))
                        x_pos += len("[?] help")
                        
                        stdscr.addstr(bottom_y + 3, x_pos, " · ", curses.color_pair(15))
                        x_pos += 3
                        
                        # [q] Quit - show counter and highlight if q_press_count > 0
                        if q_press_count > 0:
                            if q_press_count > 0 and q_press_max > 1:
                                quit_text = f"[{q_press_count}/{q_press_max}] Quit"
                            else:
                                quit_text = "[q] Quit"
                            stdscr.addstr(bottom_y + 3, x_pos, quit_text, curses.color_pair(12))
                        else:
                            quit_text = "[q] Quit"
                            stdscr.addstr(bottom_y + 3, x_pos, quit_text, curses.color_pair(15))
                        
                        x_pos += len(quit_text)
                        x_offset = x_pos + 2  # Add some padding
                    
                    # Draw animated gradient
                    if x_offset + len(self.select_ui.gradient.text) < width:
                        self.select_ui.gradient.draw(stdscr, bottom_y + 3, x_offset)
                    
                    # Set cursor position if in input mode
                    if input_mode:
                        try:
                            if curses.curs_set(1):
                                input_x = len(prompt_text) + 1
                                stdscr.move(bottom_y + 1, input_x + len(input_buffer))
                        except:
                            pass
                    
                    # Hide cursor unless in input mode with buffer
                    if not input_mode or len(input_buffer) == 0:
                        curses.curs_set(0)


                except:
                    pass
                
                stdscr.refresh()
                needs_redraw = False
                
                # If display_only mode, return after first draw
                if display_only:
                    return None
            
            # Check auto_timeout
            if auto_timeout > 0 and start_time and (time.time() - start_time) >= auto_timeout:
                return None
            
            # Handle input
            # Always use short timeout to keep animations running
            stdscr.timeout(50)
            try:
                key = stdscr.getch()
                
                # Reset q press count if a different key is pressed
                if key >= 32 and key < 127 and chr(key) != 'q':
                    if q_press_count > 0:
                        q_press_count = 0
                        q_last_press_time = None
                        needs_redraw = True
                if key == curses.KEY_RESIZE:
                    needs_redraw = True
                    continue
                elif key == 3 or key == 27:  # Ctrl+C or ESC
                    return 'q' if not input_mode else None

                elif key == ord('?') and self.show_help_mode:
                    # Exit help mode (no flash, just toggle)
                    self.show_help_mode = False
                    needs_redraw = True
                    continue
                elif key == ord('?'):
                    # Enter help mode (no flash, just toggle)
                    self.show_help_mode = True
                    needs_redraw = True
                    continue
                elif menu_items and not self.show_help_mode:
                    # Arrow key navigation
                    if key == curses.KEY_UP:
                        current_time = time.time()
                        if current_time - last_scroll_time >= scroll_delay:
                            if selected_index == -1:
                                selected_index = len(menu_items) - 1
                            else:
                                selected_index = selected_index - 1
                                if selected_index < 0:
                                    selected_index = -1
                            selected_key = menu_items[selected_index][1] if selected_index >= 0 else None
                            needs_redraw = True
                            last_scroll_time = current_time
                    elif key == curses.KEY_DOWN:
                        current_time = time.time()
                        if current_time - last_scroll_time >= scroll_delay:
                            if selected_index == -1:
                                selected_index = 0
                            else:
                                selected_index = selected_index + 1
                                if selected_index >= len(menu_items):
                                    selected_index = -1
                            selected_key = menu_items[selected_index][1] if selected_index >= 0 else None
                            needs_redraw = True
                            last_scroll_time = current_time
                    elif key == ord('\n') or key == ord(' '):
                        if input_mode:
                            if key == ord(' '):
                                input_buffer.append(' ')
                                needs_redraw = True
                            else:
                                return "".join(input_buffer)
                        else:
                            if selected_index >= 0:
                                # Flash before returning
                                self._show_flash(stdscr, selected_key, display_lines, menu_items, selected_index, height, width, False)
                                return menu_items[selected_index][1]
                    elif input_mode:
                        if key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                            if input_buffer:
                                input_buffer.pop()
                                needs_redraw = True

                        elif key >= 32 and key < 127:
                            char = chr(key)
                            if char == "q" and "q" in valid_keys:
                                # Increment q press count with debounce
                                current_time = time.time()
                                if q_last_press_time is None or (current_time - q_last_press_time) >= q_debounce_time:
                                    if q_press_count < q_press_max:  # Cap at max
                                        q_press_count += 1
                                    q_last_press_time = current_time
                                    needs_redraw = True
                            elif char in valid_keys:
                                # Cancel quit and execute other command
                                q_press_count = 0
                                q_last_press_time = None
                                return char
                            else:
                                # Cancel quit and add to input
                                q_press_count = 0
                                q_last_press_time = None
                                input_buffer.append(char)
                                needs_redraw = True
                    elif key != -1:
                        char = chr(key) if key < 256 else None
                        if char and char in valid_keys:
                            if char == "q":
                                # Increment q press count with debounce
                                current_time = time.time()
                                if q_last_press_time is None or (current_time - q_last_press_time) >= q_debounce_time:
                                    if q_press_count < q_press_max:  # Cap at max
                                        q_press_count += 1
                                    q_last_press_time = current_time
                                    # If this is a single-press quit (submenu), return immediately (no flash)
                                    if q_press_count == q_press_max and q_press_max == 1:
                                        return char
                                    needs_redraw = True
                            else:
                                selected_key = char
                                for idx, (_, return_value) in enumerate(menu_items):
                                    if return_value == char:
                                        selected_index = idx
                                        break
                                self._show_flash(stdscr, char, display_lines, menu_items, selected_index, height, width, False)
                                return char

                elif input_mode and key != -1:
                    if key == ord('\n'):
                        return "".join(input_buffer)
                    elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                        if input_buffer:
                            input_buffer.pop()
                            needs_redraw = True
                    elif key >= 32 and key < 127:
                        char = chr(key)
                        
                        if char == "q" and "q" in valid_keys:
                            # Increment q press count with debounce
                            current_time = time.time()
                            if q_last_press_time is None or (current_time - q_last_press_time) >= q_debounce_time:
                                if q_press_count < q_press_max:  # Cap at max
                                    q_press_count += 1
                                q_last_press_time = current_time
                                needs_redraw = True
                        elif char in valid_keys:
                            q_press_count = 0
                            q_last_press_time = None
                            return char
                        else:
                            q_press_count = 0
                            q_last_press_time = None
                            input_buffer.append(char)
                            needs_redraw = True


            except KeyboardInterrupt:
                return 'q' if not input_mode else None
            except:
                pass
    
    def _show_flash(self, stdscr, char: str, display_lines: List[str], menu_items: List[Tuple[str, str]], 
                    selected_index: int, height: int, width: int, is_help_mode: bool):
        """Show flash effect when key is selected"""
        stdscr.erase()
        
        # Redraw banner
        banner = self.banner.render(stdscr)
        for i, (line, color_pair) in enumerate(banner):
            try:
                stdscr.addstr(i, 0, line, curses.color_pair(color_pair))
            except:
                pass
        
        # Determine which content to show
        if is_help_mode:
            # Showing help content
            content_lines = [
                "Help:",
                "spacebar        select",
                "enter           select",
                "letter          select",
                "scroll          change selection",
                "arrow key       change selection"
            ]
        else:
            content_lines = display_lines
        
        # Redraw content
        y_content = len(banner) + 1
        menu_item_idx = 0
        for i, line in enumerate(content_lines):
            if y_content + i < height - 4:
                try:
                    is_menu_item = False
                    if menu_items and isinstance(line, str) and line.startswith("[") and not is_help_mode:
                        is_menu_item = menu_item_idx < len(menu_items)
                        is_selected = is_menu_item and menu_item_idx == selected_index
                        if is_menu_item:
                            menu_item_idx += 1
                    else:
                        is_selected = False
                    
                    is_header = isinstance(line, str) and (line.strip().endswith(":") or line.strip() in ["Menu:", "Help:", "About:"])
                    
                    if is_selected:
                        stdscr.addstr(y_content + i, 0, line, curses.color_pair(12))
                    elif is_header:
                        stdscr.addstr(y_content + i, 0, line, curses.A_BOLD)
                    else:
                        stdscr.addstr(y_content + i, 0, line)
                except:
                    pass
        
        # Redraw select UI with highlighted key
        separator = "─" * width
        bottom_y = height - 4
        
        try:
            stdscr.addstr(bottom_y, 0, separator, curses.color_pair(11))
            
            # Show prompt with highlighted key
            if char == "?":
                # For help mode transitions, always show full prompt with ?
                prompt_text = f"❯  Select an option: {char}"
                base_prompt = "❯  Select an option:"
            elif is_help_mode:
                # In help mode, use the help prompt
                prompt_text = f"❯: {char}"
                base_prompt = "❯:"
            else:
                # Normal mode, use current prompt
                prompt_text = f"{self.select_ui.prompt.split(':')[0]}: {char}"
                base_prompt = self.select_ui.prompt.split(':')[0] + ":"
            stdscr.addstr(bottom_y + 1, 0, base_prompt + " ")
            key_x = len(base_prompt) + 1
            stdscr.addstr(bottom_y + 1, key_x, char, curses.color_pair(12))
            
            stdscr.addstr(bottom_y + 2, 0, separator, curses.color_pair(11))
            
            # Draw hint with animated gradient
            if is_help_mode:
                stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                stdscr.addstr(bottom_y + 3, 1, "[?] to exit", curses.color_pair(12))
                stdscr.addstr(bottom_y + 3, 12, " · [q] Quit ", curses.color_pair(15))
                x_offset = 12 + len(" · [q] Quit ")
            else:
                stdscr.addstr(bottom_y + 3, 0, " ", curses.color_pair(15))
                stdscr.addstr(bottom_y + 3, 1, "[?] help", curses.color_pair(15))
                x_offset = 1 + len("[?] help") + 3
            
            self.select_ui.gradient.draw(stdscr, bottom_y + 3, x_offset)
        except:
            pass
        
        stdscr.refresh()
        time.sleep(0.15)  # Flash for 150ms


# Convenience functions
def show_menu(title: str, version: str, blocks: Dict[str, Any], theme: str = "blue", branding: str = "gliddd4") -> Optional[str]:
    """Show a menu window
    
    Args:
        title: Window title
        version: Version string
        blocks: Content blocks dict
        theme: Color theme ("blue", "red", "green")
        branding: Animated gradient text (default: "gliddd4")
    
    Returns:
        Selected key or None
    """
    window = Window(title, version, theme, branding)
    return window.show(blocks)

def show_input(title: str, version: str, prompt: str, theme: str = "blue", branding: str = "gliddd4") -> Optional[str]:
    """Show an input window
    
    Args:
        title: Window title
        version: Version string
        prompt: Input prompt text
        theme: Color theme
        branding: Animated gradient text (default: "gliddd4")
    
    Returns:
        Input text or None
    """
    blocks = {
        'select_ui': ("SELECT_PROMPT", f"❯  {prompt}"),
        'menu_items': [],
        'valid_keys': []
    }
    window = Window(title, version, theme, branding)
    return window.show(blocks, input_mode=True)


# Helper functions for common UI patterns
class TUIHelper:
    """Helper class for common TUI patterns"""
    
    def __init__(self, title: str = "tui", version: str = "v1.0.0", theme: str = "blue", branding: str = "gliddd4"):
        self.title = title
        self.version = version
        self.theme = theme
        self.branding = branding
    
    def show_error(self, message: str, timeout: float = 2):
        """Show an error message with auto-timeout"""
        blocks = {
            'information': [message] if isinstance(message, str) else message,
            'menu': [],
            'select_ui': ("SELECT_PROMPT", "❯"),
            'menu_items': [],
            'valid_keys': []
        }
        window = Window(self.title, self.version, self.theme, self.branding)
        window.show(blocks, auto_timeout=timeout)
    
    def show_info(self, message: str, timeout: float = 3):
        """Show an info message with auto-timeout"""
        blocks = {
            'information': [message] if isinstance(message, str) else message,
            'menu': [],
            'select_ui': ("SELECT_PROMPT", "❯"),
            'menu_items': [],
            'valid_keys': []
        }
        window = Window(self.title, self.version, self.theme, self.branding)
        window.show(blocks, auto_timeout=timeout)
    
    def show_confirmation(self, message: str, default: str = 'y') -> str:
        """Show a yes/no confirmation dialog"""
        menu_items = [
            ("[y] Yes" + (" (default)" if default == 'y' else ""), 'y'),
            ("[n] No" + (" (default)" if default == 'n' else ""), 'n'),
        ]
        
        blocks = {
            'information': [message] if isinstance(message, str) else message,
            'menu': [
                "Menu:",
                menu_items[0][0],
                menu_items[1][0],
            ],
            'select_ui': ("SELECT_PROMPT", "❯  Select an option:"),
            'menu_items': menu_items,
            'valid_keys': ['y', 'n', '\n', 'q']
        }
        
        window = Window(self.title, self.version, self.theme, self.branding)
        choice = window.show(blocks)

        
        if choice == '\n' or choice is None:
            return default
        return choice
    
    def show_goodbye(self, is_main_menu: bool = False):
        """Show goodbye message
        
        Args:
            is_main_menu: If True, show for 1 second. If False (submenu), show for 0.5 seconds
        """
        timeout = 1.0 if is_main_menu else 0.5
        window = Window(self.title, self.version, self.theme, self.branding)
        window.show_goodbye(timeout)
    
    def show_menu(self, information: list, menu_items: list, prompt: str = "❯  Select an option:", valid_keys: list = None, menu_title: str = "Menu:", quit_presses: int = 2) -> str:
        """Show a simple menu with information and menu items
        
        Args:
            information: List of info text lines
            menu_items: List of (display_text, return_value) tuples
            prompt: Select UI prompt text
            valid_keys: List of valid key chars (auto-generated from menu_items if None)
            menu_title: Title for the menu section (default: "Menu:")
            quit_presses: Number of q presses required to quit (default: 2 for submenus, use 3 for main menu)
        
        Returns:
            Selected key
        """
        if valid_keys is None:
            valid_keys = [item[1] for item in menu_items]
        
        # Always add 'q' to valid_keys for quitting (unless it's already there)
        if 'q' not in valid_keys:
            valid_keys.append('q')
        
        menu_lines = [menu_title]
        for item_text, _ in menu_items:
            menu_lines.append(item_text)
        
        blocks = {
            'information': information,
            'menu': menu_lines,
            'select_ui': ("SELECT_PROMPT", prompt),
            'menu_items': menu_items,
            'valid_keys': valid_keys
        }
        
        window = Window(self.title, self.version, self.theme, self.branding)
        return window.show(blocks, quit_presses=quit_presses)

    
    def show_input(self, prompt: str, information: list = None, quit_key: str = 'q', menu_title: str = "Menu:") -> str:
        """Show an input prompt
        
        Args:
            prompt: Input prompt text
            information: Optional info text lines
            quit_key: Key to quit (default: 'q')
            menu_title: Title for the menu section (default: "Menu:")
        
        Returns:
            Input text or None
        """
        blocks = {
            'information': information or [],
            'menu': [menu_title],
            'select_ui': ("SELECT_PROMPT", f"❯  {prompt}"),
            'menu_items': [],
            'valid_keys': [quit_key]
        }
        
        window = Window(self.title, self.version, self.theme, self.branding)
        return window.show(blocks, input_mode=True, quit_presses=2)

    
    def show_countdown(self, title: str, seconds: int, extra_info: list = None):
        """Show a countdown timer (single curses session, no flicker)
        
        Args:
            title: Countdown title
            seconds: Number of seconds to count down
            extra_info: Extra information lines to show
        """
        window = Window(self.title, self.version, self.theme, self.branding)
        window.show_countdown(title, seconds, extra_info)