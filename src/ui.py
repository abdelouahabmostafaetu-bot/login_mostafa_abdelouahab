#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN UI Components                          ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝

Professional TUI: login box, ASCII portrait, math identity,
system info, clock, logo, power menu — elegant hacker aesthetic.
"""

import curses
import math
import os
import time
import platform

# ═══════════════════════════════════════════════════════════════
# ASCII ART LOGO (clean, sharp)
# ═══════════════════════════════════════════════════════════════

LOGO_ART = [
    "   █████╗ ███╗   ███╗      ██╗      ██████╗  ██████╗ ██╗███╗   ██╗",
    "  ██╔══██╗████╗ ████║      ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║",
    "  ███████║██╔████╔██║█████╗██║     ██║   ██║██║  ███╗██║██╔██╗ ██║",
    "  ██╔══██║██║╚██╔╝██║╚════╝██║     ██║   ██║██║   ██║██║██║╚██╗██║",
    "  ██║  ██║██║ ╚═╝ ██║      ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║",
    "  ╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝",
]

MINI_LOGO = [
    " ▄▀█ █▀▄▀█ ░ █░░ █▀█ █▀▀ █ █▄░█",
    " █▀█ █░▀░█ ▄ █▄▄ █▄█ █▄█ █ █░▀█",
]

# ═══════════════════════════════════════════════════════════════
# ASCII PORTRAIT — Mathematician / Hacker identity
# ═══════════════════════════════════════════════════════════════

PORTRAIT_ART = [
    "        ┌─────────────┐",
    "        │  ██╗  ██╗   │",
    "        │  ╚██╗██╔╝   │",
    "        │   ╚███╔╝    │",
    "        │   ██╔██╗    │",
    "        │  ██╔╝ ██╗   │",
    "        │  ╚═╝  ╚═╝   │",
    "        │    ┌──┐     │",
    "        │   ─┘  └─    │",
    "        └─────────────┘",
]

IDENTITY_CARD = [
    "╔══════════════════════════════════════════════════╗",
    "║  ┌──────────┐                                   ║",
    "║  │ ▓▓▓▓▓▓▓▓ │  Abdelouahab Mostafa              ║",
    "║  │ ▓▓ ◉◉ ▓▓ │  ────────────────────              ║",
    "║  │ ▓▓▓▓▓▓▓▓ │  ◈ Mathematician                   ║",
    "║  │ ▓▓ ── ▓▓ │  ◈ Hacker · Developer              ║",
    "║  │ ▓▓▓▓▓▓▓▓ │  ◈ AM-Login Creator                ║",
    "║  └──────────┘  ◈ System Architect                ║",
    "╚══════════════════════════════════════════════════╝",
]

MATH_QUOTE = "« Abdelouahab Mostafa · Mathematician · Hacker »"

BRANDING_FRAMES = [
    "✦  Abdelouahab Mostafa · Mathematician  ✦",
    "✧  Abdelouahab Mostafa · Mathematician  ✧",
    "⊹  Abdelouahab Mostafa · Mathematician  ⊹",
]


class UIComponents:
    """Elegant TUI rendering components."""

    def __init__(self, stdscr, theme, config):
        self.stdscr = stdscr
        self.theme = theme
        self.config = config
        self.height, self.width = stdscr.getmaxyx()

    def update_size(self):
        self.height, self.width = self.stdscr.getmaxyx()

    def cx(self, text_len):
        return max(0, (self.width - text_len) // 2)

    # ═══════════════════════════════════════════════════
    # LOGO
    # ═══════════════════════════════════════════════════

    def draw_logo(self, y_offset=0):
        self.update_size()
        logo = LOGO_ART if self.width >= 72 else MINI_LOGO
        sy = 1 + y_offset
        for i, line in enumerate(logo):
            x = self.cx(len(line))
            y = sy + i
            if 0 <= y < self.height:
                try:
                    self.stdscr.addstr(y, x, line, self.theme.logo)
                except curses.error:
                    pass
        return sy + len(logo) + 1

    # ═══════════════════════════════════════════════════
    # IDENTITY CARD (portrait + math info)
    # ═══════════════════════════════════════════════════

    def draw_identity_card(self, y=None, frame=0):
        """Draw the mathematician identity card with portrait."""
        self.update_size()
        if y is None:
            y = 2

        for i, line in enumerate(IDENTITY_CARD):
            x = self.cx(len(line))
            dy = y + i
            if 0 <= dy < self.height:
                try:
                    if i == 0 or i == len(IDENTITY_CARD) - 1:
                        # Border: glow effect
                        glow = math.sin(frame * 0.08 + i) * 0.5 + 0.5
                        attr = self.theme.highlight if glow > 0.6 else self.theme.border
                    elif "Abdelouahab Mostafa" in line:
                        attr = self.theme.highlight
                    elif "◈" in line:
                        attr = self.theme.accent
                    elif "▓" in line or "◉" in line:
                        attr = self.theme.anim_primary
                    else:
                        attr = self.theme.border
                    self.stdscr.addstr(dy, x, line, attr)
                except curses.error:
                    pass

        return y + len(IDENTITY_CARD) + 1

    # ═══════════════════════════════════════════════════
    # BRANDING (animated glow)
    # ═══════════════════════════════════════════════════

    def draw_branding_animated(self, y=None, frame=0):
        self.update_size()
        if y is None:
            y = self.height - 3

        # Animated branding text
        idx = (frame // 8) % len(BRANDING_FRAMES)
        text = BRANDING_FRAMES[idx]
        x = self.cx(len(text))

        if 0 <= y < self.height:
            glow = math.sin(frame * 0.06) * 0.5 + 0.5
            if glow > 0.7:
                attr = self.theme.highlight
            elif glow > 0.3:
                attr = self.theme.anim_primary | curses.A_BOLD
            else:
                attr = self.theme.accent
            try:
                self.stdscr.addstr(y, x, text, attr)
            except curses.error:
                pass

        # Math quote below
        if 0 <= y + 1 < self.height and self.width > len(MATH_QUOTE):
            qx = self.cx(len(MATH_QUOTE))
            try:
                self.stdscr.addstr(y + 1, qx, MATH_QUOTE, self.theme.accent | curses.A_DIM)
            except curses.error:
                pass

    # ═══════════════════════════════════════════════════
    # CLOCK (elegant digital)
    # ═══════════════════════════════════════════════════

    def draw_clock(self, y=None):
        self.update_size()
        if self.config.clock_format == "12h":
            ts = time.strftime("%I:%M:%S %p")
        else:
            ts = time.strftime("%H:%M:%S")
        ds = time.strftime("%A, %B %d, %Y")

        if y is None:
            y = 1

        try:
            if 0 <= y < self.height:
                self.stdscr.addstr(y, self.cx(len(ts)), ts, self.theme.highlight)
            if 0 <= y + 1 < self.height:
                self.stdscr.addstr(y + 1, self.cx(len(ds)), ds, self.theme.accent)
        except curses.error:
            pass
        return y + 3

    # ═══════════════════════════════════════════════════
    # SYSTEM INFO (right side, elegant)
    # ═══════════════════════════════════════════════════

    def get_system_info(self):
        info = {}
        info["hostname"] = platform.node() or "unknown"
        info["kernel"] = platform.release() or "unknown"
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        info["os"] = line.split("=", 1)[1].strip().strip('"')
                        break
                else:
                    info["os"] = platform.system()
        except (FileNotFoundError, PermissionError):
            info["os"] = platform.system()
        try:
            with open("/proc/uptime") as f:
                up = float(f.readline().split()[0])
                info["uptime"] = f"{int(up // 3600)}h {int((up % 3600) // 60)}m"
        except (FileNotFoundError, PermissionError):
            info["uptime"] = "N/A"
        try:
            with open("/proc/meminfo") as f:
                mt = ma = 0
                for line in f:
                    if line.startswith("MemTotal:"):
                        mt = int(line.split()[1]) // 1024
                    elif line.startswith("MemAvailable:"):
                        ma = int(line.split()[1]) // 1024
                info["memory"] = f"{mt - ma}MB / {mt}MB"
        except (FileNotFoundError, PermissionError):
            info["memory"] = "N/A"
        return info

    def draw_sysinfo(self, y=None):
        self.update_size()
        if y is None:
            y = self.height - 8
        info = self.get_system_info()
        lines = [
            f"  ⌂ {info.get('hostname', 'unknown')}",
            f"  ◈ {info.get('os', 'Linux')}",
            f"  ⊕ Kernel: {info.get('kernel', 'unknown')}",
            f"  ↑ Uptime: {info.get('uptime', 'N/A')}",
            f"  ◉ {info.get('memory', 'N/A')}",
        ]
        for i, line in enumerate(lines):
            dy = y + i
            if 0 <= dy < self.height:
                try:
                    self.stdscr.addstr(dy, 2, line, self.theme.accent | curses.A_DIM)
                except curses.error:
                    pass

    # ═══════════════════════════════════════════════════
    # LOGIN BOX (double border, glowing, clean)
    # ═══════════════════════════════════════════════════

    def draw_login_box(self, y=None, username="", password="", session_name="",
                       active_field=0, message="", message_type="normal",
                       attempt_count=0, frame=0):
        self.update_size()
        bw = min(self.config.box_width, self.width - 4)
        bh = 14
        bx = self.cx(bw)
        by = y if y is not None else (self.height - bh) // 2
        box = self.theme.get_box_chars(self.config.box_style)

        # Glow border
        border_attr = self.theme.border
        if self.config.border_glow:
            glow = math.sin(frame * 0.06) * 0.5 + 0.5
            if glow > 0.7:
                border_attr = self.theme.highlight
            elif glow > 0.4:
                border_attr = self.theme.border | curses.A_BOLD

        self._draw_box(by, bx, bh, bw, box, border_attr)

        # Title
        title = f" ◈ {self.config.branding_text} ◈ "
        tx = bx + (bw - len(title)) // 2
        if 0 <= by < self.height:
            try:
                self.stdscr.addstr(by, tx, title, self.theme.highlight)
            except curses.error:
                pass

        ix = bx + 2
        iw = bw - 4
        cy = by + 2

        # Username
        label = "  ⊳ User:    "
        fw = iw - len(label)
        self._draw_field(cy, ix, label, username, fw, active=(active_field == 0))
        cy += 2

        # Password
        label = "  ⊳ Pass:    "
        self._draw_field(cy, ix, label, "●" * len(password), fw, active=(active_field == 1))
        cy += 2

        # Session
        label = "  ⊳ Session: "
        self._draw_field(cy, ix, label, f"◂ {session_name} ▸", fw, active=(active_field == 2))
        cy += 2

        # Divider
        if 0 <= cy < self.height:
            try:
                self.stdscr.addstr(cy, bx, box["lt"], border_attr)
                self.stdscr.addstr(cy, bx + 1, box["h"] * (bw - 2), border_attr)
                self.stdscr.addstr(cy, bx + bw - 1, box["rt"], border_attr)
            except curses.error:
                pass
        cy += 1

        # Message
        if message:
            ma = {"error": self.theme.error, "success": self.theme.highlight,
                  "warning": self.theme.warning}.get(message_type, self.theme.normal)
            msg = message[:iw]
            mx = bx + (bw - len(msg)) // 2
            if 0 <= cy < self.height:
                try:
                    self.stdscr.addstr(cy, mx, msg, ma)
                except curses.error:
                    pass

        # Help hints
        hy = by + bh - 2
        ht = "[Tab]Switch [Enter]Login [F1]Help [F2]Power [F3]Anim [F4]Theme"
        ht = ht[:iw]
        hx = bx + (bw - len(ht)) // 2
        if 0 <= hy < self.height:
            try:
                self.stdscr.addstr(hy, hx, ht, self.theme.accent | curses.A_DIM)
            except curses.error:
                pass

        # Attempt counter
        if attempt_count > 0:
            at = f"Attempts: {attempt_count}/{self.config.max_attempts}"
            ax = bx + bw - len(at) - 2
            aby = by + bh - 1
            if 0 <= aby < self.height:
                try:
                    self.stdscr.addstr(aby, ax, at, self.theme.warning | curses.A_DIM)
                except curses.error:
                    pass

        return (by, bx, by + bh, bx + bw)

    def _draw_box(self, y, x, h, w, box, border_attr=None):
        if border_attr is None:
            border_attr = self.theme.border
        # Top
        if 0 <= y < self.height:
            try:
                self.stdscr.addstr(y, x, box["tl"], border_attr)
                self.stdscr.addstr(y, x + 1, box["h"] * (w - 2), border_attr)
                self.stdscr.addstr(y, x + w - 1, box["tr"], border_attr)
            except curses.error:
                pass
        # Sides + fill
        for i in range(1, h - 1):
            dy = y + i
            if 0 <= dy < self.height:
                try:
                    self.stdscr.addstr(dy, x, box["v"], border_attr)
                    self.stdscr.addstr(dy, x + 1, " " * (w - 2), self.theme.normal)
                    self.stdscr.addstr(dy, x + w - 1, box["v"], border_attr)
                except curses.error:
                    pass
        # Bottom
        bot = y + h - 1
        if 0 <= bot < self.height:
            try:
                self.stdscr.addstr(bot, x, box["bl"], border_attr)
                self.stdscr.addstr(bot, x + 1, box["h"] * (w - 2), border_attr)
                self.stdscr.addstr(bot, x + w - 1, box["br"], border_attr)
            except curses.error:
                pass

    def _draw_field(self, y, x, label, value, fw, active=False):
        if not (0 <= y < self.height):
            return
        try:
            la = self.theme.highlight if active else self.theme.normal
            self.stdscr.addstr(y, x, label, la)
        except curses.error:
            pass
        fx = x + len(label)
        aw = max(1, fw - 1)
        try:
            if active:
                disp = value[:aw].ljust(aw)
                self.stdscr.addstr(y, fx, disp, self.theme.input_style | curses.A_UNDERLINE | curses.A_BOLD)
                cx = fx + min(len(value), aw)
                if cx < self.width:
                    self.stdscr.addstr(y, cx, "▌", self.theme.highlight)
            else:
                self.stdscr.addstr(y, fx, value[:aw].ljust(aw), self.theme.input_style)
        except curses.error:
            pass

    # ═══════════════════════════════════════════════════
    # POWER MENU
    # ═══════════════════════════════════════════════════

    def draw_power_menu(self, selected=0):
        self.update_size()
        opts = [
            ("⏻  Shutdown",  "systemctl poweroff"),
            ("↺  Reboot",    "systemctl reboot"),
            ("⏾  Suspend",   "systemctl suspend"),
            ("⏏  Hibernate", "systemctl hibernate"),
            ("✕  Cancel",    None),
        ]
        bw, bh = 30, len(opts) + 4
        bx = self.cx(bw)
        by = (self.height - bh) // 2
        box = self.theme.get_box_chars("double")
        self._draw_box(by, bx, bh, bw, box)
        title = " ⚡ Power Menu ⚡ "
        try:
            self.stdscr.addstr(by, bx + (bw - len(title)) // 2, title, self.theme.highlight)
        except curses.error:
            pass
        for i, (label, _) in enumerate(opts):
            oy = by + 2 + i
            if 0 <= oy < self.height:
                try:
                    if i == selected:
                        self.stdscr.addstr(oy, bx + 3, f" ▸ {label} ", self.theme.highlight | curses.A_REVERSE)
                    else:
                        self.stdscr.addstr(oy, bx + 3, f"   {label} ", self.theme.normal)
                except curses.error:
                    pass
        return opts

    # ═══════════════════════════════════════════════════
    # HELP SCREEN
    # ═══════════════════════════════════════════════════

    def draw_help_screen(self):
        self.update_size()
        lines = [
            "╔═══════════════ AM-LOGIN Help ═══════════════╗",
            "║                                             ║",
            "║  Tab / Shift+Tab   Navigate fields          ║",
            "║  Enter             Login                    ║",
            "║  ← / →             Change session           ║",
            "║  F1                Toggle help              ║",
            "║  F2                Power menu               ║",
            "║  F3                Cycle animation           ║",
            "║  F4                Cycle theme               ║",
            "║  F5                Toggle clock              ║",
            "║  Ctrl+C / Esc      Exit (demo mode)         ║",
            "║                                             ║",
            "║  Animations: matrix, starfield, fire,       ║",
            "║  wave, rain, dna, cyber, glitch, math, name ║",
            "║                                             ║",
            "║  By: Abdelouahab Mostafa                    ║",
            "║  « Mathematician · Hacker »                 ║",
            "║                                             ║",
            "║         Press any key to close              ║",
            "╚═════════════════════════════════════════════╝",
        ]
        sy = (self.height - len(lines)) // 2
        for i, line in enumerate(lines):
            x = self.cx(len(line))
            y = sy + i
            if 0 <= y < self.height:
                try:
                    self.stdscr.addstr(y, x, line, self.theme.accent)
                except curses.error:
                    pass

    # ═══════════════════════════════════════════════════
    # WELCOME ANIMATION (elegant intro)
    # ═══════════════════════════════════════════════════

    def fade_in_text(self, y, x, text, attr, delay=0.025):
        for i, ch in enumerate(text):
            if x + i < self.width and 0 <= y < self.height:
                try:
                    self.stdscr.addch(y, x + i, ch, attr)
                    self.stdscr.refresh()
                    time.sleep(delay)
                except curses.error:
                    pass

    def draw_welcome_animation(self):
        self.update_size()
        self.stdscr.clear()
        cx = self.width // 2
        cy = self.height // 2

        # Phase 1: Name reveal
        name = "Abdelouahab Mostafa"
        self.fade_in_text(cy - 3, cx - len(name) // 2, name, self.theme.logo, delay=0.04)
        time.sleep(0.2)

        # Phase 2: Title
        title = "─── Mathematician · Display Manager ───"
        self.fade_in_text(cy - 1, cx - len(title) // 2, title, self.theme.accent, delay=0.015)
        time.sleep(0.2)

        time.sleep(0.1)

        # Phase 4: Loading bar
        bw = 35
        bx = cx - bw // 2
        by = cy + 4
        try:
            self.stdscr.addstr(by - 1, cx - 6, "Initializing...", self.theme.normal)
        except curses.error:
            pass
        for i in range(bw + 1):
            p = i / bw
            filled = "█" * i + "░" * (bw - i)
            pct = f" {int(p * 100)}%"
            try:
                self.stdscr.addstr(by, bx, f"[{filled}]{pct}", self.theme.anim_primary)
                self.stdscr.refresh()
            except curses.error:
                pass
            time.sleep(0.015)
        time.sleep(0.3)

    # ═══════════════════════════════════════════════════
    # LOCKOUT SCREEN
    # ═══════════════════════════════════════════════════

    def draw_lockout_screen(self, remaining):
        self.update_size()
        lines = [
            "╔══════════════════════════════════════╗",
            "║         ⚠  ACCOUNT LOCKED  ⚠        ║",
            "║                                      ║",
            "║   Too many failed login attempts.     ║",
            f"║   Try again in: {remaining:>4}s               ║",
            "║                                      ║",
            "╚══════════════════════════════════════╝",
        ]
        sy = (self.height - len(lines)) // 2
        for i, line in enumerate(lines):
            x = self.cx(len(line))
            y = sy + i
            if 0 <= y < self.height:
                try:
                    self.stdscr.addstr(y, x, line, self.theme.error)
                except curses.error:
                    pass
