"""Grind Life RPG TikToks, batch v5 (2026-10-22).
python3 videos_v5.py <slug>|all        -> ../v5-<slug>.mp4 (+ thumb)
python3 videos_v5.py <slug> frames     -> check/v5/<slug>_<t>.png
Slugs: full-clear, nepa-light, broke-goblin.
All numbers come from /workspace/grind-life-rpg/src:
  engine/config.ts (TUNING.quest, fullClear 25 XP / 15 coins / chest 5-25, hp.grindDayHeal 10, hp.perQuestHeal 2,
  hp.fullClearExtraHeal 5, grindSlots 3/4@L5/5@L10, grindDayThreshold 3), engine/game.ts (checkGrindDay / Full Clear),
  app/(tabs)/index.tsx ('Grind Day locked', 'Full Clear +25 XP' labels), data/quests.ts, data/campaigns.ts
  (broke-to-budgeted, CAMPAIGN_REWARDS, freePreviewDays 3, notice 'Guidance on habits, not financial advice.').
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import tk, pixel
from tk import text_mix, C, pix, num, tag, body, bodyb, vt, text, box, pill, bar, ease, back, appear, sprite, hero, wrap

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)

NEW = {
 'goblin': ["..K..........K..",
            ".KLK..KKKK..KLK.",
            ".KLLKKLLLLKKLLK.",
            "..KLLLLLLLLLLK..",
            "...KLLLLLLLLK...",
            "...KLWWLLWWLK...",
            "...KLWKLLKWLK...",
            "...KLLLLLLLLK...",
            "...KLKWKKWKLK...",
            "....KlLLLLlK....",
            "..KKKppppppKKK..",
            ".KLKpppGGpppKLK.",
            ".KLKppGKKGppKLK.",
            "..K.KppppppK.K..",
            "....KDDDDDDK....",
            "....KDDK.KDDK...",
            "...KKKK...KKKK.."],
 'chest_open': [".KKKKKKKKKK.", "KggGGGGGGggK", "KgGGGGGGGGgK", "KKKKKKKKKKKK", "KYWYYGYYWYYK", "KGYYWYYGYYGK",
                "KKKKKYYKKKKK", "KgGGGKKGGGgK", "KgGGGGGGGGgK", "KKKKKKKKKKKK"],
 'bulb':  ["...KKKK...", "..KYYYYK..", ".KYWYYYYK.", "KYWYYYYYYK", "KYWYOYOYYK", "KYYYOYOYYK", ".KYYYOYYK.", "..KYYOYK..", "...KYYK...",
           "...KBBK...", "...KKKK...", "...KBBK...", "...KKKK...", "....KK...."],
 'check': ["......KK", ".....KLK", "KK..KLK.", "KLKKLK..", ".KLLK...", "..KK...."],
}
for k, v in NEW.items():
    w = max(len(r) for r in v); pixel.SPR[k] = [r.ljust(w, '.') for r in v]
BULB_OFF = {'Y': '#4b3a85', 'W': '#6a56a8', 'O': '#3a2c6e', 'B': '#6a56a8'}

def base(t, seed=7): return tk.background(seed).copy()

_dark = {}
def dark_bg(seed):
    """Same Save Point skyline with every window light off (NEPA took light)."""
    if seed not in _dark:
        a = np.array(tk.background(seed)).copy(); reg = a[150 * 6:tk.GROUND]
        for col in ('#FFC23D', '#3ED6C4'):
            rgb = np.array([int(col[i:i + 2], 16) for i in (1, 3, 5)])
            m = (reg == rgb).all(-1); reg[m] = (34, 26, 66)
        a = (a * 0.72).astype(np.uint8)
        _dark[seed] = Image.fromarray(a)
    return _dark[seed]

def tickbox(d, img, x, y, ok):
    d.rectangle([x, y, x + 64, y + 64], fill=C['green'] if ok else '#2a2150', outline=C['ink'], width=5)
    if ok: sprite(img, 'check', x + 8, y + 14, 6, recolor={'L': C['cream']})

def quest_row(d, img, y, name, desc, xp, ok, p, w_desc=660):
    y += int((1 - p) * 50)
    box(d, 120, y, 960, y + 190, border=C['green'] if ok else C['purple'], fill='#221840')
    text(d, (160, y + 26), name, pix(54), C['cream'])
    for j, ln in enumerate(wrap(desc, body(36), w_desc)): text(d, (160, y + 96 + j * 42), ln, body(36), C['dim'], sh=0)
    pill(d, 750 if len(xp) < 7 else 730, y + 30, xp, num(32), bg=C['teal'])
    tickbox(d, img, 860, y + 106, ok)

# ======================================================= 1. full-clear (feature reveal)
FQ = [('Gym Session', 'You trained for 45+ minutes', '+35 XP'), ('Pay Yourself', 'Moved any amount into savings', '+20 XP'),
      ('Make Your Bed', 'Bed made before you leave the room', '+10 XP'), ('Deep Read', 'Read for 30 minutes', '+20 XP')]
FQ_T = [1.0, 2.1, 3.2, 4.7]  # tick times inside the quest beat
def fc_frame(t):
    img = base(t, 17); d = ImageDraw.Draw(img); hero(img, t)
    if t < 2.8:
        box(d, 80, 280, 1000, 1240, border=C['gold'])
        text(d, (540, 330), 'Clear EVERY quest', pix(84), C['cream'], 'ma')
        text(d, (540, 430), 'today and you open', pix(84), C['cream'], 'ma')
        sc = 1 + 0.04 * abs(((t * 2) % 2) - 1)
        text(d, (540, 540), 'A LOOT CHEST', pix(int(118 * sc)), C['gold'], 'ma')
        s = 28; cw, ch = tk.sprite_size('chest', s); wob = [0, 6, 0, -6][int(t * 10) % 4] if t > 0.4 else 0
        sprite(img, 'chest', 540 - cw // 2 + wob, 700, s, outline=C['ink'])
        if t > 1.0:
            p = ease(appear(t, 1.0, 0.3))
            pill(d, 540, 1010 + int((1 - p) * 30), 'IT IS CALLED A FULL CLEAR', tag(36), bg=C['purple'], fg=C['cream'], anchor='m')
            text(d, (540, 1120), 'Real habits. Real loot.', bodyb(46), C['teal'], 'ma', sh=3)
    elif t < 8.8:
        lt = t - 2.8; box(d, 80, 240, 1000, 1345)
        done = sum(1 for x in FQ_T if lt > x)
        text(d, (540, 280), "TODAY'S GRIND: 4 QUESTS", tag(36), C['lilac'], 'ma', sh=3)
        locked = done >= 3
        if not locked:
            gw_ = num(52).getlength('GRIND 3/3'); text(d, (130, 350), f'GRIND {done}/3', num(52), C['gold'])
            bar(d, int(130 + gw_ + 40), 362, int(940 - (130 + gw_ + 40)), 38, done / 3, col=C['green'])
        else:
            q = back(appear(lt, FQ_T[2], 0.25))
            d.rectangle([120, 336, 960, 420], fill=C['green'] if done < 4 else C['gold'])
            text(d, (150, 378), 'GRIND DAY LOCKED' if done < 4 else 'FULL CLEAR!', pix(int(48 * max(.6, min(1.15, q)))), C['ink'], 'lm', sh=0)
            if done < 4: text(d, (935, 378), 'Full Clear +25 XP', tag(28), C['ink'], 'rm', sh=0)
        for i, (n, desc, xp) in enumerate(FQ):
            p = ease(appear(lt, 0.15 + i * 0.2, 0.3))
            if p > 0: quest_row(d, img, 450 + i * 200, n, desc, xp, lt > FQ_T[i], p)
        if locked and done < 4:
            text(d, (540, 1268), 'One more = FULL CLEAR', bodyb(44), C['gold'], 'ma', sh=3)
        img = tk.flash(img, max(0, 1 - (lt - FQ_T[3]) / 0.2) if FQ_T[3] < lt < FQ_T[3] + 0.2 else 0)
    elif t < 13.2:
        lt = t - 8.8; box(d, 80, 260, 1000, 1290, border=C['gold'])
        p = back(appear(lt, 0, 0.3))
        text(d, (540, 300), 'FULL CLEAR', pix(int(116 * max(.3, p))), C['gold'], 'ma')
        s = 19
        if lt < 0.6:
            cw, ch = tk.sprite_size('chest', s); wob = [0, 8, 0, -8][int(lt * 14) % 4]
            sprite(img, 'chest', 540 - cw // 2 + wob, 460, s, outline=C['ink'])
        else:
            cw, ch = tk.sprite_size('chest_open', s)
            sprite(img, 'chest_open', 540 - cw // 2, 440, s, outline=C['ink'])
        tk.coins_burst(img, t, 8.8 + 0.6, 540, 520, n=12)
        rows = [(1.0, '+25 XP', C['teal']), (1.4, '+15 COINS', C['gold'])]
        for at, s_, col in rows:
            if lt > at: pill(d, 300 if s_ == '+25 XP' else 650, 680, s_, num(46), bg=col, anchor='m')
        if lt > 1.8:
            text(d, (540, 780), 'BONUS CHEST', tag(36), C['lilac'], 'ma', sh=3)
            roll = 18 if lt > 2.8 else 5 + (int(lt * 23) % 21)
            text(d, (540, 830), f'+{roll} COINS', num(84), C['gold'] if lt > 2.8 else C['cream'], 'ma')
            text(d, (540, 950), 'rolls 5 to 25 every day', body(38), C['dim'], 'ma', sh=0)
        if lt > 3.2:
            sprite(img, 'heart', 230, 1060, 8); text(d, (330, 1092), '+5 HP extra heal', bodyb(48), C['red'], 'lm', sh=3)
            text(d, (540, 1170), '(+15 HP total with the Grind Day)', body(36), C['dim'], 'ma', sh=0)
        img = tk.flash(img, 1 - (lt - 0.6) / 0.18 if 0.6 <= lt < 0.78 else 0)
    else:
        tk.end_card_live(img, t, 13.2)
    return img
FC = dict(total=16.3, frame=fc_frame, seed=11, music=dict(bpm=126, root=55, prog=(0, -4, 3, -2)),
          events=[(0.4, 'blip'), (1.0, 'blip'), (2.8, 'whoosh')] + [(2.8 + x, 'coin') for x in FQ_T[:3]] + [(2.8 + FQ_T[2] + 0.05, 'blip'), (2.8 + FQ_T[3], 'level'),
                  (8.8, 'whoosh'), (9.4, 'hit'), (9.4, 'coin'), (9.8, 'coin'), (10.2, 'coin')] + [(8.8 + 1.8 + k * 0.1, 'tick') for k in range(10)]
                 + [(11.6, 'coin'), (12.0, 'blip'), (13.2, 'whoosh')],
          checks=[0.0, 1.5, 4.5, 6.4, 8.2, 9.2, 11.0, 12.6, 15.0])

# ======================================================= 2. nepa-light (Lagos POV humour)
NQ = [('Home Burner', '20-minute home workout or 50 push-ups', '+20 XP'), ('Still Mind', '10 minutes of meditation', '+10 XP'),
      ('Lights Out', 'In bed by your target bedtime', '+20 XP')]
NQ_T = [1.2, 2.9, 4.6]
OFF_AT, BACK_AT = 0.35, 12.2
def nepa_frame(t):
    lit = t < OFF_AT or t >= BACK_AT
    img = (base(t, 21) if lit else dark_bg(21).copy()); d = ImageDraw.Draw(img); hero(img, t, x=90)
    if t < 3.0:
        box(d, 80, 280, 1000, 1240, border=C['red'])
        text(d, (540, 330), 'POV:', pix(84), C['cream'], 'ma')
        text(d, (540, 430), 'NEPA took light', pix(100), C['gold'], 'ma')
        s = 14; bw_, bh_ = tk.sprite_size('bulb', s)
        sprite(img, 'bulb', 540 - bw_ // 2, 570, s, recolor=BULB_OFF if t >= OFF_AT else None, outline=C['ink'])
        pill(d, 540, 790 + 20, 'LIGHT: OFF' if t >= OFF_AT else 'LIGHT: ON', num(48), bg=C['red'] if t >= OFF_AT else C['green'], fg=C['cream'], anchor='m')
        if t > 1.1:
            p = ease(appear(t, 1.1, 0.3)); y = 960 + int((1 - p) * 30)
            text(d, (540, y), '...and the grind', bodyb(54), C['cream'], 'ma', sh=3)
            text(d, (540, y + 66), 'DID NOT STOP', bodyb(60), C['teal'], 'ma', sh=3)
    elif t < 10.0:
        lt = t - 3.0; done = sum(1 for x in NQ_T if lt > x)
        box(d, 80, 260, 1000, 1240)
        text(d, (540, 300), "QUESTS THAT DON'T NEED LIGHT", tag(34), C['lilac'], 'ma', sh=3)
        gw_ = num(52).getlength('GRIND 3/3'); text(d, (130, 370), f'GRIND {done}/3', num(52), C['gold'])
        bar(d, int(130 + gw_ + 40), 382, int(940 - (130 + gw_ + 40)), 38, done / 3, col=C['green'])
        for i, (n, desc, xp) in enumerate(NQ):
            p = ease(appear(lt, 0.2 + i * 1.7, 0.3))
            if p > 0: quest_row(d, img, 490 + i * 230, n, desc, xp, lt > NQ_T[i], p)
        if lt > NQ_T[2] + 0.2:
            pill(d, 540, 1170, 'NEPA SAID BEDTIME', tag(32), bg=C['gold'], anchor='m')
    elif t < BACK_AT:
        lt = t - 10.0; box(d, 80, 320, 1000, 1180, border=C['gold'])
        p = back(appear(lt, 0, 0.3))
        text(d, (540, 380), 'LIGHT: OFF', pix(int(104 * max(.3, p))), '#6a56a8', 'ma')
        text(d, (540, 500), 'STREAK: ON', pix(int(118 * max(.3, p))), C['orange'], 'ma')
        sprite(img, 'flame', 540 - 64, 630, 16, outline=C['ink'])
        if lt > 0.6:
            sprite(img, 'heart', 230, 800, 8); text(d, (330, 832), '+10 HP Grind Day heal', bodyb(48), C['red'], 'lm', sh=3)
        if lt > 1.0:
            sprite(img, 'heart', 230, 910, 8); text(d, (330, 942), '+2 HP for every quest', bodyb(48), C['red'], 'lm', sh=3)
        if lt > 1.4:
            text(d, (540, 1050), 'Light go, streak no go.', bodyb(52), C['teal'], 'ma', sh=3)
        img = tk.flash(img, 1 - lt / 0.18 if lt < 0.18 else 0)
    elif t < 13.6:
        lt = t - BACK_AT; box(d, 80, 420, 1000, 1080, border=C['green'])
        p = back(appear(lt, 0, 0.3))
        s = 14; bw_, bh_ = tk.sprite_size('bulb', s)
        sprite(img, 'bulb', 540 - bw_ // 2, 470, s, outline=C['ink'])
        text(d, (540, 700), 'UP NEPA!', pix(int(140 * max(.3, p))), C['gold'], 'ma', sh=8)
        text(d, (540, 880), '(you already secured the day)', body(40), C['cream'], 'ma', sh=3)
        img = tk.flash(img, 1 - lt / 0.2 if lt < 0.2 else 0)
    else:
        tk.end_card_live(img, t, 13.6)
    return img
NEPA = dict(total=16.6, frame=nepa_frame, seed=13, music=dict(bpm=120, root=53, prog=(0, 3, -4, -2)),
            events=[(OFF_AT, 'down'), (1.1, 'blip'), (3.0, 'whoosh')] + sum([[(3.0 + 0.2 + i * 1.7, 'blip'), (3.0 + NQ_T[i], 'coin')] for i in range(3)], [])
                   + [(3.0 + NQ_T[2] + 0.2, 'blip'), (10.0, 'level'), (10.6, 'coin'), (11.0, 'coin'), (BACK_AT, 'level'), (13.6, 'whoosh')],
            checks=[0.0, 0.3, 1.8, 5.0, 7.0, 9.6, 11.8, 12.9, 15.3])

# ======================================================= 3. broke-goblin (money / campaign)
BW = [('WEEK 1', 'See it', 'Find your top 3 money leaks'), ('WEEK 2', 'Plan it', 'Create a separate savings pot or account'),
      ('WEEK 3', 'Plug leaks', 'Shop around or negotiate one bill'), ('WEEK 4', 'Grow it', 'Write a simple offer: what, for whom, at what price')]
def broke_frame(t):
    img = base(t, 19); d = ImageDraw.Draw(img); hero(img, t)
    if t < 2.9:
        box(d, 80, 280, 1000, 1260, border=C['red'])
        text(d, (540, 320), '"Where does my', pix(82), C['cream'], 'ma')
        text(d, (540, 415), 'money go?"', pix(82), C['cream'], 'ma')
        sc = 1 + 0.04 * abs(((t * 2) % 2) - 1)
        text(d, (540, 520), 'is now a BOSS', pix(int(112 * sc)), C['red'], 'ma')
        s = 17; gw_, gh_ = tk.sprite_size('goblin', s); bob = 8 if int(t * 3) % 2 else 0
        sprite(img, 'goblin', 540 - gw_ // 2, 690 - bob, s, outline=C['ink'])
        for k, cx in enumerate((230, 850)):
            cy = 800 + int(30 * abs(((t * 1.6 + k * 0.5) % 2) - 1)); sprite(img, 'coin', cx - 36, cy, 9, outline=C['ink'])
        if t > 0.9:
            pill(d, 540, 1100, 'DAY 30 BOSS: THE BROKE GOBLIN', tag(34), bg=C['red'], fg=C['cream'], anchor='m')
    elif t < 8.4:
        lt = t - 2.9; box(d, 80, 240, 1000, 1290)
        pill(d, 130, 290, 'CAMPAIGN: BROKE TO BUDGETED', tag(34), bg=C['purple'], fg=C['cream'])
        mk = min(3, int(max(0, lt - 0.3) / 1.1))
        for i, (w, title, task) in enumerate(BW):
            p = ease(appear(lt, 0.2 + i * 0.25))
            if p <= 0: continue
            y = 420 + i * 200 + int((1 - p) * 40)
            if i < 3: d.rectangle([186, y + 70, 194, y + 200], fill='#4b3a85')
            on = i <= mk
            d.rectangle([150, y, 230, y + 80], fill=C['gold'] if on else '#4b3a85', outline=C['ink'], width=5)
            text(d, (190, y + 40), str(i + 1), num(44), C['ink'], 'mm', sh=0)
            text_mix(d, (270, y - 4), f'{w}: {title}', 54, C['cream'] if on else C['dim'])
            for j, ln in enumerate(wrap(task, body(36), 660)): text(d, (270, y + 66 + j * 42), ln, body(36), C['dim'], sh=0)
        if lt > 1.0:
            text(d, (540, 1210), 'No-Spend Days on Day 6, 15 and 26', body(38), C['lilac'], 'ma', sh=3)
    elif t < 13.8:
        lt = t - 8.4; box(d, 80, 240, 1000, 1290, border=C['red'])
        text(d, (540, 280), 'DAY 30', tag(44), C['lilac'], 'ma', sh=3)
        text(d, (540, 330), 'THE BROKE GOBLIN', pix(84), C['red'], 'ma')
        steps = [(0.4, 'Compare to your Day 3 baseline'), (1.2, 'Final review'), (2.0, 'Commit to month 2')]
        for i, (at, s_) in enumerate(steps):
            if lt > at - 0.2:
                y = 470 + i * 84; ok = lt > at
                tickbox(d, img, 150, y, ok); text(d, (240, y + 32), s_, bodyb(44), C['cream'] if ok else C['dim'], 'lm', sh=3)
        dead = lt > 2.6; s = 14; gw_, gh_ = tk.sprite_size('goblin', s)
        if lt < 2.3 or (lt < 2.6 and int(lt * 20) % 2):
            sprite(img, 'goblin', 540 - gw_ // 2, 740, s, outline=C['ink'])
        if dead:
            p = back(appear(lt, 2.6, 0.25))
            text(d, (540, 770), 'DEFEATED', pix(int(130 * max(.3, p))), C['gold'], 'ma', sh=8)
        if lt > 3.0:
            pill(d, 300, 1010, '+1,000 XP', num(44), bg=C['teal'], anchor='m'); pill(d, 740, 1010, '+500 COINS', num(44), bg=C['gold'], anchor='m')
        if lt > 3.9:
            text(d, (540, 1140), 'First 3 days free.', body(38), C['cream'], 'ma', sh=3)
            text(d, (540, 1192), 'Guidance on habits, not financial advice.', body(36), C['dim'], 'ma', sh=0)
        tk.coins_burst(img, t, 8.4 + 2.7, 540, 820, n=12)
        img = tk.shake(img, t, 8.4 + 2.6, 0.35)
    else:
        tk.end_card_live(img, t, 13.8)
    return img
BROKE = dict(total=16.8, frame=broke_frame, seed=17, music=dict(bpm=128, root=52, prog=(0, -2, -4, 3)),
             events=[(0.3, 'coin'), (0.9, 'blip'), (1.4, 'coin'), (2.9, 'whoosh')] + [(2.9 + 0.3 + i * 1.1, 'tick') for i in range(4)] + [(3.9, 'blip'), (8.4, 'whoosh')]
                    + [(8.4 + a, 'coin') for a in (0.4, 1.2, 2.0)] + [(11.0, 'hit'), (11.1, 'coin'), (11.4, 'level'), (12.3, 'blip'), (13.8, 'whoosh')],
             checks=[0.0, 1.5, 4.0, 6.9, 9.5, 10.9, 12.0, 13.4, 15.5])

VIDEOS = {'full-clear': FC, 'nepa-light': NEPA, 'broke-goblin': BROKE}
THUMB_T = {'full-clear': 1.5, 'nepa-light': 1.8, 'broke-goblin': 1.5}

def render(slug):
    v = VIDEOS[slug]; wav = f'/tmp/v5-{slug}.wav'
    tk.soundtrack(v['total'], v['events'], wav, seed=v['seed'], **v['music'])
    out = os.path.join(OUT, f'v5-{slug}.mp4'); tk.encode(v['frame'], v['total'], wav, out)
    v['frame'](THUMB_T[slug]).save(os.path.join(OUT, f'v5-{slug}-thumb.png'))
    print(out)

def frames(slug):
    v = VIDEOS[slug]; os.makedirs(os.path.join(HERE, 'check', 'v5'), exist_ok=True)
    for t in v['checks']: v['frame'](t).save(os.path.join(HERE, 'check', 'v5', f'{slug}_{t:04.1f}.png'))

if __name__ == '__main__':
    slugs = list(VIDEOS) if sys.argv[1] == 'all' else [sys.argv[1]]
    for s in slugs: (frames if len(sys.argv) > 2 and sys.argv[2] == 'frames' else render)(s)
