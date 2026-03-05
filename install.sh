#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AM-LOGIN Installer — TUI Display Manager
# By: Abdelouahab Mostafa
# ═══════════════════════════════════════════════════════════════

set -e

APP_NAME="am-login"
INSTALL_DIR="/opt/am-login"
SERVICE_FILE="/etc/systemd/system/am-login.service"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

msg()  { echo -e "${CYAN}[AM-Login]${NC} $1"; }
ok()   { echo -e "${GREEN}[  OK  ]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1" >&2; }

banner() {
    echo -e "${CYAN}"
    echo "   █████╗ ███╗   ███╗      ██╗      ██████╗  ██████╗ ██╗███╗   ██╗"
    echo "  ██╔══██╗████╗ ████║      ██║     ██╔═══██╗██╔════╝ ██║████╗  ██║"
    echo "  ███████║██╔████╔██║█████╗██║     ██║   ██║██║  ███╗██║██╔██╗ ██║"
    echo "  ██╔══██║██║╚██╔╝██║╚════╝██║     ██║   ██║██║   ██║██║██║╚██╗██║"
    echo "  ██║  ██║██║ ╚═╝ ██║      ███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║"
    echo "  ╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝"
    echo -e "${NC}"
    echo -e "  ${BOLD}Installer — By Abdelouahab Mostafa${NC}"
    echo ""
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        err "This script must be run as root (sudo)."
        exit 1
    fi
}

install_deps() {
    msg "Checking dependencies..."
    if command -v pacman &>/dev/null; then
        pacman -S --needed --noconfirm python python-pam \
            plasma-wayland-session qt6-wayland 2>/dev/null || true
    elif command -v apt-get &>/dev/null; then
        apt-get install -y python3 python3-pam \
            kde-plasma-desktop plasma-workspace-wayland 2>/dev/null || true
    elif command -v dnf &>/dev/null; then
        dnf install -y python3 python3-pam \
            plasma-workspace-wayland qt6-qtwayland 2>/dev/null || true
    fi
    ok "Dependencies checked"
}

install_files() {
    msg "Installing to ${INSTALL_DIR}..."
    mkdir -p "${INSTALL_DIR}"/{src,config,assets,themes,scripts}

    cp -r src/*.py "${INSTALL_DIR}/src/"
    cp am_login.py "${INSTALL_DIR}/"
    cp config/default.conf "${INSTALL_DIR}/config/"
    cp scripts/*.sh "${INSTALL_DIR}/scripts/" 2>/dev/null || true

    chmod +x "${INSTALL_DIR}/am_login.py"
    chmod +x "${INSTALL_DIR}/scripts/"*.sh 2>/dev/null || true

    # Create launcher
    cat > /usr/local/bin/am-login << 'LAUNCHER'
#!/bin/bash
exec python3 /opt/am-login/am_login.py "$@"
LAUNCHER
    chmod +x /usr/local/bin/am-login

    ok "Files installed to ${INSTALL_DIR}"
}

install_service() {
    msg "Installing systemd service..."
    cat > "${SERVICE_FILE}" << 'SERVICE'
[Unit]
Description=AM-Login Display Manager
Documentation=https://github.com/am-login
Conflicts=getty@tty1.service
After=systemd-user-sessions.service
After=plymouth-quit-wait.service
After=systemd-logind.service

[Service]
Type=idle
ExecStart=/usr/local/bin/am-login
StandardInput=tty
StandardOutput=tty
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes
TTYVTDisallocate=yes
Environment=XDG_SESSION_TYPE=wayland
Environment=QT_QPA_PLATFORM=wayland
Restart=always
RestartSec=1

[Install]
WantedBy=graphical.target
Alias=display-manager.service
SERVICE

    systemctl daemon-reload
    ok "Systemd service installed"
    msg "Enable with: systemctl enable am-login"
}

uninstall() {
    msg "Uninstalling AM-Login..."
    systemctl stop am-login 2>/dev/null || true
    systemctl disable am-login 2>/dev/null || true
    rm -rf "${INSTALL_DIR}"
    rm -f /usr/local/bin/am-login
    rm -f "${SERVICE_FILE}"
    systemctl daemon-reload
    ok "AM-Login uninstalled"
}

case "${1:-install}" in
    install)
        banner
        check_root
        install_deps
        install_files
        install_service
        echo ""
        ok "Installation complete!"
        msg "Test:   am-login --demo"
        msg "Enable: sudo systemctl enable --now am-login"
        ;;
    uninstall)
        check_root
        uninstall
        ;;
    *)
        echo "Usage: $0 {install|uninstall}"
        exit 1
        ;;
esac
