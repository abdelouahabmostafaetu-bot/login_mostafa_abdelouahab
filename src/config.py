#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN Configuration Module                    ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import configparser
import os

DEFAULT_CONFIG_PATH = "/etc/am-login/default.conf"
USER_CONFIG_PATH = os.path.expanduser("~/.config/am-login/config.conf")
LOCAL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "default.conf")


class Config:
    DEFAULTS = {
        "General": {
            "animation": "matrix",
            "animation_speed": "6",
            "theme": "cyber",
            "show_clock": "true",
            "clock_format": "24h",
            "show_sysinfo": "true",
            "show_branding": "true",
            "branding_text": "Abdelouahab Mostafa",
            "box_style": "double",
            "box_width": "52",
            "auto_login_user": "",
            "auto_login_delay": "5",
            "max_attempts": "5",
            "lockout_duration": "300",
            "screensaver_timeout": "60",
            "screensaver_animation": "starfield",
        },
        "Sessions": {
            "default_session": "0",
        },
        "Appearance": {
            "bg_char": " ",
            "fade_in": "true",
            "fade_speed": "3",
            "show_logo": "true",
            "show_portrait": "true",
            "border_glow": "true",
            "typing_animation": "true",
        },
    }

    def __init__(self, config_path=None):
        self.parser = configparser.ConfigParser()
        for section, values in self.DEFAULTS.items():
            self.parser[section] = values
        paths = [LOCAL_CONFIG_PATH, DEFAULT_CONFIG_PATH, USER_CONFIG_PATH]
        if config_path:
            paths.append(config_path)
        for path in paths:
            if os.path.exists(path):
                self.parser.read(path)

    def get(self, section, key, fallback=None):
        return self.parser.get(section, key, fallback=fallback)

    def getint(self, section, key, fallback=0):
        return self.parser.getint(section, key, fallback=fallback)

    def getbool(self, section, key, fallback=False):
        return self.parser.getboolean(section, key, fallback=fallback)

    @property
    def animation(self):
        return self.get("General", "animation", "matrix")

    @property
    def animation_speed(self):
        return self.getint("General", "animation_speed", 6)

    @property
    def theme(self):
        return self.get("General", "theme", "cyber")

    @property
    def show_clock(self):
        return self.getbool("General", "show_clock", True)

    @property
    def clock_format(self):
        return self.get("General", "clock_format", "24h")

    @property
    def show_sysinfo(self):
        return self.getbool("General", "show_sysinfo", True)

    @property
    def show_branding(self):
        return self.getbool("General", "show_branding", True)

    @property
    def branding_text(self):
        return self.get("General", "branding_text", "Abdelouahab Mostafa")

    @property
    def box_style(self):
        return self.get("General", "box_style", "double")

    @property
    def box_width(self):
        return self.getint("General", "box_width", 52)

    @property
    def show_logo(self):
        return self.getbool("Appearance", "show_logo", True)

    @property
    def show_portrait(self):
        return self.getbool("Appearance", "show_portrait", True)

    @property
    def fade_in(self):
        return self.getbool("Appearance", "fade_in", True)

    @property
    def fade_speed(self):
        return self.getint("Appearance", "fade_speed", 3)

    @property
    def border_glow(self):
        return self.getbool("Appearance", "border_glow", True)

    @property
    def typing_animation(self):
        return self.getbool("Appearance", "typing_animation", True)

    @property
    def max_attempts(self):
        return self.getint("General", "max_attempts", 5)

    @property
    def lockout_duration(self):
        return self.getint("General", "lockout_duration", 300)

    @property
    def screensaver_timeout(self):
        return self.getint("General", "screensaver_timeout", 60)

    @property
    def screensaver_animation(self):
        return self.get("General", "screensaver_animation", "starfield")
