#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN Session Manager                        ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝

Discovers and launches X11, Wayland, and TTY sessions.
"""

import os
import subprocess
import configparser


class Session:
    """Represents a desktop session."""
    def __init__(self, name, exec_cmd, session_type="x11", desktop_names=None, comment=""):
        self.name = name
        self.exec_cmd = exec_cmd
        self.session_type = session_type  # "x11", "wayland", "tty"
        self.desktop_names = desktop_names or []
        self.comment = comment

    def __repr__(self):
        return f"Session({self.name}, {self.session_type})"


class SessionManager:
    """Discovers and manages display sessions."""

    X_SESSION_DIRS = [
        "/usr/share/xsessions",
        "/usr/local/share/xsessions",
    ]
    WAYLAND_SESSION_DIRS = [
        "/usr/share/wayland-sessions",
        "/usr/local/share/wayland-sessions",
    ]
    COMMON_FALLBACKS = {
        "i3":        ("i3", "x11"),
        "sway":      ("sway", "wayland"),
        "openbox":   ("openbox-session", "x11"),
        "bspwm":     ("bspwm", "x11"),
        "dwm":       ("dwm", "x11"),
        "awesome":   ("awesome", "x11"),
        "hyprland":  ("Hyprland", "wayland"),
        "plasma":    ("startplasma-x11", "x11"),
        "gnome":     ("gnome-session", "x11"),
        "xfce":      ("startxfce4", "x11"),
        "cinnamon":  ("cinnamon-session", "x11"),
        "mate":      ("mate-session", "x11"),
        "lxqt":      ("startlxqt", "x11"),
        "budgie":    ("budgie-desktop", "x11"),
    }

    def __init__(self):
        self.sessions = []
        self.current_index = 0
        self._discover()

    def _discover(self):
        """Discover all sessions from .desktop files."""
        self.sessions = []

        # Discover X11 sessions
        for d in self.X_SESSION_DIRS:
            self._scan_dir(d, "x11")

        # Discover Wayland sessions
        for d in self.WAYLAND_SESSION_DIRS:
            self._scan_dir(d, "wayland")

        # Always add shell/TTY
        self.sessions.append(Session("Shell (TTY)", os.environ.get("SHELL", "/bin/bash"), "tty"))

        # If nothing found, add common fallbacks
        if len(self.sessions) <= 1:
            for name, (cmd, stype) in self.COMMON_FALLBACKS.items():
                if self._command_exists(cmd):
                    self.sessions.insert(-1, Session(name.capitalize(), cmd, stype))

    def _scan_dir(self, directory, session_type):
        """Scan a directory for .desktop session files."""
        if not os.path.isdir(directory):
            return
        try:
            for fn in sorted(os.listdir(directory)):
                if not fn.endswith(".desktop"):
                    continue
                path = os.path.join(directory, fn)
                session = self._parse_desktop(path, session_type)
                if session:
                    # Avoid duplicates
                    if not any(s.name == session.name for s in self.sessions):
                        self.sessions.append(session)
        except PermissionError:
            pass

    def _parse_desktop(self, path, session_type):
        """Parse a .desktop file into a Session object."""
        cp = configparser.ConfigParser(interpolation=None)
        cp.read(path, encoding="utf-8")
        section = "Desktop Entry"
        if section not in cp:
            return None

        name = cp.get(section, "Name", fallback="")
        exec_cmd = cp.get(section, "Exec", fallback="")
        comment = cp.get(section, "Comment", fallback="")
        desktop_names = cp.get(section, "DesktopNames", fallback="").split(";")
        hidden = cp.getboolean(section, "Hidden", fallback=False)
        no_display = cp.getboolean(section, "NoDisplay", fallback=False)

        if not name or not exec_cmd or hidden or no_display:
            return None

        # Detect session type from TryExec or name
        if "wayland" in path.lower() or "wayland" in name.lower():
            session_type = "wayland"

        return Session(name, exec_cmd, session_type, desktop_names, comment)

    def _command_exists(self, cmd):
        """Check if command is available on the system."""
        try:
            subprocess.run(["which", cmd], capture_output=True, timeout=3)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @property
    def current(self):
        if self.sessions:
            return self.sessions[self.current_index]
        return Session("Shell", "/bin/bash", "tty")

    def next(self):
        if self.sessions:
            self.current_index = (self.current_index + 1) % len(self.sessions)
        return self.current

    def prev(self):
        if self.sessions:
            self.current_index = (self.current_index - 1) % len(self.sessions)
        return self.current

    def get_all(self):
        return list(self.sessions)

    def launch(self, session, username):
        """Launch a session for the specified user."""
        if session.session_type == "tty":
            return self._launch_tty(session, username)
        elif session.session_type == "wayland":
            return self._launch_wayland(session, username)
        else:
            return self._launch_x11(session, username)

    def _launch_tty(self, session, username):
        """Drop to shell."""
        try:
            os.execvp("su", ["su", "-l", username])
        except OSError as e:
            return False, str(e)

    def _launch_x11(self, session, username):
        """Launch X11 session via startx/xinit."""
        xinitrc = f"/tmp/.am-xinitrc-{username}"
        try:
            with open(xinitrc, "w") as f:
                f.write(f"#!/bin/sh\nexec {session.exec_cmd}\n")
            os.chmod(xinitrc, 0o755)

            # Find available VT
            vt = self._find_free_vt()
            os.execvp("su", [
                "su", "-l", username, "-c",
                f"startx {xinitrc} -- :{self._find_free_display()} vt{vt}"
            ])
        except OSError as e:
            return False, str(e)

    def _launch_wayland(self, session, username):
        """Launch Wayland session."""
        try:
            vt = self._find_free_vt()
            env_setup = (
                f"export XDG_SESSION_TYPE=wayland; "
                f"export XDG_RUNTIME_DIR=/run/user/$(id -u); "
                f"exec {session.exec_cmd}"
            )
            os.execvp("su", ["su", "-l", username, "-c", env_setup])
        except OSError as e:
            return False, str(e)

    def _find_free_vt(self):
        """Find a free virtual terminal."""
        try:
            result = subprocess.run(["fgconsole"], capture_output=True, text=True, timeout=3)
            current = int(result.stdout.strip())
            return current + 1
        except Exception:
            return 7

    def _find_free_display(self):
        """Find a free X display number."""
        for i in range(10):
            if not os.path.exists(f"/tmp/.X{i}-lock"):
                return i
        return 1
