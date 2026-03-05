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
        # Wayland sessions (preferred)
        "plasma-wayland": ("startplasma-wayland", "wayland"),
        "sway":           ("sway", "wayland"),
        "hyprland":       ("Hyprland", "wayland"),
        "gnome-wayland":  ("gnome-session --session=gnome", "wayland"),
        # X11 sessions
        "plasma-x11":     ("startplasma-x11", "x11"),
        "i3":             ("i3", "x11"),
        "openbox":        ("openbox-session", "x11"),
        "bspwm":          ("bspwm", "x11"),
        "dwm":            ("dwm", "x11"),
        "awesome":        ("awesome", "x11"),
        "gnome":          ("gnome-session", "x11"),
        "xfce":           ("startxfce4", "x11"),
        "cinnamon":       ("cinnamon-session", "x11"),
        "mate":           ("mate-session", "x11"),
        "lxqt":           ("startlxqt", "x11"),
        "budgie":         ("budgie-desktop", "x11"),
    }

    # Environment variables needed for specific Wayland compositors
    WAYLAND_ENV = {
        "plasma-wayland": {
            "XDG_SESSION_TYPE": "wayland",
            "XDG_SESSION_DESKTOP": "KDE",
            "XDG_CURRENT_DESKTOP": "KDE",
            "QT_QPA_PLATFORM": "wayland",
            "QT_WAYLAND_DISABLE_WINDOWDECORATION": "1",
            "KWIN_COMPOSE": "Q",
        },
        "sway": {
            "XDG_SESSION_TYPE": "wayland",
            "XDG_SESSION_DESKTOP": "sway",
            "XDG_CURRENT_DESKTOP": "sway",
        },
        "hyprland": {
            "XDG_SESSION_TYPE": "wayland",
            "XDG_SESSION_DESKTOP": "Hyprland",
            "XDG_CURRENT_DESKTOP": "Hyprland",
        },
    }

    def __init__(self, preferred_type="wayland"):
        self.sessions = []
        self.current_index = 0
        self.preferred_type = preferred_type
        self._discover()
        self._select_preferred()

    def _discover(self):
        """Discover all sessions from .desktop files.

        Wayland sessions are scanned first and sorted to the top so that
        compositors like Plasma Wayland appear before their X11 counterparts.
        """
        self.sessions = []

        # Discover Wayland sessions first (preferred on modern systems)
        for d in self.WAYLAND_SESSION_DIRS:
            self._scan_dir(d, "wayland")

        # Discover X11 sessions
        for d in self.X_SESSION_DIRS:
            self._scan_dir(d, "x11")

        # Always add shell/TTY
        self.sessions.append(Session("Shell (TTY)", os.environ.get("SHELL", "/bin/bash"), "tty"))

        # If nothing found, add common fallbacks
        if len(self.sessions) <= 1:
            for name, (cmd, stype) in self.COMMON_FALLBACKS.items():
                # For fallback commands, check only the binary name (first word)
                binary = cmd.split()[0]
                if self._command_exists(binary):
                    self.sessions.insert(-1, Session(name.capitalize(), cmd, stype))

    def _select_preferred(self):
        """Auto-select the first session matching preferred_type (e.g. 'wayland')."""
        for i, s in enumerate(self.sessions):
            if s.session_type == self.preferred_type:
                self.current_index = i
                return

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
            result = subprocess.run(["which", cmd], capture_output=True, timeout=3)
            return result.returncode == 0
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
        """Launch Wayland session with proper environment."""
        try:
            vt = self._find_free_vt()

            # Build environment exports
            env_lines = []
            env_lines.append("export XDG_SESSION_TYPE=wayland")
            env_lines.append("export XDG_RUNTIME_DIR=/run/user/$(id -u)")

            # Ensure XDG_RUNTIME_DIR exists
            env_lines.append(
                'if [ ! -d "$XDG_RUNTIME_DIR" ]; then '
                'mkdir -p "$XDG_RUNTIME_DIR" && chmod 0700 "$XDG_RUNTIME_DIR"; fi'
            )

            # Detect session-specific env (Plasma Wayland, Sway, Hyprland, etc.)
            session_key = self._match_wayland_env_key(session)
            if session_key and session_key in self.WAYLAND_ENV:
                for var, val in self.WAYLAND_ENV[session_key].items():
                    env_lines.append(f"export {var}={val}")
            else:
                # Generic Wayland env fallback
                env_lines.append("export XDG_SESSION_DESKTOP=wayland")

            # DBus session (needed by KDE Plasma and GNOME)
            env_lines.append(
                'if command -v dbus-run-session >/dev/null 2>&1; then '
                f'exec dbus-run-session {session.exec_cmd}; '
                f'else exec {session.exec_cmd}; fi'
            )

            env_setup = "; ".join(env_lines)
            os.execvp("su", ["su", "-l", username, "-c", env_setup])
        except OSError as e:
            return False, str(e)

    def _match_wayland_env_key(self, session):
        """Match a session to a WAYLAND_ENV key."""
        name_lower = session.name.lower()
        exec_lower = session.exec_cmd.lower()

        if "plasma" in name_lower or "startplasma-wayland" in exec_lower:
            return "plasma-wayland"
        if "hyprland" in name_lower or "hyprland" in exec_lower:
            return "hyprland"
        if "sway" in name_lower or "sway" in exec_lower:
            return "sway"
        return None

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
