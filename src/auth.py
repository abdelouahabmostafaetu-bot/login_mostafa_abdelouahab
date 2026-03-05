#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN Authentication Module                   ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝

Handles PAM, shadow, and su-based authentication.
Compatible with Python 3.13+ (no crypt/spwd).
"""

import os
import subprocess
import hashlib

# Optional PAM support
try:
    import pam as pam_module
    HAS_PAM = True
except ImportError:
    HAS_PAM = False

# Optional crypt support (removed in Python 3.13+)
try:
    import crypt
    HAS_CRYPT = True
except ImportError:
    HAS_CRYPT = False

# Optional spwd support (removed in Python 3.13+)
try:
    import spwd
    HAS_SPWD = True
except ImportError:
    HAS_SPWD = False


class AuthResult:
    """Authentication attempt result."""
    def __init__(self, success, message="", username=""):
        self.success = success
        self.message = message
        self.username = username

    def __bool__(self):
        return self.success


class PAMAuthenticator:
    """PAM-based authentication (preferred method)."""
    def __init__(self):
        if not HAS_PAM:
            raise RuntimeError("python-pam not available")
        self.pam = pam_module.pam()

    def authenticate(self, username, password):
        try:
            if self.pam.authenticate(username, password, service="login"):
                return AuthResult(True, "Login successful", username)
            else:
                return AuthResult(False, self.pam.reason or "Authentication failed")
        except Exception as e:
            return AuthResult(False, f"PAM error: {e}")


class ShadowAuthenticator:
    """Shadow password authentication (/etc/shadow)."""
    def __init__(self):
        if not HAS_CRYPT or not HAS_SPWD:
            raise RuntimeError("crypt/spwd modules not available (Python 3.13+)")

    def authenticate(self, username, password):
        try:
            sp = spwd.getspnam(username)
            if sp.sp_pwdp in ("!", "*", "!!", ""):
                return AuthResult(False, "Account locked or no password")
            enc = crypt.crypt(password, sp.sp_pwdp)
            if enc == sp.sp_pwdp:
                return AuthResult(True, "Login successful", username)
            return AuthResult(False, "Invalid password")
        except KeyError:
            return AuthResult(False, "User not found")
        except PermissionError:
            return AuthResult(False, "Permission denied (shadow)")
        except Exception as e:
            return AuthResult(False, f"Shadow auth error: {e}")


class SUAuthenticator:
    """su command-based authentication (fallback for Python 3.13+)."""
    def authenticate(self, username, password):
        try:
            proc = subprocess.Popen(
                ["su", "-c", "echo __AUTH_OK__", username],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, "LANG": "C"},
            )
            stdout, _ = proc.communicate(input=(password + "\n").encode(), timeout=10)
            if b"__AUTH_OK__" in stdout:
                return AuthResult(True, "Login successful", username)
            return AuthResult(False, "Invalid username or password")
        except subprocess.TimeoutExpired:
            proc.kill()
            return AuthResult(False, "Authentication timed out")
        except FileNotFoundError:
            return AuthResult(False, "su command not found")
        except Exception as e:
            return AuthResult(False, f"Auth error: {e}")


class DemoAuthenticator:
    """Demo-mode authenticator (no real auth)."""
    DEMO_USERS = {
        "abdelouahab": "math2024",
        "admin": "admin",
        "demo": "demo",
        "root": "toor",
        "euler": "e2718",
        "gauss": "pi314",
    }

    def authenticate(self, username, password):
        if username in self.DEMO_USERS:
            if self.DEMO_USERS[username] == password:
                return AuthResult(True, f"Welcome, {username} (demo mode)", username)
            return AuthResult(False, "Invalid password (demo)")
        return AuthResult(False, f"User '{username}' not found (demo)")


def get_authenticator(demo_mode=False):
    """Return the best available authenticator."""
    if demo_mode:
        return DemoAuthenticator()

    # Priority: PAM > Shadow > SU
    if HAS_PAM:
        try:
            return PAMAuthenticator()
        except RuntimeError:
            pass
    if HAS_CRYPT and HAS_SPWD:
        try:
            return ShadowAuthenticator()
        except RuntimeError:
            pass

    # Fallback to su-based auth
    return SUAuthenticator()
