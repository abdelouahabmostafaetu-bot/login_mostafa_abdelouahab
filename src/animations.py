#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║              AM-LOGIN Animation Engine                        ║
║              By: Abdelouahab Mostafa                         ║
╚══════════════════════════════════════════════════════════════╝

Elite animations: Matrix, Starfield, Fire, Wave, Rain (with lightning),
DNA Helix, Cyber Grid, Glitch, Math Rain, Name Particles.
Fast · Elegant · Hacker aesthetic.
"""

import curses
import random
import math


class AnimationEngine:
    """High-performance background animation engine."""

    MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789@#$%&*アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ"
    MATH_CHARS = "∫∑∏∂∇∆Ωπεδ∞≈≠≡±÷×√∈∉⊂⊃∪∩∧∨⊕⊗λμσφψωαβγθ"
    RAIN_CHARS = "│┃╎╏║∣∥|"
    DNA_CHARS = "ATCG·─═~"
    FIRE_CHARS = " .:-=+*#%@█▓▒░"
    CYBER_CHARS = "01"
    GLITCH_CHARS = "!@#$%^&*█▓▒░╬╫╪┼│─"

    def __init__(self, stdscr, theme, speed=6, safe_zone=None):
        self.stdscr = stdscr
        self.theme = theme
        self.speed = max(1, min(10, speed))
        self.safe_zone = safe_zone
        self.height, self.width = stdscr.getmaxyx()
        self.frame = 0
        self.state = {}

    def set_safe_zone(self, y1, x1, y2, x2):
        self.safe_zone = (y1, x1, y2, x2)

    def _in_safe_zone(self, y, x):
        if not self.safe_zone:
            return False
        y1, x1, y2, x2 = self.safe_zone
        return y1 - 1 <= y <= y2 + 1 and x1 - 1 <= x <= x2 + 1

    def _put(self, y, x, ch, attr=0):
        """Safe put character, respecting safe zone and bounds."""
        if self._in_safe_zone(y, x):
            return
        try:
            if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
                self.stdscr.addch(y, x, ch, attr)
        except curses.error:
            pass

    def _puts(self, y, x, s, attr=0):
        """Safe put string."""
        if 0 <= y < self.height - 1:
            for i, ch in enumerate(s):
                nx = x + i
                if 0 <= nx < self.width - 1 and not self._in_safe_zone(y, nx):
                    try:
                        self.stdscr.addch(y, nx, ch, attr)
                    except curses.error:
                        pass

    def update_size(self):
        self.height, self.width = self.stdscr.getmaxyx()

    # ═══════════════════════════════════════════════════
    # 1. MATRIX RAIN — fast, dense, flickering
    # ═══════════════════════════════════════════════════

    def _init_matrix(self):
        drops = []
        for _ in range(self.width):
            drops.append(self._new_matrix_drop())
        self.state["mx"] = drops

    def _new_matrix_drop(self):
        return {
            "x": random.randint(0, max(0, self.width - 1)),
            "y": random.uniform(-self.height * 1.5, 0),
            "sp": random.uniform(0.6, 2.2) * (self.speed / 5),
            "ln": random.randint(4, 28),
            "ch": [random.choice(self.MATRIX_CHARS) for _ in range(30)],
        }

    def draw_matrix(self):
        if "mx" not in self.state:
            self._init_matrix()
        for d in self.state["mx"]:
            y, x = int(d["y"]), d["x"]
            for i in range(d["ln"]):
                dy = y - i
                if 0 <= dy < self.height and 0 <= x < self.width:
                    c = d["ch"][i % len(d["ch"])]
                    if i == 0:
                        self._put(dy, x, ord(c), self.theme.highlight)
                    elif i < 2:
                        self._put(dy, x, ord(c), self.theme.anim_primary | curses.A_BOLD)
                    elif i < d["ln"] // 3:
                        self._put(dy, x, ord(c), self.theme.anim_primary)
                    else:
                        self._put(dy, x, ord(c), self.theme.anim_secondary | curses.A_DIM)
            d["y"] += d["sp"]
            if random.random() < 0.25:
                d["ch"][random.randint(0, len(d["ch"]) - 1)] = random.choice(self.MATRIX_CHARS)
            if y - d["ln"] > self.height:
                d.update(self._new_matrix_drop())
                d["y"] = random.uniform(-12, -1)

    # ═══════════════════════════════════════════════════
    # 2. MATH RAIN — for the mathematician ∫∑π∞
    # ═══════════════════════════════════════════════════

    def _init_math(self):
        formulas = [
            "SYS:OK", "AUTH", "CRYPT", "HASH", "KERN", "PROC",
            "INIT", "SOCK", "PORT", "PIPE", "FORK", "EXEC",
            "ROOT", "NODE", "SYNC", "LOCK", "0xFF", "NULL",
            "SCAN", "PING", "0x00", "LOAD", "LINK",
        ]
        drops = []
        for _ in range(self.width // 2):
            drops.append({
                "x": random.randint(0, max(0, self.width - 1)),
                "y": random.uniform(-self.height, 0),
                "sp": random.uniform(0.3, 1.5) * (self.speed / 5),
                "txt": random.choice(formulas),
                "single": random.random() < 0.6,
                "ch": random.choice(self.MATH_CHARS),
                "br": random.uniform(0.2, 1.0),
            })
        self.state["math"] = drops

    def draw_math_rain(self):
        if "math" not in self.state:
            self._init_math()
        for d in self.state["math"]:
            y, x = int(d["y"]), d["x"]
            if d["single"]:
                if 0 <= y < self.height and 0 <= x < self.width:
                    if d["br"] > 0.7:
                        a = self.theme.highlight
                    elif d["br"] > 0.4:
                        a = self.theme.anim_primary | curses.A_BOLD
                    else:
                        a = self.theme.anim_secondary | curses.A_DIM
                    self._put(y, x, ord(d["ch"]), a)
                    for t in range(1, 4):
                        if 0 <= y - t < self.height:
                            self._put(y - t, x, ord(d["ch"]), self.theme.anim_secondary | curses.A_DIM)
            else:
                for i, ch in enumerate(d["txt"]):
                    cx = x + i
                    if 0 <= y < self.height and 0 <= cx < self.width:
                        a = self.theme.anim_primary | curses.A_BOLD if i == 0 else self.theme.anim_secondary
                        self._put(y, cx, ord(ch), a)
            d["y"] += d["sp"]
            if random.random() < 0.05:
                d["ch"] = random.choice(self.MATH_CHARS)
            if y > self.height + 5:
                d["y"] = random.uniform(-10, -1)
                d["x"] = random.randint(0, max(0, self.width - 1))
                d["br"] = random.uniform(0.2, 1.0)

    # ═══════════════════════════════════════════════════
    # 3. STARFIELD — warp speed with streaks
    # ═══════════════════════════════════════════════════

    def _init_stars(self):
        stars = []
        for _ in range((self.width * self.height) // 10):
            stars.append({
                "x": random.uniform(-1, 1), "y": random.uniform(-1, 1),
                "z": random.uniform(0.01, 1),
                "sp": random.uniform(0.004, 0.018) * (self.speed / 5),
            })
        self.state["stars"] = stars

    def draw_starfield(self):
        if "stars" not in self.state:
            self._init_stars()
        cx, cy = self.width // 2, self.height // 2
        for s in self.state["stars"]:
            f = 1.0 / max(s["z"], 0.01)
            sx = int(cx + s["x"] * f * cx * 0.5)
            sy = int(cy + s["y"] * f * cy * 0.5)
            if 0 <= sx < self.width and 0 <= sy < self.height:
                if s["z"] < 0.1:
                    self._put(sy, sx, ord("█"), self.theme.highlight)
                    for streak in range(1, 3):
                        pf = 1.0 / max(s["z"] + streak * 0.06, 0.01)
                        px = int(cx + s["x"] * pf * cx * 0.5)
                        py = int(cy + s["y"] * pf * cy * 0.5)
                        if 0 <= px < self.width and 0 <= py < self.height:
                            self._put(py, px, ord("─"), self.theme.anim_secondary | curses.A_DIM)
                elif s["z"] < 0.25:
                    self._put(sy, sx, ord("★"), self.theme.anim_primary | curses.A_BOLD)
                elif s["z"] < 0.5:
                    self._put(sy, sx, ord("*"), self.theme.anim_primary)
                elif s["z"] < 0.75:
                    self._put(sy, sx, ord("·"), self.theme.anim_secondary)
                else:
                    self._put(sy, sx, ord("."), self.theme.anim_secondary | curses.A_DIM)
            s["z"] -= s["sp"]
            if s["z"] <= 0.005:
                s["x"] = random.uniform(-1, 1)
                s["y"] = random.uniform(-1, 1)
                s["z"] = 1.0

    # ═══════════════════════════════════════════════════
    # 4. FIRE — realistic heat propagation
    # ═══════════════════════════════════════════════════

    def _init_fire(self):
        self.state["fg"] = [[0.0] * self.width for _ in range(self.height)]

    def draw_fire(self):
        if "fg" not in self.state:
            self._init_fire()
        g = self.state["fg"]
        while len(g) < self.height:
            g.append([0.0] * self.width)
        for r in g:
            while len(r) < self.width:
                r.append(0.0)
        for x in range(self.width):
            if random.random() < 0.7:
                g[self.height - 1][x] = random.uniform(0.6, 1.0)
            if random.random() < 0.3 and self.height > 1:
                g[self.height - 2][x] = random.uniform(0.3, 0.8)
        for y in range(0, max(0, self.height - 2)):
            for x in range(self.width):
                decay = random.uniform(0.015, 0.06)
                sx = max(0, min(self.width - 1, x + random.randint(-1, 1)))
                g[y][x] = max(0, (g[y + 1][sx] + g[y + 1][x] + g[y + 2][sx]) / 3.0 - decay)
        for y in range(self.height):
            for x in range(self.width):
                h = g[y][x]
                if h <= 0.01:
                    continue
                ci = max(0, min(len(self.FIRE_CHARS) - 1, int(h * (len(self.FIRE_CHARS) - 1))))
                if h > 0.85:
                    a = self.theme.highlight
                elif h > 0.6:
                    a = self.theme.anim_primary | curses.A_BOLD
                elif h > 0.35:
                    a = self.theme.anim_primary
                else:
                    a = self.theme.anim_secondary | curses.A_DIM
                self._put(y, x, ord(self.FIRE_CHARS[ci]), a)

    # ═══════════════════════════════════════════════════
    # 5. WAVE — smooth interference patterns
    # ═══════════════════════════════════════════════════

    def draw_wave(self):
        t = self.frame * 0.08 * (self.speed / 5)
        for y in range(self.height):
            for x in range(self.width):
                v = (
                    math.sin(x * 0.06 + t) * 0.25 +
                    math.sin(y * 0.1 + t * 1.4) * 0.25 +
                    math.sin((x + y) * 0.04 + t * 0.8) * 0.25 +
                    math.sin(math.sqrt((x - self.width / 2) ** 2 + (y - self.height / 2) ** 2) * 0.05 + t) * 0.25
                )
                v = (v + 1) / 2
                if v < 0.15:
                    continue
                elif v < 0.3:
                    self._put(y, x, ord("·"), self.theme.anim_secondary | curses.A_DIM)
                elif v < 0.5:
                    self._put(y, x, ord("~"), self.theme.anim_secondary)
                elif v < 0.7:
                    self._put(y, x, ord("≈"), self.theme.anim_primary)
                elif v < 0.85:
                    self._put(y, x, ord("≋"), self.theme.anim_primary | curses.A_BOLD)
                else:
                    self._put(y, x, ord("█"), self.theme.highlight)

    # ═══════════════════════════════════════════════════
    # 6. RAIN — with lightning flashes
    # ═══════════════════════════════════════════════════

    def _init_rain(self):
        drops = []
        for _ in range(self.width // 2):
            drops.append({
                "x": random.randint(0, max(0, self.width - 1)),
                "y": random.randint(-self.height, 0),
                "sp": random.uniform(0.8, 2.0) * (self.speed / 5),
                "ch": random.choice(self.RAIN_CHARS),
                "w": random.uniform(-0.3, 0.1),
            })
        self.state["rain"] = drops
        self.state["splash"] = []
        self.state["lflash"] = 0

    def draw_rain(self):
        if "rain" not in self.state:
            self._init_rain()
        # Lightning
        if self.state["lflash"] > 0:
            self.state["lflash"] -= 1
            if self.state["lflash"] > 2:
                for y in range(0, self.height, 3):
                    for x in range(0, self.width, 4):
                        self._put(y, x, ord("░"), self.theme.highlight)
        elif random.random() < 0.004:
            self.state["lflash"] = 4
            lx = random.randint(5, max(6, self.width - 5))
            for ly in range(0, self.height // 2):
                self._put(ly, lx, ord("│"), self.theme.highlight)
                lx = max(0, min(self.width - 1, lx + random.randint(-2, 2)))
        # Splashes
        new_sp = []
        for sp in self.state["splash"]:
            if sp["l"] > 0:
                sz = 3 - sp["l"]
                for dx in range(-sz, sz + 1):
                    nx = sp["x"] + dx
                    if 0 <= nx < self.width and 0 <= sp["y"] < self.height:
                        self._put(sp["y"], nx, ord("·" if abs(dx) == sz else "°"), self.theme.anim_secondary)
                sp["l"] -= 1
                new_sp.append(sp)
        self.state["splash"] = new_sp
        for d in self.state["rain"]:
            y, x = int(d["y"]), int(d["x"])
            for i in range(3):
                dy = y - i
                if 0 <= dy < self.height and 0 <= x < self.width:
                    if i == 0:
                        self._put(dy, x, ord(d["ch"]), self.theme.anim_primary | curses.A_BOLD)
                    else:
                        self._put(dy, x, ord("│"), self.theme.anim_secondary | curses.A_DIM)
            d["y"] += d["sp"]
            d["x"] += d["w"]
            if y >= self.height - 1:
                self.state["splash"].append({"x": x, "y": self.height - 1, "l": 3})
                d["y"] = random.randint(-10, -1)
                d["x"] = random.randint(0, max(0, self.width - 1))

    # ═══════════════════════════════════════════════════
    # 7. DNA HELIX
    # ═══════════════════════════════════════════════════

    def draw_dna(self):
        t = self.frame * 0.1 * (self.speed / 5)
        cx = self.width // 2
        for y in range(self.height):
            o1 = int(math.sin(y * 0.3 + t) * 18)
            o2 = int(math.sin(y * 0.3 + t + math.pi) * 18)
            x1, x2 = cx + o1, cx + o2
            if 0 <= x1 < self.width:
                self._put(y, x1, ord(self.DNA_CHARS[y % 4]), self.theme.anim_primary | curses.A_BOLD)
            if 0 <= x2 < self.width:
                self._put(y, x2, ord(self.DNA_CHARS[(y + 2) % 4]), self.theme.anim_secondary | curses.A_BOLD)
            if abs(o1 - o2) > 2 and y % 2 == 0:
                mn, mx = min(x1, x2), max(x1, x2)
                for rx in range(mn + 1, mx):
                    if 0 <= rx < self.width:
                        p = (rx - mn) / max(1, mx - mn)
                        a = self.theme.anim_primary | curses.A_DIM if p < 0.5 else self.theme.anim_secondary | curses.A_DIM
                        self._put(y, rx, ord("─"), a)

    # ═══════════════════════════════════════════════════
    # 8. CYBER GRID — hacker pulse grid
    # ═══════════════════════════════════════════════════

    def draw_cyber_grid(self):
        t = self.frame * 0.06 * (self.speed / 5)
        cx, cy = self.width // 2, self.height // 2
        for y in range(self.height):
            for x in range(self.width):
                hl = (y % 4 == 0)
                vl = (x % 8 == 0)
                if not hl and not vl:
                    continue
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 * 4)
                pulse = math.sin(dist * 0.1 - t * 2) * 0.5 + 0.5
                if hl and vl:
                    ch, a = "┼", (self.theme.highlight if pulse > 0.7 else self.theme.anim_primary)
                elif hl:
                    ch = "─"
                    a = (self.theme.anim_primary | curses.A_BOLD) if pulse > 0.8 else (self.theme.anim_secondary if pulse > 0.4 else self.theme.anim_secondary | curses.A_DIM)
                else:
                    ch = "│"
                    a = (self.theme.anim_primary | curses.A_BOLD) if pulse > 0.8 else (self.theme.anim_secondary if pulse > 0.4 else self.theme.anim_secondary | curses.A_DIM)
                self._put(y, x, ord(ch), a)
        # Data nodes
        for y in range(0, self.height, 4):
            for x in range(0, self.width, 8):
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 * 4)
                if math.sin(dist * 0.08 - t * 3) * 0.5 + 0.5 > 0.85:
                    self._put(y, x, ord(random.choice(self.CYBER_CHARS)), self.theme.highlight)

    # ═══════════════════════════════════════════════════
    # 9. GLITCH — cyberpunk scanlines
    # ═══════════════════════════════════════════════════

    def draw_glitch(self):
        t = self.frame
        for y in range(self.height):
            intensity = math.sin(y * 0.5 + t * 0.2) * 0.5 + 0.5
            if intensity < 0.3:
                continue
            if y % 2 == 0:
                for x in range(0, self.width, 2):
                    self._put(y, x, ord("░" if intensity < 0.6 else "▒"), self.theme.anim_secondary | curses.A_DIM)
        for _ in range(2 + int(math.sin(t * 0.3) * 3 + 3)):
            gy = random.randint(0, max(0, self.height - 1))
            gx = random.randint(0, max(0, self.width - 10))
            for dx in range(random.randint(3, 15)):
                x = gx + dx
                if 0 <= x < self.width:
                    ch = random.choice(self.GLITCH_CHARS)
                    if random.random() < 0.3:
                        a = self.theme.highlight
                    elif random.random() < 0.5:
                        a = self.theme.anim_primary | curses.A_BOLD
                    else:
                        a = self.theme.anim_secondary
                    self._put(gy, x, ord(ch), a)
        for _ in range(5):
            y = random.randint(0, max(0, self.height - 1))
            x = random.randint(0, max(0, self.width - 10))
            self._puts(y, x, f"0x{random.randint(0, 0xFFFF):04X}", self.theme.anim_primary | curses.A_DIM)

    # ═══════════════════════════════════════════════════
    # 10. NAME PARTICLES — Abdelouahab Mostafa assembles
    # ═══════════════════════════════════════════════════

    def draw_name_particles(self):
        if "np" not in self.state:
            name = "Abdelouahab Mostafa"
            cx, cy = self.width // 2, self.height // 3
            particles = []
            for i, ch in enumerate(name):
                particles.append({
                    "c": ch, "x": random.uniform(0, self.width), "y": random.uniform(0, self.height),
                    "tx": cx - len(name) // 2 + i, "ty": cy,
                    "ok": False, "sp": 0, "tr": [],
                })
            sub = "  Mathematician · Hacker  "
            sub_p = []
            for i, ch in enumerate(sub):
                sub_p.append({
                    "c": ch, "x": random.uniform(0, self.width), "y": random.uniform(0, self.height),
                    "tx": cx - len(sub) // 2 + i, "ty": cy + 2,
                    "ok": False, "sp": 0, "dl": i * 2 + 50,
                })
            orbiters = []
            for i, ch in enumerate("◆◇●○★☆✦✧⊹◈"):
                orbiters.append({
                    "c": ch, "a": (2 * math.pi * i) / 10,
                    "r": 14, "sp": 0.03 + random.uniform(-0.01, 0.01),
                })
            self.state["np"] = particles
            self.state["np_sub"] = sub_p
            self.state["np_orb"] = orbiters
            self.state["np_f"] = 0

        self.state["np_f"] += 1
        f = self.state["np_f"]
        cx, cy = self.width // 2, self.height // 3
        ease = 0.09 * (self.speed / 5)

        # Name
        for p in self.state["np"]:
            if not p["ok"]:
                dx, dy = p["tx"] - p["x"], p["ty"] - p["y"]
                p["x"] += dx * ease
                p["y"] += dy * ease
                p["tr"].append((int(p["x"]), int(p["y"])))
                if len(p["tr"]) > 5:
                    p["tr"].pop(0)
                if abs(dx) < 0.3 and abs(dy) < 0.3:
                    p["x"], p["y"], p["ok"], p["sp"] = p["tx"], p["ty"], True, 12
            ix, iy = int(p["x"]), int(p["y"])
            if not p["ok"]:
                for tx, ty in p["tr"]:
                    if 0 <= tx < self.width and 0 <= ty < self.height:
                        self._put(ty, tx, ord("·"), self.theme.anim_secondary | curses.A_DIM)
            if 0 <= ix < self.width and 0 <= iy < self.height:
                if p["sp"] > 0:
                    self._put(iy, ix, ord(p["c"]), self.theme.highlight)
                    p["sp"] -= 1
                    for _ in range(2):
                        sx, sy = ix + random.randint(-3, 3), iy + random.randint(-2, 2)
                        if 0 <= sx < self.width and 0 <= sy < self.height:
                            self._put(sy, sx, ord(random.choice("✦✧⊹·*°")), self.theme.anim_secondary)
                elif p["ok"]:
                    glow = math.sin(f * 0.05 + ix * 0.2) * 0.5 + 0.5
                    self._put(iy, ix, ord(p["c"]), self.theme.highlight if glow > 0.8 else self.theme.anim_primary | curses.A_BOLD)
                else:
                    self._put(iy, ix, ord(p["c"]), self.theme.anim_secondary)

        # Subtitle
        for p in self.state["np_sub"]:
            if f < p["dl"]:
                continue
            if not p["ok"]:
                dx, dy = p["tx"] - p["x"], p["ty"] - p["y"]
                p["x"] += dx * 0.12
                p["y"] += dy * 0.12
                if abs(dx) < 0.3 and abs(dy) < 0.3:
                    p["x"], p["y"], p["ok"], p["sp"] = p["tx"], p["ty"], True, 8
            ix, iy = int(p["x"]), int(p["y"])
            if 0 <= ix < self.width and 0 <= iy < self.height:
                if p["sp"] > 0:
                    self._put(iy, ix, ord(p["c"]), self.theme.highlight)
                    p["sp"] -= 1
                elif p["ok"]:
                    self._put(iy, ix, ord(p["c"]), self.theme.accent)
                else:
                    self._put(iy, ix, ord(p["c"]), self.theme.anim_secondary | curses.A_DIM)

        # Orbiting math symbols
        for o in self.state["np_orb"]:
            o["a"] += o["sp"]
            ox = int(cx + math.cos(o["a"]) * o["r"] * 2)
            oy = int(cy + 1 + math.sin(o["a"]) * o["r"] * 0.6)
            if 0 <= ox < self.width and 0 <= oy < self.height:
                self._put(oy, ox, ord(o["c"]), self.theme.anim_primary)

    # ═══════════════════════════════════════════════════
    # DISPATCHER
    # ═══════════════════════════════════════════════════

    def draw_frame(self, animation_type="matrix"):
        self.update_size()
        self.frame += 1
        funcs = {
            "matrix": self.draw_matrix, "starfield": self.draw_starfield,
            "fire": self.draw_fire, "wave": self.draw_wave,
            "rain": self.draw_rain, "dna": self.draw_dna,
            "name": self.draw_name_particles, "cyber": self.draw_cyber_grid,
            "glitch": self.draw_glitch, "math": self.draw_math_rain,
        }
        funcs.get(animation_type, self.draw_matrix)()

    def render(self, animation_type="matrix", frame=None):
        """Alias for draw_frame (used by am_login.py)."""
        self.draw_frame(animation_type)

    def reset(self):
        self.state = {}
        self.frame = 0
