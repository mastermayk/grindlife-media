"""Grind Life RPG TikToks, batch v4 (2026-10-19).
python3 videos_v4.py <slug>|all        -> ../v4-<slug>.mp4
python3 videos_v4.py <slug> frames     -> check/v4/<slug>_<t>.png
All numbers come from /workspace/grind-life-rpg/src (engine/config.ts, engine/rank.ts, data/quests.ts, data/campaigns.ts).
"""
import os, sys
from PIL import Image, ImageDraw
import tk
from tk import text_mix, C, pix, num, tag, body, bodyb, vt, text, box, pill, bar, ease, back, appear, sprite, hero, wrap

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)

def base(t, seed=7):
    return tk.background(seed).copy()

# ======================================================= 1. rank-diamond
RANKS = [('BRONZE', 12, '#D08A4E'), ('SILVER', 16, '#D7D9E6'), ('GOLD', 20, '#FFC23D'), ('PLATINUM', 24, '#3ED6C4'), ('DIAMOND', 27, '#8BE9FF')]
def rank_frame(t):
    img = base(t, 7); d = ImageDraw.Draw(img); hero(img, t)
    if t < 2.6:
        sc = 1 + 0.03 * abs(((t * 2) % 2) - 1)
        box(d, 80, 300, 1000, 1000, border=C['purple'])
        text(d, (540, 380), 'Your consistency', pix(int(84 * sc)), C['cream'], 'ma')
        text(d, (540, 480), 'has a', pix(int(84 * sc)), C['cream'], 'ma')
        text(d, (540, 590), 'RANK NOW', pix(int(124 * sc)), C['gold'], 'ma')
        p = back(appear(t, 0.8, 0.35))
        if p > 0:
            s = max(1, int(14 * p)); gw, gh = tk.sprite_size('gem', s)
            sprite(img, 'gem', 540 - gw // 2, 880 - gh // 2 + 20, s, recolor={'A': '#8BE9FF'}, outline=C['ink'])
            text(d, (540, 760), 'Can you hit DIAMOND?', bodyb(54), C['teal'], 'ma')
    elif t < 6.2:
        lt = t - 2.6; box(d, 80, 300, 1000, 1120)
        pill(d, 130, 350, 'RANKED CYCLE', tag(34), bg=C['purple'], fg=C['cream'])
        rows = [('30', 'days in every ranked cycle'), ('3', 'quests done = 1 Grind Day'), ('4', 'Rest Days count too (max 4)'), ('=', 'Score = Grind Days + Rest Days')]
        for i, (n, s) in enumerate(rows):
            p = ease(appear(lt, 0.25 + i * 0.75)); 
            if p <= 0: continue
            y = 480 + i * 150 + int((1 - p) * 40)
            text(d, (230, y + 40), n, num(72), C['gold'], 'mm')
            for j, ln in enumerate(wrap(s, body(46), 640)): text(d, (310, y + j * 54 + 10), ln, body(46), C['cream'], sh=3)
    elif t < 11.0:
        lt = t - 6.2; box(d, 80, 260, 1000, 1240)
        score = min(27, int(max(0, lt - 0.3) / 3.7 * 27))
        text(d, (540, 300), 'CONSISTENCY SCORE', tag(40), C['lilac'], 'ma', sh=3)
        text(d, (540, 360), f'{score} / 30', num(96), C['cream'], 'ma')
        bar(d, 140, 500, 800, 34, score / 30, col=C['teal'])
        for i, (name, thr, col) in enumerate(RANKS):
            y = 1110 - i * 120; lit = score >= thr
            if lit: d.rectangle([130, y - 50, 950, y + 50], fill='#2a1f4f')
            sprite(img, 'gem', 160, y - 35, 10, recolor={'A': col if lit else '#4b3a85', 'W': '#FFFFFF' if lit else '#6a56a8'})
            text(d, (280, y), name, pix(64), col if lit else '#6a56a8', 'lm', sh=4 if lit else 0)
            text(d, (930, y), f'{thr}+ days', num(40), C['cream'] if lit else '#6a56a8', 'rm', sh=3 if lit else 0)
    elif t < 13.5:
        lt = t - 11.0; box(d, 80, 330, 1000, 1150, border=C['gold'])
        p = back(appear(lt, 0, 0.3)); s = max(1, int(16 * p)); gw, gh = tk.sprite_size('gem', s)
        sprite(img, 'gem', 540 - gw // 2, 400, s, recolor={'A': '#8BE9FF'}, outline=C['ink'])
        text(d, (540, 560), 'PROMOTED!', pix(int(130 * max(.3, p))), C['gold'], 'ma')
        if lt > 0.5:
            pill(d, 540, 740, '+200 XP', num(52), bg=C['teal'], anchor='m')
        if lt > 0.8:
            pill(d, 540, 850, '+150 COINS', num(52), bg=C['gold'], anchor='m')
        if lt > 1.2:
            text(d, (540, 990), 'Up 1 tier per cycle.', body(46), C['cream'], 'ma', sh=3)
            text(d, (540, 1050), 'Slack off? Drop 1.', bodyb(46), C['red'], 'ma', sh=3)
        tk.coins_burst(img, t, 11.8, 540, 900)
        img = tk.flash(img, 1 - lt / 0.18 if lt < 0.18 else 0)
    else:
        tk.end_card_live(img, t, 13.5)
    return img
RANK = dict(total=16.5, frame=rank_frame, seed=3, music=dict(bpm=124, root=57, prog=(0, -4, 3, -2)),
            events=[(2.6, 'whoosh'), (2.85, 'blip'), (3.6, 'blip'), (4.35, 'blip'), (5.1, 'blip'), (6.2, 'whoosh')]
                   + [(6.5 + thr / 27 * 3.7, 'coin') for _, thr, _ in RANKS] + [(11.0, 'level'), (11.5, 'coin'), (11.8, 'coin'), (13.5, 'whoosh')],
            checks=[0.0, 1.5, 4.0, 5.9, 8.0, 10.6, 12.6, 15.5])

# ======================================================= 2. lagos-traffic
TQ = [('Learn On the Move', '30 min podcast or audiobook'), ('Three Lines', 'Journal 3 lines or 3 things you are grateful for'), ('Plan Tomorrow', "Write tomorrow's top 3 tasks")]
def traffic_frame(t):
    img = base(t, 9); d = ImageDraw.Draw(img)
    # danfo crawling in traffic behind the hero
    dx = 1080 - 120 - int((t * 14) % 40) - 260
    if t < 13.4:
        sprite(img, 'danfo', dx, tk.GROUND - 14 * 9 - 6, 9, outline='#4b3a85')
    hero(img, t, x=60)
    if t < 2.8:
        box(d, 80, 300, 1000, 1080, border=C['gold'])
        text(d, (540, 360), 'POV:', pix(84), C['cream'], 'ma')
        text(d, (540, 460), 'Lagos traffic', pix(100), C['gold'], 'ma')
        text_mix(d, (540, 580), 'ate 3 hours', 100, C['gold'], 'ma')
        mins = 178 + int(t * 6)
        pill(d, 540, 730, f'STUCK {mins // 60}H {mins % 60:02d}M', num(44), bg=C['red'], fg=C['cream'], anchor='m')
        if t > 0.9:
            p = ease(appear(t, 0.9, 0.3)); y = 880 + int((1 - p) * 30)
            text(d, (540, y), '...and you STILL secured', bodyb(50), C['cream'], 'ma', sh=3)
            text(d, (540, y + 62), 'the Grind Day', bodyb(50), C['teal'], 'ma', sh=3)
    elif t < 9.6:
        lt = t - 2.8; done = sum(1 for i in range(3) if lt > 0.2 + i * 1.9 + 1.1)
        box(d, 80, 260, 1000, 1240)
        text(d, (540, 300), 'QUESTS YOU CAN DO IN A DANFO', tag(36), C['lilac'], 'ma', sh=3)
        gw_ = num(56).getlength('GRIND 3/3'); text(d, (130, 380), f'GRIND {done}/3', num(56), C['gold'])
        bar(d, int(130 + gw_ + 40), 392, int(940 - (130 + gw_ + 40)), 40, done / 3, col=C['green'])
        for i, (n, desc) in enumerate(TQ):
            p = ease(appear(lt, 0.2 + i * 1.9, 0.3))
            if p <= 0: continue
            y = 500 + i * 240 + int((1 - p) * 60)
            ok = lt > 0.2 + i * 1.9 + 1.1
            box(d, 120, y, 960, y + 210, border=C['green'] if ok else C['purple'], fill='#221840')
            text(d, (160, y + 30), n, pix(56), C['cream'])
            for j, ln in enumerate(wrap(desc, body(38), 560)): text(d, (160, y + 100 + j * 44), ln, body(38), C['dim'], sh=0)
            pill(d, 730, y + 34, '+10 XP', num(34), bg=C['teal'])
            if ok:
                d.rectangle([860, y + 120, 920, y + 180], fill=C['green'])
                text(d, (890, y + 150), 'OK', num(30), C['ink'], 'mm', sh=0)
    elif t < 13.4:
        lt = t - 9.6; box(d, 80, 300, 1000, 1200, border=C['gold'])
        p = back(appear(lt, 0, 0.3))
        text(d, (540, 360), 'GRIND DAY', pix(int(120 * max(.3, p))), C['gold'], 'ma')
        text(d, (540, 500), 'SECURED', pix(int(120 * max(.3, p))), C['gold'], 'ma')
        if lt > 0.5:
            sprite(img, 'heart', 250, 680, 8); text(d, (350, 712), '+10 HP heal', bodyb(52), C['red'], 'lm', sh=3)
        if lt > 0.9:
            sprite(img, 'flame', 254, 800, 8); text(d, (350, 836), 'Streak still alive', bodyb(52), C['orange'], 'lm', sh=3)
        if lt > 1.4:
            text(d, (540, 950), 'STREAK XP BOOST', tag(36), C['lilac'], 'ma', sh=3)
            tiers = [('3D', '1.1x'), ('7D', '1.2x'), ('14D', '1.3x'), ('30D', '1.4x'), ('60D', '1.5x')]
            for i, (a, b_) in enumerate(tiers):
                x = 160 + i * 160; q = ease(appear(lt, 1.5 + i * 0.12, 0.2))
                if q <= 0: continue
                d.rectangle([x, 1010, x + 140, 1140], fill='#2a1f4f', outline=C['orange'], width=4)
                text(d, (x + 70, 1045), a, num(34), C['cream'], 'mm', sh=0)
                text(d, (x + 70, 1105), b_, num(36), C['gold'], 'mm', sh=0)
        img = tk.flash(img, 1 - lt / 0.18 if lt < 0.18 else 0)
    else:
        tk.end_card_live(img, t, 13.4)
    return img
TRAFFIC = dict(total=16.5, frame=traffic_frame, seed=5, music=dict(bpm=118, root=55, prog=(0, 3, -2, -4)),
               events=[(0.9, 'blip'), (2.8, 'whoosh')] + sum([[(2.8 + 0.2 + i * 1.9, 'blip'), (2.8 + 0.2 + i * 1.9 + 1.1, 'coin')] for i in range(3)], [])
                      + [(9.6, 'level'), (10.1, 'coin'), (10.5, 'blip')] + [(9.6 + 1.5 + i * 0.12, 'tick') for i in range(5)] + [(13.4, 'whoosh')],
               checks=[0.0, 1.6, 4.2, 6.4, 9.3, 11.8, 15.4])

# ======================================================= 3. couch-titan
WEEKS = [('WEEK 1', 'Start moving', '8 x (60 s jog, 90 s walk)'), ('WEEK 2', 'Build', '5 x (2 min jog, 2 min walk)'),
         ('WEEK 3', 'Longer runs', '3 x (6 min jog, 2 min walk)'), ('WEEK 4', 'Go the distance', '15-minute continuous jog')]
def couch_frame(t):
    img = base(t, 13); d = ImageDraw.Draw(img); hero(img, t)
    if t < 2.8:
        box(d, 80, 300, 1000, 1240, border=C['red'])
        text_mix(d, (540, 350), 'Couch to 5K, but', 78, C['cream'], 'ma')
        text(d, (540, 450), 'the final boss is', pix(78), C['cream'], 'ma')
        text(d, (540, 560), 'YOUR COUCH', pix(124), C['red'], 'ma')
        s = 18; cw, ch = tk.sprite_size('couch', s); bob = 8 if int(t * 3) % 2 else 0
        sprite(img, 'couch', 540 - cw // 2, 760 - bob, s, outline=C['ink'])
        if t > 1.0:
            pill(d, 540, 1060, 'DAY 30 BOSS: THE COUCH TITAN', tag(36), bg=C['red'], fg=C['cream'], anchor='m')
    elif t < 7.6:
        lt = t - 2.8; box(d, 80, 260, 1000, 1260)
        pill(d, 130, 310, 'CAMPAIGN: COUCH TO 5K', tag(34), bg=C['purple'], fg=C['cream'])
        mk = min(3, int(max(0, lt - 0.3) / 1.0))
        for i, (w, title, task) in enumerate(WEEKS):
            p = ease(appear(lt, 0.2 + i * 0.25)); 
            if p <= 0: continue
            y = 440 + i * 200 + int((1 - p) * 40)
            if i < 3: d.rectangle([186, y + 70, 194, y + 200], fill='#4b3a85')
            on = i <= mk
            d.rectangle([150, y, 230, y + 80], fill=C['gold'] if on else '#4b3a85', outline=C['ink'], width=5)
            text(d, (190, y + 40), str(i + 1), num(44), C['ink'], 'mm', sh=0)
            text_mix(d, (270, y - 4), f'{w}: {title}', 54, C['cream'] if on else C['dim'])
            text(d, (270, y + 66), task, body(38), C['dim'], sh=0)
        text(d, (540, 1180), 'Checkpoints on Day 7, 14 and 21', body(38), C['lilac'], 'ma', sh=3)
    elif t < 11.0:
        lt = t - 7.6; box(d, 80, 300, 1000, 1150, border=C['gold'])
        text(d, (540, 350), 'THE LOOT', pix(96), C['gold'], 'ma')
        rows = [('Every day', '+20 XP', '+10 coins'), ('Every checkpoint', '+100 XP', '+50 coins'), ('Beat the boss', '+1,000 XP', '+500 coins')]
        for i, (a, xp, co) in enumerate(rows):
            p = ease(appear(lt, 0.3 + i * 0.8))
            if p <= 0: continue
            y = 520 + i * 190 + int((1 - p) * 40)
            text(d, (140, y), a, bodyb(48), C['cream'], sh=3)
            pill(d, 140, y + 70, xp, num(44), bg=C['teal']); pill(d, 560, y + 70, co, num(44), bg=C['gold'])
        tk.coins_burst(img, t, 7.6 + 0.3 + 1.6, 540, 1000, n=10)
    elif t < 14.0:
        lt = t - 11.0; box(d, 80, 260, 1000, 1240, border=C['red'])
        text(d, (540, 300), 'DAY 30', tag(44), C['lilac'], 'ma', sh=3)
        text(d, (540, 350), 'THE COUCH TITAN', pix(84), C['red'], 'ma')
        hits = sum(1 for h in (0.6, 1.2, 1.8) if lt > h); dead = lt > 2.6
        bar(d, 160, 480, 760, 44, (3 - hits) / 3, col=C['red'])
        text(d, (540, 545), f'HITS {hits}/3', num(40), C['cream'], 'ma', sh=3)
        s = 16; cw, ch = tk.sprite_size('couch', s)
        if lt < 2.3 or (lt < 2.6 and int(lt * 20) % 2):
            sprite(img, 'couch', 540 - cw // 2, 640, s, outline=C['ink'] if not hits or int(lt * 20) % 2 else C['cream'])
        if dead:
            p = back(appear(lt, 2.6, 0.25))
            text(d, (540, 700), 'DEFEATED', pix(int(130 * max(.3, p))), C['gold'], 'ma', sh=8)
        text(d, (540, 940), 'Cover 5 km, any mix', bodyb(48), C['cream'], 'ma', sh=3)
        text(d, (540, 1000), 'of running and walking', bodyb(48), C['cream'], 'ma', sh=3)
        text(d, (540, 1110), 'First 3 days free. Not medical advice.', body(36), C['dim'], 'ma', sh=0)
        for h in (11.6, 12.2, 12.8): img = tk.shake(img, t, h)
    else:
        tk.end_card_live(img, t, 14.0)
    return img
COUCH = dict(total=17.0, frame=couch_frame, seed=7, music=dict(bpm=132, root=52, prog=(0, -4, -2, -5)),
             events=[(1.0, 'blip'), (2.8, 'whoosh')] + [(2.8 + 0.3 + i * 1.0, 'tick') for i in range(4)] + [(7.6, 'whoosh')]
                    + [(7.6 + 0.3 + i * 0.8, 'coin') for i in range(3)] + [(11.0, 'whoosh'), (11.6, 'hit'), (12.2, 'hit'), (12.8, 'hit'), (13.6, 'level'), (14.0, 'whoosh')],
             checks=[0.0, 1.5, 5.5, 7.3, 10.4, 12.0, 13.8, 16.0])

VIDEOS = {'rank-diamond': RANK, 'lagos-traffic': TRAFFIC, 'couch-titan': COUCH}

def render(slug):
    v = VIDEOS[slug]; wav = f'/tmp/v4-{slug}.wav'
    tk.soundtrack(v['total'], v['events'], wav, seed=v['seed'], **v['music'])
    out = os.path.join(OUT, f'v4-{slug}.mp4'); tk.encode(v['frame'], v['total'], wav, out)
    # thumbnail = first frame (hook)
    v['frame'](0.4).save(os.path.join(OUT, f'v4-{slug}-thumb.png'))
    print(out)

def frames(slug):
    v = VIDEOS[slug]; os.makedirs(os.path.join(HERE, 'check', 'v4'), exist_ok=True)
    for t in v['checks']: v['frame'](t).save(os.path.join(HERE, 'check', 'v4', f'{slug}_{t:04.1f}.png'))

if __name__ == '__main__':
    slugs = list(VIDEOS) if sys.argv[1] == 'all' else [sys.argv[1]]
    for s in slugs: (frames if len(sys.argv) > 2 and sys.argv[2] == 'frames' else render)(s)
