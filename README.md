# AM-Login — TUI Display Manager

```
   █████╗ ███╗   ███╗      ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
  ██╔══██╗████╗ ████║      ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
  ███████║██╔████╔██║█████╗██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
  ██╔══██║██║╚██╔╝██║╚════╝██║     ██║   ██║██║   ██║██║██║╚██╗██║
  ██║  ██║██║ ╚═╝ ██║      ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
  ╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝
```

**A beautiful TUI login/display manager inspired by [ly](https://github.com/fairyglade/ly).**
**By: Abdelouahab Mostafa — Mathematician · Hacker**

---

## Features

- **10 Background Animations**: Matrix rain, math rain (∫∑π formulas), starfield, fire, sine
  wave, rain with lightning, DNA helix, cyber grid, glitch effect, name particles
- **7 Color Themes**: Cyber, Ocean, Forest, Sunset, Neon, Blood, Ice
- **5 Box Styles**: Single, Double, Rounded, Heavy, ASCII
- **Mathematician Identity Card**: Personalized portrait & math branding
- **Elegant Hacker Aesthetic**: Glowing borders, animated branding, Unicode art
- **Session Discovery**: Auto-detects X11/Wayland/TTY desktop sessions
- **Authentication**: PAM, shadow passwords, or su-based (Python 3.13+ compatible)
- **Welcome Animation**: Cinematic intro with loading bar
- **Power Menu**: Shutdown, reboot, suspend, hibernate
- **Lockout Protection**: Configurable max attempts & lockout timer
- **systemd Integration**: Production-ready display manager service
- **Fully Configurable**: INI config file for all settings

---

## Quick Start

### Demo Mode (no root required)

```bash
python3 am_login.py --demo
```

### Demo with options

```bash
# Skip intro animation
python3 am_login.py --demo --skip-intro

# Choose theme and animation
python3 am_login.py --demo --theme neon --anim matrix

# All animations: matrix, starfield, fire, wave, rain, dna, cyber, glitch, math, name
# All themes: cyber, ocean, forest, sunset, neon, blood, ice
```

### Demo Login Credentials

| User         | Password |
|--------------|----------|
| abdelouahab  | math2024 |
| admin        | admin    |
| demo         | demo     |
| root         | toor     |
| euler        | e2718    |
| gauss        | pi314    |

---

## Keyboard Shortcuts

| Key              | Action               |
|------------------|----------------------|
| `Tab`            | Next field           |
| `Shift+Tab`      | Previous field       |
| `Enter`          | Login / Confirm      |
| `←` / `→`        | Change session       |
| `F1`             | Help screen          |
| `F2`             | Power menu           |
| `F3`             | Cycle animation      |
| `F4`             | Cycle theme          |
| `F5`             | Toggle clock         |
| `Esc` / `Ctrl+C` | Quit (demo mode)     |

---

## Installation (as Display Manager)

```bash
# Install system-wide
sudo bash install.sh install

# Enable as your display manager
sudo systemctl enable --now am-login

# To uninstall
sudo bash install.sh uninstall
```

---

## Configuration

Edit `config/default.conf`:

```ini
[general]
branding_text = AM-Login
author = Abdelouahab Mostafa

[theme]
name = cyber           # cyber, ocean, forest, sunset, neon, blood, ice

[animation]
type = matrix          # matrix, starfield, fire, wave, rain, dna, cyber, glitch, math, name, none

[ui]
show_clock = true
clock_format = 24h
show_hostname = true
show_sysinfo = true
show_portrait = true   # Show mathematician identity card
box_style = double     # single, double, rounded, heavy, ascii
box_width = 60
border_glow = true

[auth]
max_attempts = 5
lockout_duration = 30
```

---

## Project Structure

```
login_them/
├── am_login.py          # Main application
├── install.sh           # System installer
├── config/
│   └── default.conf     # Default configuration
├── src/
│   ├── __init__.py
│   ├── config.py        # Config management
│   ├── themes.py        # 7 color themes + box styles
│   ├── animations.py    # 10 background animations
│   ├── ui.py            # UI components + identity card
│   ├── auth.py          # PAM / shadow / su authentication
│   └── sessions.py      # Session discovery & launcher
└── README.md
```

---

## Requirements

- Python 3.8+ (tested on 3.14)
- `ncurses` (included in Python standard library)
- **Optional**: `python-pam` for PAM authentication
- **Optional**: UTF-8 terminal with Unicode support

---

## Notes

- Python 3.13+ removed `crypt` and `spwd` modules — AM-Login automatically
  falls back to `su`-based authentication
- For best visuals, use a terminal with full Unicode and 256-color support
- In production (as DM), the service runs on TTY1

---

**Abdelouahab Mostafa** — *Mathematician · Hacker*
*« Mathematics is the queen of the sciences » — C.F. Gauss*
