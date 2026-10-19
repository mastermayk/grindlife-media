"""Grind Life RPG TikTok toolkit (v4, rebuilt 2026-10-19).
Save Point pixel style. Frames are drawn with PIL, music/SFX synthesised with numpy,
encoded with ffmpeg (H.264 yuv420p 30fps 1080x1920 + AAC).
Backup copy lives in the public repo mastermayk/grindlife-media under build/.
"""
import math, os, random, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, '/workspace/grindlife-social')
import pixel  # noqa: E402

W, H, FPS = 1080, 1920, 30
FONT_DIR = '/workspace/grindlife-social/fonts/ttf'
C = dict(ink='#1E1530', cream='#FFF5DA', red='#FF4F6A', teal='#3ED6C4', gold='#FFC23D', purple='#8B5CF6',
         lilac='#B9A9F0', green='#7BD34A', orange='#FF8A3D', yellow='#FFE45C', shadow='#0B0816', panel='#1A1230',
         dim='#9C8FC7')

_fc = {}
def _font(file, size):
    k = (file, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONT_DIR, file), size, layout_engine=ImageFont.Layout.BASIC)
    return _fc[k]
def pix(s): return _font('PixelifySans.ttf', s)            # headings
def num(s): return _font('Silkscreen-Regular.ttf', max(28, s))  # numbers / tags (Pixelify 5 looks like S)
def tag(s): return _font('Silkscreen-Regular.ttf', max(28, s))
def body(s): return _font('AtkinsonHyperlegible-Regular.ttf', max(36, s))  # VT323 small c~o bug
def bodyb(s): return _font('AtkinsonHyperlegible-Bold.ttf', max(36, s))
def vt(s): return _font('VT323.ttf', max(44, s))

def ease(p): p = max(0., min(1., p)); return 1 - (1 - p) ** 3
def back(p):
    p = max(0., min(1., p)); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2
def appear(t, t0, d=0.25): return 0. if t < t0 else min(1., (t - t0) / d)

# ---------- background
_bg = {}
def background(seed=7, tower=True):
    if seed not in _bg:
        g = pixel.scene(180, 320, ground=262, seed=seed, moon=(146, 18), tower=(22, 74) if tower else None,
                        tank=None, stars=46, star_h=140, back=(16, 30), front=(10, 18))
        _bg[seed] = pixel.up(g, 6)
    return _bg[seed]
GROUND = 262 * 6

# ---------- sprites
EXTRA = {
 'couch': ["....KKKKKKKKKKKKKK....",
           "...KPPPPPPPPPPPPPPK...",
           "...KPKKPPPPPPPPKKPK...",
           "...KPPKKPPPPPPKKPPK...",
           "...KPPPRKPPPPKRPPPK...",
           "...KPPPPPPPPPPPPPPK...",
           "...KPPPPKKKKKKPPPPK...",
           ".KKKPPPKWKWKWKKPPPKKK.",
           "KppKKKKKKKKKKKKKKKKppK",
           "KppKBBBBBBBBBBBBBBKppK",
           "KppKBBBBBBBBBBBBBBKppK",
           "KppKKKKKKKKKKKKKKKKppK",
           "KKKKKKKKKKKKKKKKKKKKKK",
           ".KsK..............KsK."],
 'danfo': ["...KKKKKKKKKKKKKKKKK...",
           "..KGGGGGGGGGGGGGGGGGK..",
           ".KGKKKKGKKKKGKKKKGKKGK.",
           ".KGKTTKGKTTKGKTTKGKTKGK",
           "KGGKTTKGKTTKGKTTKGKTTKGK",
           "KGGKKKKGKKKKGKKKKGKKKKGK",
           "KGGGGGGGGGGGGGGGGGGGGGGK",
           "KKKKKKKKKKKKKKKKKKKKKKKK",
           "KGGGGGGGGGGGGGGGGGGGGGYK",
           "KGGGGGGGGGGGGGGGGGGGGGGK",
           "KKKKKKKKKKKKKKKKKKKKKKKK",
           "..KKKK..........KKKK....",
           ".KDDDDK........KDDDDK...",
           "..KKKK..........KKKK...."],
 'gem':   ["..KKKKK..", ".KAAWAAK.", "KAAAAAAAK", ".KAAAAAK.", "..KAAAK..", "...KAK...", "....K...."],
 'chest': [".KKKKKKKKKK.", "KggGGGGGGggK", "KgGGGGGGGGgK", "KKKKKYYKKKKK", "KgGGGKKGGGgK", "KgGGGGGGGGgK", "KKKKKKKKKKKK"],
}
for k, v in EXTRA.items():
    w = max(len(r) for r in v); pixel.SPR[k] = [r.ljust(w, '.') for r in v]

def sprite(img, name, x, y, s, recolor=None, outline=None):
    d = ImageDraw.Draw(img); rows = pixel.SPR[name]
    if outline:
        for yy, row in enumerate(rows):
            for xx, ch in enumerate(row):
                if ch != '.':
                    d.rectangle([x + xx * s - 4, y + yy * s - 4, x + xx * s + s + 3, y + yy * s + s + 3], fill=outline)
    for yy, row in enumerate(rows):
        for xx, ch in enumerate(row):
            if ch == '.': continue
            col = (recolor or {}).get(ch) or pixel.PAL.get(ch)
            if col: d.rectangle([x + xx * s, y + yy * s, x + xx * s + s - 1, y + yy * s + s - 1], fill=col)
def sprite_size(name, s): r = pixel.SPR[name]; return len(r[0]) * s, len(r) * s

def hero(img, t, x=110, s=9):
    bob = 6 if int(t * 4) % 2 else 0
    sprite(img, 'hero', x, GROUND - 24 * s - bob, s, outline='#4b3a85')

# ---------- drawing helpers
def text(d, xy, s, f, fill=C['cream'], anchor='la', sh=5, shc=C['shadow']):
    x, y = xy
    if sh: d.text((x + sh, y + sh), s, font=f, fill=shc, anchor=anchor)
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def _runs(s):
    out = []
    for ch in s:
        isd = ch.isdigit()
        if out and out[-1][0] == isd: out[-1][1] += ch
        else: out.append([isd, ch])
    return out

def text_mix(d, xy, s, size, fill=C['cream'], anchor='la', sh=5):
    """Pixelify heading with digits drawn in Silkscreen (Pixelify 5 reads as S)."""
    fp, fn = pix(size), num(int(size * 0.78))
    runs = _runs(s); wid = sum((fn if dg else fp).getlength(t_) for dg, t_ in runs)
    x, y = xy
    if anchor[0] == 'm': x -= wid / 2
    base_y = y + fp.getmetrics()[0]
    for dg, t_ in runs:
        f = fn if dg else fp
        if sh: d.text((x + sh, base_y + sh), t_, font=f, fill=C['shadow'], anchor='ls')
        d.text((x, base_y), t_, font=f, fill=fill, anchor='ls'); x += f.getlength(t_)
    return wid

def wrap(s, f, maxw):
    out, line = [], ''
    for w_ in s.split():
        tst = (line + ' ' + w_).strip()
        if f.getlength(tst) <= maxw: line = tst
        else: out.append(line); line = w_
    if line: out.append(line)
    return out

def box(d, x0, y0, x1, y1, border=C['purple'], fill=C['panel'], b=6):
    n = b  # notched pixel corners
    d.rectangle([x0 + n, y0, x1 - n, y1], fill=border); d.rectangle([x0, y0 + n, x1, y1 - n], fill=border)
    d.rectangle([x0 + b + n, y0 + b, x1 - b - n, y1 - b], fill=fill); d.rectangle([x0 + b, y0 + b + n, x1 - b, y1 - b - n], fill=fill)
    d.rectangle([x0 + b + n, y0 + b, x1 - b - n, y0 + b + 3], fill='#2c2254')  # inner highlight

def pill(d, x, y, s, f, fg=C['ink'], bg=C['gold'], pad=16, anchor='l'):
    w = f.getlength(s) + pad * 2; bb = f.getbbox('Ag'); h = bb[3] - bb[1] + pad * 1.2
    if anchor == 'm': x -= w / 2
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.rectangle([x + 4, y + h, x + w + 4, y + h + 4], fill=C['shadow'])
    d.text((x + pad, y + h / 2), s, font=f, fill=fg, anchor='lm')
    return x + w

def bar(d, x, y, w, h, p, col=C['green'], bg='#2a2150', border=C['ink']):
    d.rectangle([x - 4, y - 4, x + w + 4, y + h + 4], fill=border)
    d.rectangle([x, y, x + w, y + h], fill=bg)
    if p > 0: d.rectangle([x, y, x + int(w * max(0, min(1, p))), y + h], fill=col)
    for xx in range(x, x + w, 24): d.rectangle([xx, y, xx + 1, y + h], fill=border)

def flash(img, a):
    if a <= 0: return img
    return Image.blend(img, Image.new('RGB', img.size, '#FFF5DA'), min(1, a))

def shake(img, t, t0, dur=0.3, amp=18):
    if not (t0 <= t < t0 + dur): return img
    k = 1 - (t - t0) / dur; rnd = random.Random(int(t * 1000))
    dx, dy = int(rnd.uniform(-amp, amp) * k), int(rnd.uniform(-amp, amp) * k)
    out = Image.new('RGB', img.size, '#120d24'); out.paste(img, (dx, dy)); return out

def coins_burst(img, t, t0, cx, cy, n=8, s=6):
    if t < t0 or t > t0 + 0.9: return
    p = (t - t0) / 0.9; rnd = random.Random(int(t0 * 100))
    for i in range(n):
        ang = rnd.uniform(-math.pi * 0.9, -math.pi * 0.1); sp = rnd.uniform(260, 520)
        x = cx + math.cos(ang) * sp * p; y = cy + math.sin(ang) * sp * p + 900 * p * p
        sprite(img, 'coin', int(x), int(y), s)

def end_card_live(img, t, t0):
    """Live end card: drives to grindlife.kingzapp.dev (web app is live)."""
    d = ImageDraw.Draw(img); p = ease(appear(t, t0, 0.35)); off = int((1 - p) * 80)
    box(d, 110, 330 + off, 970, 1330 + off, border=C['gold'])
    # framed mini scene with hero
    fx, fy = 400, 400 + off
    mini = pixel.up(pixel.scene(46, 46, ground=40, seed=11, moon=(32, 4), tower=None, stars=14, back=(8, 10), front=(6, 8)), 6)
    d.rectangle([fx - 8, fy - 8, fx + 276 + 8, fy + 276 + 8], fill=C['gold']); img.paste(mini, (fx, fy))
    sprite(img, 'hero', fx + 66, fy + 276 - 24 * 6 - 18 - (6 if int(t * 4) % 2 else 0), 6)
    text(d, (540, 730 + off), 'GRIND LIFE RPG', pix(96), C['gold'], 'ma')
    bw = 420; d.rectangle([540 - bw // 2, 860 + off, 540 + bw // 2, 960 + off], fill=C['red'])
    d.rectangle([540 - bw // 2 + 6, 960 + off, 540 + bw // 2 + 6, 966 + off], fill=C['shadow'])
    pulse = 1 if int(t * 3) % 2 else 0
    text(d, (540, 910 + off), 'PLAY FREE', num(60 + pulse * 2), C['cream'], 'mm', sh=0)
    d.rectangle([150, 1010 + off, 930, 1110 + off], outline=C['gold'], width=5)
    text(d, (540, 1060 + off), 'grindlife.kingzapp.dev', vt(78), C['cream'], 'mm', sh=3)
    text(d, (540, 1150 + off), 'Free habit RPG in your browser', body(42), C['cream'], 'ma', sh=3)
    text(d, (540, 1215 + off), 'Built in Lagos by Kingzapp', body(38), C['lilac'], 'ma', sh=3)

# ---------- audio
SR = 44100
def _t(d): return np.arange(int(SR * d)) / SR
def sq(f, d, duty=0.5, v=0.2):
    if f <= 0: return np.zeros(int(SR * d))
    t = _t(d); w = np.where((t * f) % 1 < duty, 1., -1.) * v
    env = np.minimum(1, (len(t) - np.arange(len(t))) / (SR * 0.02)); return w * env
def tri(f, d, v=0.3):
    t = _t(d); return (2 * np.abs(2 * ((t * f) % 1) - 1) - 1) * v * np.minimum(1, (len(t) - np.arange(len(t))) / (SR * 0.02))
def noise(d, v=0.1, decay=30):
    t = _t(d); return np.random.default_rng(1).uniform(-1, 1, len(t)) * v * np.exp(-t * decay)
def kick(v=0.5):
    t = _t(0.18); f = 150 * np.exp(-t * 25) + 45; return np.sin(2 * np.pi * np.cumsum(f) / SR) * v * np.exp(-t * 18)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def put(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[:j - i]

def music(total, bpm=124, root=57, prog=(0, -4, 3, -2), seed=1, lead_pat=None):
    buf = np.zeros(int(SR * total) + SR); beat = 60 / bpm; s16 = beat / 4
    rnd = random.Random(seed); bar_len = beat * 4; nbars = int(total / bar_len) + 1
    pat = lead_pat or [0, 7, 12, 7, 3, 7, 10, 7, 0, 7, 12, 15, 12, 10, 7, 3]
    for b in range(nbars):
        r = root + prog[b % len(prog)]; t0 = b * bar_len
        minor = [0, 3, 7, 10, 12, 15] if prog[b % len(prog)] in (0, 3 - 3) else [0, 4, 7, 11, 12, 16]
        for i in range(16):
            n = pat[i]; n = min(minor, key=lambda m: abs(m - n)) if n not in minor else n
            put(buf, sq(mtof(r + 12 + n), s16 * 0.9, 0.25, 0.07), t0 + i * s16)
        for i in range(8):
            put(buf, tri(mtof(r - 12 + (7 if i % 4 == 3 else 0)), beat / 2 * 0.9, 0.22), t0 + i * beat / 2)
        for i in range(4):
            put(buf, kick(0.45), t0 + i * beat)
            put(buf, noise(0.05, 0.05, 80), t0 + i * beat + beat / 2)
            if i % 2 == 1: put(buf, noise(0.14, 0.12, 25), t0 + i * beat)
        if b % 2 == 1:  # little melody hook
            for k, n in enumerate([12, 15, 19, 17]):
                put(buf, sq(mtof(r + 24 + n - 12), beat / 2 * 0.8, 0.5, 0.045), t0 + 2 * beat + k * beat / 2)
    return buf[:int(SR * total)]

def sfx(kind):
    if kind == 'coin': return np.concatenate([sq(988, 0.06, 0.5, 0.18), sq(1319, 0.16, 0.5, 0.18)])
    if kind == 'hit': return noise(0.18, 0.35, 18) + np.pad(sq(110, 0.12, 0.5, 0.25), (0, int(SR * 0.06)))
    if kind == 'level': return np.concatenate([sq(mtof(m), 0.07, 0.5, 0.16) for m in (72, 76, 79, 84, 88)] + [sq(mtof(91), 0.25, 0.5, 0.16)])
    if kind == 'blip': return sq(1760, 0.03, 0.5, 0.08)
    if kind == 'whoosh':
        t = _t(0.25); return np.random.default_rng(2).uniform(-1, 1, len(t)) * 0.12 * np.sin(np.pi * t / 0.25)
    if kind == 'down': return np.concatenate([sq(mtof(m), 0.08, 0.5, 0.15) for m in (76, 72, 67, 60)])
    if kind == 'tick': return sq(2093, 0.02, 0.5, 0.07)
    raise ValueError(kind)

def soundtrack(total, events, path, **mk):
    m = music(total, **mk) * 0.75
    for at, kind in events: put(m, sfx(kind), at)
    n = int(SR * 0.6); m[-n:] *= np.linspace(1, 0, n)
    m = m / max(1e-6, np.abs(m).max()) * 0.89
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes())

# ---------- encode
def encode(frame_fn, total, wav, out):
    cmd = ['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
           '-profile:v', 'high', '-r', str(FPS), '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        p.stdin.write(frame_fn(i / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    assert p.returncode == 0, 'ffmpeg failed'
