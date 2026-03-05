#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AM-LOGIN Theme Preview — Cycle through all themes
# By: Abdelouahab Mostafa
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export TERM="${TERM:-xterm-256color}"

THEMES=("cyber" "ocean" "forest" "sunset" "neon" "blood" "ice")
ANIMS=("matrix" "starfield" "fire" "wave" "rain" "dna" "cyber" "glitch" "math" "name")

echo "AM-Login Theme Preview"
echo "======================"
echo ""
echo "Themes: ${THEMES[*]}"
echo "Animations: ${ANIMS[*]}"
echo ""

THEME="${1:-cyber}"
ANIM="${2:-matrix}"

echo "Launching: theme=$THEME, animation=$ANIM"
echo "Press Esc to exit, F3 to cycle animations, F4 to cycle themes"
echo ""

exec python3 "$PROJECT_DIR/am_login.py" --demo --skip-intro --theme "$THEME" --anim "$ANIM"
