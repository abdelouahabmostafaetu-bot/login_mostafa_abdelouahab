#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN — TUI Display Manager                  ║
║              By: Abdelouahab Mostafa                         ║
║              Mathematician · Hacker                          ║
╚══════════════════════════════════════════════════════════════╝

A beautiful TUI login manager inspired by ly.
Personalized with elite hacker / mathematician aesthetics.

Usage:
  python3 am_login.py [--demo] [--skip-intro] [--theme THEME]
                      [--anim ANIM] [--config FILE]
"""

import argparse
import curses
import locale
import os
import signal
import sys
import time

# Ensure src is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.themes import Theme
from src.animations import AnimationEngine
from src.ui import UIComponents
from src.auth import get_authenticator
from src.sessions import SessionManager

# ═══════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════

VERSION = "1.0.0"
AUTHOR = "Abdelouahab Mostafa"
APP_NAME = "AM-Login"

ANIMATION_TYPES = [
    "matrix", "starfield", "fire", "wave", "rain",
    "dna", "cyber", "glitch", "math", "name", "none",
]

THEME_NAMES = ["cyber", "ocean", "forest", "sunset", "neon", "blood", "ice"]


class AMLogin:
    """Main AM-Login application."""

    def __init__(self, stdscr, args):
        self.stdscr = stdscr
        self.args = args
        self.running = True

        # Init curses
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self.stdscr.timeout(33)  # ~30 FPS
        self.stdscr.keypad(True)

        # Locale (for Unicode)
        try:
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            pass

        # Load config
        self.config = Config(args.config)

        # Apply CLI overrides
        if args.theme:
            self.config.parser.set("General", "theme", args.theme)
        if args.anim:
            self.config.parser.set("General", "animation", args.anim)

        # Theme
        self.theme = Theme(self.config.theme)
        self.theme.init_colors()
        self.theme_index = THEME_NAMES.index(self.config.theme) if self.config.theme in THEME_NAMES else 0

        # Animation
        self.anim_engine = AnimationEngine(self.stdscr, self.theme)
        self.anim_type = self.config.animation
        self.anim_index = ANIMATION_TYPES.index(self.anim_type) if self.anim_type in ANIMATION_TYPES else 0

        # UI
        self.ui = UIComponents(self.stdscr, self.theme, self.config)

        # Auth
        self.auth = get_authenticator(demo_mode=args.demo)

        # Sessions
        self.sessions = SessionManager(preferred_type=self.config.preferred_session_type)

        # State
        self.frame = 0
        self.username = ""
        self.password = ""
        self.active_field = 0  # 0=user, 1=pass, 2=session
        self.message = ""
        self.message_type = "normal"
        self.message_time = 0
        self.attempt_count = 0
        self.locked_until = 0
        self.show_help = False
        self.show_power = False
        self.power_selected = 0
        self.show_clock = self.config.show_clock
        self.show_portrait = self.config.show_portrait

    def run(self):
        """Main application loop."""
        # Welcome animation
        if not self.args.skip_intro:
            try:
                self.ui.draw_welcome_animation()
                time.sleep(0.5)
            except Exception:
                pass

        while self.running:
            try:
                self._tick()
            except KeyboardInterrupt:
                if self.args.demo:
                    self.running = False
                    break

    def _tick(self):
        """Single frame of the main loop."""
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()

        # Check lockout
        if self.locked_until > 0:
            remaining = int(self.locked_until - time.time())
            if remaining > 0:
                self.anim_engine.render(self.anim_type, self.frame)
                self.ui.draw_lockout_screen(remaining)
                self.stdscr.refresh()
                self.frame += 1
                self.stdscr.getch()
                return
            else:
                self.locked_until = 0
                self.attempt_count = 0

        # Background animation
        self.anim_engine.render(self.anim_type, self.frame)

        if self.show_help:
            self.ui.draw_help_screen()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            if key != -1:
                self.show_help = False
            self.frame += 1
            return

        if self.show_power:
            self.anim_engine.render(self.anim_type, self.frame)
            opts = self.ui.draw_power_menu(self.power_selected)
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self._handle_power_input(key, opts)
            self.frame += 1
            return

        # Layout
        y = 0
        if self.show_clock:
            y = self.ui.draw_clock(y=1)

        if self.show_portrait and h > 30:
            y = self.ui.draw_identity_card(y=y, frame=self.frame)

        # Login box
        box_y = max(y, (h - 14) // 2)
        self.ui.draw_login_box(
            y=box_y,
            username=self.username,
            password=self.password,
            session_name=self.sessions.current.name,
            active_field=self.active_field,
            message=self.message if time.time() - self.message_time < 5 else "",
            message_type=self.message_type,
            attempt_count=self.attempt_count,
            frame=self.frame,
        )

        # System info (bottom-left)
        self.ui.draw_sysinfo()

        # Branding (bottom-center)
        self.ui.draw_branding_animated(y=h - 3, frame=self.frame)

        self.stdscr.refresh()
        self.frame += 1

        # Input
        key = self.stdscr.getch()
        if key != -1:
            self._handle_input(key)

    def _handle_input(self, key):
        """Process key input."""
        # F-keys
        if key == curses.KEY_F1:
            self.show_help = not self.show_help
            return
        if key == curses.KEY_F2:
            self.show_power = True
            self.power_selected = 0
            return
        if key == curses.KEY_F3:
            self._cycle_animation()
            return
        if key == curses.KEY_F4:
            self._cycle_theme()
            return
        if key == curses.KEY_F5:
            self.show_clock = not self.show_clock
            return

        # Esc or Ctrl+C in demo
        if key == 27:
            if self.args.demo:
                self.running = False
            return

        # Tab / Shift-Tab
        if key == 9:  # Tab
            self.active_field = (self.active_field + 1) % 3
            return
        if key == curses.KEY_BTAB:  # Shift-Tab
            self.active_field = (self.active_field - 1) % 3
            return

        # Arrow keys on session field
        if self.active_field == 2:
            if key == curses.KEY_LEFT:
                self.sessions.prev()
                return
            if key == curses.KEY_RIGHT:
                self.sessions.next()
                return

        # Enter
        if key in (curses.KEY_ENTER, 10, 13):
            if self.active_field == 0 and self.username:
                self.active_field = 1
            elif self.active_field == 1:
                self._do_login()
            elif self.active_field == 2:
                self.active_field = 0
            return

        # Backspace
        if key in (curses.KEY_BACKSPACE, 127, 8):
            if self.active_field == 0:
                self.username = self.username[:-1]
            elif self.active_field == 1:
                self.password = self.password[:-1]
            return

        # Character input
        if 32 <= key <= 126:
            ch = chr(key)
            if self.active_field == 0:
                if len(self.username) < 32:
                    self.username += ch
            elif self.active_field == 1:
                if len(self.password) < 64:
                    self.password += ch

    def _handle_power_input(self, key, opts):
        """Handle input in power menu."""
        if key == curses.KEY_UP:
            self.power_selected = max(0, self.power_selected - 1)
        elif key == curses.KEY_DOWN:
            self.power_selected = min(len(opts) - 1, self.power_selected + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            _, cmd = opts[self.power_selected]
            if cmd is None:
                self.show_power = False
                return
            if self.args.demo:
                self.message = f"Demo: would run '{cmd}'"
                self.message_type = "warning"
                self.message_time = time.time()
                self.show_power = False
                return
            os.system(cmd)
        elif key == 27 or key == curses.KEY_F2:
            self.show_power = False

    def _do_login(self):
        """Attempt authentication."""
        if not self.username:
            self.message = "Username required"
            self.message_type = "error"
            self.message_time = time.time()
            return

        result = self.auth.authenticate(self.username, self.password)

        if result.success:
            self.message = result.message
            self.message_type = "success"
            self.message_time = time.time()

            # Brief success display
            self._show_success()

            if self.args.demo:
                self.running = False
                return

            # Launch session
            session = self.sessions.current
            self.sessions.launch(session, self.username)
        else:
            self.attempt_count += 1
            self.message = result.message
            self.message_type = "error"
            self.message_time = time.time()
            self.password = ""

            # Lockout
            if self.attempt_count >= self.config.max_attempts:
                self.locked_until = time.time() + self.config.lockout_duration

    def _show_success(self):
        """Flash success for a moment."""
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        cy = h // 2

        lines = [
            f"✓ Welcome, {self.username}!",
            f"  Starting {self.sessions.current.name}...",
        ]
        for i, line in enumerate(lines):
            x = max(0, (w - len(line)) // 2)
            y = cy - 1 + i
            if 0 <= y < h:
                try:
                    self.stdscr.addstr(y, x, line, self.theme.highlight)
                except curses.error:
                    pass
        self.stdscr.refresh()
        time.sleep(1.5)

    def _cycle_animation(self):
        """Cycle to next animation type."""
        self.anim_index = (self.anim_index + 1) % len(ANIMATION_TYPES)
        self.anim_type = ANIMATION_TYPES[self.anim_index]
        self.message = f"Animation: {self.anim_type}"
        self.message_type = "normal"
        self.message_time = time.time()

    def _cycle_theme(self):
        """Cycle to next theme."""
        self.theme_index = (self.theme_index + 1) % len(THEME_NAMES)
        name = THEME_NAMES[self.theme_index]
        self.theme = Theme(name)
        self.theme.init_colors()
        self.anim_engine = AnimationEngine(self.stdscr, self.theme)
        self.ui = UIComponents(self.stdscr, self.theme, self.config)
        self.message = f"Theme: {name}"
        self.message_type = "normal"
        self.message_time = time.time()


# ═══════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════

def parse_args():
    p = argparse.ArgumentParser(
        prog="am_login",
        description=f"{APP_NAME} v{VERSION} — TUI Display Manager by {AUTHOR}",
    )
    p.add_argument("--version", action="version", version=f"{APP_NAME} v{VERSION} by {AUTHOR}")
    p.add_argument("--demo", action="store_true", help="Run in demo mode (no real auth)")
    p.add_argument("--skip-intro", action="store_true", help="Skip the welcome animation")
    p.add_argument("--theme", choices=THEME_NAMES, help="Color theme")
    p.add_argument("--anim", choices=ANIMATION_TYPES, help="Background animation")
    p.add_argument("--config", default=None, help="Path to config file")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Only ignore SIGINT in production (non-demo) mode
    if not args.demo:
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    # Ensure TERM is set (fixes curses init on some terminals/TTYs)
    if not os.environ.get("TERM"):
        os.environ["TERM"] = "xterm-256color"

    try:
        curses.wrapper(lambda stdscr: AMLogin(stdscr, args).run())
    except KeyboardInterrupt:
        pass
    except curses.error as e:
        print(f"\n{APP_NAME}: Terminal error — {e}", file=sys.stderr)
        print("  Make sure your terminal supports curses (try: export TERM=xterm-256color)", file=sys.stderr)
        sys.exit(1)
    finally:
        print(f"\n{APP_NAME} v{VERSION} — Goodbye!")
