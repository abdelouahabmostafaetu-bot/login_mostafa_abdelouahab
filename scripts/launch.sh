#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AM-LOGIN Quick Launcher
# By: Abdelouahab Mostafa
# ═══════════════════════════════════════════════════════════════
#
# Usage:
#   ./scripts/launch.sh              # Run in demo mode
#   ./scripts/launch.sh --theme neon # Choose a theme
#   sudo ./scripts/launch.sh --real  # Run with real auth
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Ensure TERM is set (fixes curses issues on some terminals)
export TERM="${TERM:-xterm-256color}"

# Ensure UTF-8 locale
export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

ARGS=("$@")

# Default to demo mode if not running as root and --real not specified
if [[ $EUID -ne 0 ]] && [[ ! " ${ARGS[*]} " =~ " --real " ]]; then
    # Add --demo if not already present
    if [[ ! " ${ARGS[*]} " =~ " --demo " ]]; then
        ARGS=("--demo" "${ARGS[@]}")
    fi
fi

# Remove --real flag (it's our custom flag, not passed to Python)
ARGS=("${ARGS[@]/--real/}")

exec python3 "$PROJECT_DIR/am_login.py" "${ARGS[@]}"
