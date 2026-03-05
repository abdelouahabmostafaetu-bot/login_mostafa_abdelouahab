#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN Theme Engine                            ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import curses


class Theme:
    THEMES = {
        "cyber": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_GREEN,
            "accent": curses.COLOR_CYAN, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_GREEN,
            "border": curses.COLOR_CYAN, "logo": curses.COLOR_GREEN,
            "anim_primary": curses.COLOR_GREEN, "anim_secondary": curses.COLOR_CYAN,
        },
        "ocean": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_CYAN,
            "accent": curses.COLOR_BLUE, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_CYAN,
            "border": curses.COLOR_BLUE, "logo": curses.COLOR_CYAN,
            "anim_primary": curses.COLOR_BLUE, "anim_secondary": curses.COLOR_CYAN,
        },
        "forest": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_GREEN,
            "accent": curses.COLOR_YELLOW, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_GREEN,
            "border": curses.COLOR_GREEN, "logo": curses.COLOR_YELLOW,
            "anim_primary": curses.COLOR_GREEN, "anim_secondary": curses.COLOR_YELLOW,
        },
        "sunset": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_YELLOW,
            "accent": curses.COLOR_RED, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_YELLOW,
            "border": curses.COLOR_RED, "logo": curses.COLOR_YELLOW,
            "anim_primary": curses.COLOR_RED, "anim_secondary": curses.COLOR_YELLOW,
        },
        "neon": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_MAGENTA,
            "accent": curses.COLOR_CYAN, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_MAGENTA,
            "border": curses.COLOR_CYAN, "logo": curses.COLOR_MAGENTA,
            "anim_primary": curses.COLOR_MAGENTA, "anim_secondary": curses.COLOR_CYAN,
        },
        "blood": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_RED,
            "accent": curses.COLOR_YELLOW, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_RED,
            "border": curses.COLOR_RED, "logo": curses.COLOR_RED,
            "anim_primary": curses.COLOR_RED, "anim_secondary": curses.COLOR_YELLOW,
        },
        "ice": {
            "bg": curses.COLOR_BLACK, "fg": curses.COLOR_WHITE,
            "accent": curses.COLOR_CYAN, "highlight": curses.COLOR_WHITE,
            "error": curses.COLOR_RED, "warning": curses.COLOR_YELLOW,
            "input_bg": curses.COLOR_BLACK, "input_fg": curses.COLOR_WHITE,
            "border": curses.COLOR_CYAN, "logo": curses.COLOR_WHITE,
            "anim_primary": curses.COLOR_WHITE, "anim_secondary": curses.COLOR_CYAN,
        },
    }

    BOX_STYLES = {
        "single": {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│", "lt": "├", "rt": "┤"},
        "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║", "lt": "╠", "rt": "╣"},
        "rounded": {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│", "lt": "├", "rt": "┤"},
        "heavy": {"tl": "┏", "tr": "┓", "bl": "┗", "br": "┛", "h": "━", "v": "┃", "lt": "┣", "rt": "┫"},
        "ascii": {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|", "lt": "+", "rt": "+"},
    }

    PAIR_NORMAL = 1
    PAIR_ACCENT = 2
    PAIR_HIGHLIGHT = 3
    PAIR_ERROR = 4
    PAIR_WARNING = 5
    PAIR_INPUT = 6
    PAIR_BORDER = 7
    PAIR_LOGO = 8
    PAIR_ANIM_PRIMARY = 9
    PAIR_ANIM_SECONDARY = 10
    PAIR_DIM = 11
    PAIR_BRIGHT = 12

    def __init__(self, theme_name="cyber"):
        self.theme_name = theme_name if theme_name in self.THEMES else "cyber"
        self.colors = self.THEMES[self.theme_name]

    def init_colors(self):
        if not curses.has_colors():
            return
        curses.start_color()
        curses.use_default_colors()
        c = self.colors
        curses.init_pair(self.PAIR_NORMAL, c["fg"], c["bg"])
        curses.init_pair(self.PAIR_ACCENT, c["accent"], c["bg"])
        curses.init_pair(self.PAIR_HIGHLIGHT, c["highlight"], c["bg"])
        curses.init_pair(self.PAIR_ERROR, c["error"], c["bg"])
        curses.init_pair(self.PAIR_WARNING, c["warning"], c["bg"])
        curses.init_pair(self.PAIR_INPUT, c["input_fg"], c["input_bg"])
        curses.init_pair(self.PAIR_BORDER, c["border"], c["bg"])
        curses.init_pair(self.PAIR_LOGO, c["logo"], c["bg"])
        curses.init_pair(self.PAIR_ANIM_PRIMARY, c["anim_primary"], c["bg"])
        curses.init_pair(self.PAIR_ANIM_SECONDARY, c["anim_secondary"], c["bg"])
        curses.init_pair(self.PAIR_DIM, curses.COLOR_BLACK, c["bg"])
        curses.init_pair(self.PAIR_BRIGHT, curses.COLOR_WHITE, c["bg"])

    def get_box_chars(self, style="double"):
        return self.BOX_STYLES.get(style, self.BOX_STYLES["double"])

    @property
    def normal(self):
        return curses.color_pair(self.PAIR_NORMAL)

    @property
    def accent(self):
        return curses.color_pair(self.PAIR_ACCENT)

    @property
    def highlight(self):
        return curses.color_pair(self.PAIR_HIGHLIGHT) | curses.A_BOLD

    @property
    def error(self):
        return curses.color_pair(self.PAIR_ERROR) | curses.A_BOLD

    @property
    def warning(self):
        return curses.color_pair(self.PAIR_WARNING)

    @property
    def input_style(self):
        return curses.color_pair(self.PAIR_INPUT)

    @property
    def border(self):
        return curses.color_pair(self.PAIR_BORDER)

    @property
    def logo(self):
        return curses.color_pair(self.PAIR_LOGO) | curses.A_BOLD

    @property
    def anim_primary(self):
        return curses.color_pair(self.PAIR_ANIM_PRIMARY)

    @property
    def anim_secondary(self):
        return curses.color_pair(self.PAIR_ANIM_SECONDARY)

    @property
    def dim(self):
        return curses.color_pair(self.PAIR_DIM) | curses.A_DIM

    @property
    def bright(self):
        return curses.color_pair(self.PAIR_BRIGHT) | curses.A_BOLD
