# -*- coding: utf-8 -*-
"""Qonun sharhi multfilm videosi: render.py <modda> <tts_out_dir> <chiqish.mp4> [--preview N]"""
import glob, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(__file__))
import spec

W, H, FPS, S = 1080, 1920, 30, 2
FONT = os.path.join(os.path.dirname(__file__), "Baloo2.ttf")
OUT = (58, 36, 26)          # kontur
CREAM = (253, 247, 235)
RED = (171, 52, 36)
GREEN = (44, 104, 68)
BROWN = (75, 44, 30)
SKIN = (243, 196, 150)
PINK = (240, 150, 130)


def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, int(size))
    f.set_variation_by_name(weight)
    return f


def sc(*v):
    return [int(round(x * S)) for x in v]


class D:
    """1080×1920 koordinatalarda chizadi, ichkarida S marta katta."""

    def __init__(self, img):
        self.img, self.d = img, ImageDraw.Draw(img)

    def ell(self, cx, cy, rx, ry, fill, outline=OUT, w=5):
        self.d.ellipse(sc(cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline, width=int(w * S) if outline else 0)

    def rect(self, x0, y0, x1, y1, fill, outline=OUT, w=5, r=0):
        self.d.rounded_rectangle(sc(x0, y0, x1, y1), radius=int(r * S), fill=fill, outline=outline, width=int(w * S) if outline else 0)

    def poly(self, pts, fill, outline=OUT, w=5):
        p = [(int(x * S), int(y * S)) for x, y in pts]
        self.d.polygon(p, fill=fill)
        if outline:
            self.d.line(p + [p[0]], fill=outline, width=int(w * S), joint="curve")

    def line(self, pts, fill=OUT, w=5):
        self.d.line([(int(x * S), int(y * S)) for x, y in pts], fill=fill, width=int(w * S), joint="curve")

    def arc(self, cx, cy, rx, ry, a0, a1, fill=OUT, w=5):
        self.d.arc(sc(cx - rx, cy - ry, cx + rx, cy + ry), a0, a1, fill=fill, width=int(w * S))

    def chord(self, cx, cy, rx, ry, a0, a1, fill, outline=OUT, w=5):
        self.d.chord(sc(cx - rx, cy - ry, cx + rx, cy + ry), a0, a1, fill=fill, outline=outline, width=int(w * S) if outline else 0)


def background():
    img = Image.new("RGB", (W * S, H * S))
    top, mid = np.array([252, 238, 214]), np.array([246, 226, 198])
    ys = np.linspace(0, 1, H * S)[:, None]
    grad = (top * (1 - ys) + mid * ys).astype(np.uint8)
    img = Image.fromarray(np.repeat(grad[:, None, :], W * S, axis=1))
    d = D(img)
    d.rect(0, 1185, W, 1600, (243, 222, 194), outline=None)
    d.line([(0, 1185), (W, 1185)], fill=(214, 172, 124), w=5)
    # rasm
    d.rect(55, 1020, 295, 1200, (253, 232, 178), w=5, r=8)
    d.poly([(75, 1180), (150, 1082), (225, 1180)], (90, 150, 96), outline=None)
    d.ell(253, 1056, 16, 16, (232, 160, 60), w=4)
    # deraza
    d.rect(712, 1020, 1040, 1330, (190, 220, 240), w=5)
    d.rect(866, 1020, 882, 1330, (250, 250, 250), outline=None)
    d.rect(712, 1160, 1040, 1174, (250, 250, 250), outline=None)
    d.rect(693, 1020, 768, 1345, (205, 108, 70), outline=None)
    d.rect(982, 1020, 1058, 1345, (205, 108, 70), outline=None)
    # gul
    for (lx, ly, rx, ry) in [(55, 1310, 38, 22), (125, 1290, 34, 20), (10, 1368, 30, 20), (175, 1330, 30, 18)]:
        d.line([(132, 1450), (lx, ly)], fill=(60, 110, 70), w=5)
        d.ell(lx, ly, rx, ry, (62, 122, 80), w=4)
    d.poly([(84, 1445), (182, 1445), (170, 1530), (96, 1530)], (205, 108, 70), w=4)
    return img


def desk(d):
    d.rect(-10, 1568, W + 10, 1606, (219, 164, 108), w=5)
    d.rect(-10, 1603, W + 10, H + 10, (186, 132, 82), outline=None)
    d.line([(0, 1604), (W, 1604)], w=5)
    # krujka
    d.arc(128, 1540, 20, 18, -90, 90, w=6)
    d.rect(57, 1508, 124, 1578, (252, 250, 244), w=5, r=8)
    # kitoblar
    d.rect(906, 1548, 1036, 1578, (171, 52, 36), w=5, r=4)
    d.rect(916, 1518, 1026, 1548, (44, 104, 68), w=5, r=4)


def mic(d, x):
    d.line([(x, 1520), (x, 1560)], w=10)
    d.ell(x, 1568, 58, 14, (52, 50, 56), w=4)
    d.rect(x - 26, 1445, x + 26, 1535, (86, 84, 92), w=5, r=24)
    for y in (1468, 1488, 1508):
        d.line([(x - 20, y), (x + 20, y)], fill=(52, 50, 56), w=4)


def eye(d, cx, cy, closed, lashes=False, side=1):
    if closed:
        d.arc(cx, cy - 6, 24, 16, 20, 160, w=6)
        return
    d.ell(cx, cy, 24, 25, (255, 255, 255), w=5)
    d.ell(cx, cy + 2, 12, 13, (60, 38, 30), outline=None)
    d.ell(cx - 4, cy - 3, 4, 4, (255, 255, 255), outline=None)
    if lashes:
        d.line([(cx + side * 21, cy - 12), (cx + side * 33, cy - 18)], w=5)


def mouth(d, cx, cy, level):
    if level == 0:
        d.arc(cx, cy - 14, 32, 22, 25, 155, w=6)
    elif level == 1:
        d.ell(cx, cy, 17, 11, (150, 40, 40), w=5)
    else:
        d.ell(cx, cy + 3, 21, 20, (150, 40, 40), w=5)
        d.chord(cx, cy + 8, 13, 12, 0, 180, (232, 120, 120), outline=None)


def boy(d, blink, m):
    hx, hy = 285, 1275
    d.ell(285, 1585, 205, 105, (47, 107, 79), w=5)          # kurtka
    d.poly([(235, 1485), (335, 1485), (285, 1570)], (252, 250, 244), w=5)
    d.poly([(274, 1500), (296, 1500), (302, 1570), (268, 1570)], (171, 52, 36), w=4)
    d.rect(252, 1385, 318, 1490, SKIN, w=5)                  # bo‘yin
    d.ell(hx - 122, hy + 12, 18, 28, SKIN, w=5)
    d.ell(hx + 122, hy + 12, 18, 28, SKIN, w=5)
    d.ell(hx, hy, 122, 142, SKIN, w=5)
    # soch
    d.chord(hx, hy - 6, 131, 152, 197, 343, (40, 28, 24), w=5)
    d.arc(hx - 50, hy - 30, 30, 14, 200, 340, w=6)
    d.arc(hx + 50, hy - 30, 30, 14, 200, 340, w=6)
    eye(d, hx - 50, hy + 10, blink)
    eye(d, hx + 50, hy + 10, blink)
    d.ell(hx - 76, hy + 72, 26, 15, PINK, outline=None)
    d.ell(hx + 76, hy + 72, 26, 15, PINK, outline=None)
    mouth(d, hx, hy + 92, m)


def girl(d, blink, m, hand=0):
    hx, hy = 792, 1283
    hair = (74, 42, 28)
    d.ell(hx, 1100, 54, 50, hair, w=5)                        # tugun
    d.rect(hx - 146, hy - 150, hx + 146, hy + 210, hair, w=5, r=120)
    d.ell(792, 1590, 195, 105, (217, 104, 63), w=5)          # kiyim
    d.rect(762, 1395, 822, 1490, SKIN, w=5)
    d.ell(hx, hy, 118, 136, SKIN, w=5)
    d.chord(hx, hy - 20, 124, 132, 190, 350, hair, w=5)
    d.poly([(hx + 20, hy - 100), (hx + 122, hy - 45), (hx + 118, hy + 20), (hx + 60, hy - 50)], hair, outline=None)
    d.line([(hx + 118, hy + 20), (hx + 60, hy - 50), (hx + 20, hy - 95)], w=5)
    d.arc(hx - 50, hy - 36, 28, 12, 200, 340, w=6)
    d.arc(hx + 52, hy - 36, 28, 12, 200, 340, w=6)
    eye(d, hx - 50, hy + 2, blink, lashes=True, side=-1)
    eye(d, hx + 52, hy + 2, blink, lashes=True)
    d.ell(hx - 76, hy + 62, 26, 15, PINK, outline=None)
    d.ell(hx + 76, hy + 62, 26, 15, PINK, outline=None)
    mouth(d, hx, hy + 86, m)
    d.ell(880, 1440 - hand, 33, 34, SKIN, w=5)               # qo‘l
    d.line([(868, 1418 - hand), (878, 1408 - hand)], w=4)


def plates(bg):
    """(bola blink, qiz blink, qiz og‘iz, qo‘l) -> RGB kadr."""
    out = {}
    for bb in (0, 1):
        for gb in (0, 1):
            for gm in (0, 1, 2):
                for hand in (0, 1):
                    img = bg.copy()
                    d = D(img)
                    boy(d, bb, 0)
                    girl(d, gb, gm, hand * 14)
                    desk(d)
                    mic(d, 438)
                    mic(d, 650)
                    out[(bb, gb, gm, hand)] = img.resize((W, H), Image.LANCZOS)
    return out


def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def title_layer(n, title):
    img = Image.new("RGBA", (W * S, 380 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def outlined(text, y, size, fill):
        f = font(size * S, "ExtraBold")
        while d.textlength(text, font=f) > (W - 110) * S:
            size -= 4
            f = font(size * S, "ExtraBold")
        x = W * S / 2
        d.text((x + 5 * S, y * S + 6 * S), text, font=f, anchor="mm", fill=OUT + (70,), stroke_width=int(13 * S), stroke_fill=OUT + (70,))
        d.text((x, y * S), text, font=f, anchor="mm", fill=OUT, stroke_width=int(13 * S), stroke_fill=OUT)
        d.text((x, y * S), text, font=f, anchor="mm", fill=CREAM, stroke_width=int(8 * S), stroke_fill=CREAM)
        d.text((x, y * S), text, font=f, anchor="mm", fill=fill)

    outlined(f"JK {n}", 150, 150, RED)
    outlined(title, 292, 96, GREEN)
    return img.resize((W, 380), Image.LANCZOS)


CARD = (48, 380, 1008, 1016)


def card_layer(pill, main, green):
    x0, y0, x1, y1 = CARD
    pad = 40
    img = Image.new("RGBA", ((x1 - x0 + pad * 2) * S, (y1 - y0 + pad * 2) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cw, ch = (x1 - x0) * S, (y1 - y0) * S
    o = pad * S
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([o + 22 * S, o + 22 * S, o + cw + 22 * S, o + ch + 22 * S], radius=34 * S, fill=(120, 70, 40, 75))
    img.alpha_composite(sh)
    d.rounded_rectangle([o, o, o + cw, o + ch], radius=34 * S, fill=CREAM, outline=OUT, width=5 * S)
    # pill
    pf = font(58 * S, "ExtraBold")
    pw = d.textlength(pill, font=pf) + 80 * S
    px, py = o + cw / 2, o + 82 * S
    d.rounded_rectangle([px - pw / 2, py - 46 * S, px + pw / 2, py + 46 * S], radius=46 * S, fill=RED, outline=OUT, width=5 * S)
    d.text((px, py + 3 * S), pill, font=pf, anchor="mm", fill=(255, 250, 240))
    # matn
    size = 54
    while True:
        f = font(size * S, "Bold")
        lh = int(size * 1.28 * S)
        rows = [(l, BROWN) for l in wrap(d, main, f, cw - 90 * S)]
        for g in green:
            rows += [(l, GREEN) for l in wrap(d, g, f, cw - 90 * S)]
        if len(rows) * lh <= ch - 190 * S or size <= 36:
            break
        size -= 3
    area0, area1 = o + 140 * S, o + ch - 30 * S
    y = (area0 + area1) / 2 - len(rows) * lh / 2 + lh / 2
    for text, col in rows:
        d.text((o + cw / 2, y), text, font=f, anchor="mm", fill=col)
        y += lh
    return img.resize(((x1 - x0 + pad * 2), (y1 - y0 + pad * 2)), Image.LANCZOS), (x0 - pad, y0 - pad)


SUB = (24, 1742, 1056, 1890)


def sub_layer(lines):
    x0, y0, x1, y1 = SUB
    img = Image.new("RGBA", ((x1 - x0) * S, (y1 - y0) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=26 * S, fill=(75, 46, 32, 255))
    f = font(42 * S, "Bold")
    lh = 54 * S
    y = img.height / 2 - (len(lines) - 1) * lh / 2 + 2 * S
    for l in lines:
        d.text((img.width / 2, y), l, font=f, anchor="mm", fill=(255, 250, 240))
        y += lh
    return img.resize((x1 - x0, y1 - y0), Image.LANCZOS)


def sub_chunks(text):
    """Matnni 2 qatorli bo‘laklarga ajratadi: [(qatorlar, belgi soni)]."""
    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    f = font(42, "Bold")
    lines = wrap(d, text, f, SUB[2] - SUB[0] - 70)
    chunks = [lines[i:i + 2] for i in range(0, len(lines), 2)]
    if len(chunks) > 1 and len(chunks[-1]) == 1 and len(chunks[-1][0]) < 14:   # yolg‘iz qisqa qator
        last = chunks.pop()
        merged = " ".join(chunks.pop() + last)
        l3 = wrap(d, merged, f, SUB[2] - SUB[0] - 70)
        k = (len(l3) + 1) // 2
        chunks += [l3[:k], l3[k:]] if len(l3) > 2 else [l3]
    return [(c, sum(len(x) for x in c)) for c in chunks]


def dur(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))


def main():
    n, ttsdir, outpath = sys.argv[1], sys.argv[2], sys.argv[3]
    preview = int(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None
    art = next(a for a in spec.ARTICLES if a["key"] == n)
    segs = spec.segments(art)
    mp3 = sorted(glob.glob(os.path.join(ttsdir, "[0-9][0-9].mp3")))
    assert len(mp3) == len(segs), (len(mp3), len(segs))
    random.seed(n)

    # ovoz yo‘lagi
    LEAD, GAP, TAIL = 0.35, 0.40, 1.0
    work = outpath + ".tmp"
    os.makedirs(work, exist_ok=True)
    wav = os.path.join(work, "a.wav")
    durs = [dur(p) for p in mp3]
    starts, t = [], LEAD
    for dd in durs:
        starts.append(t)
        t += dd + GAP
    total = t - GAP + TAIL
    inputs, filt = [], []
    for i, p in enumerate(mp3):
        inputs += ["-i", p]
        filt.append(f"[{i}:a]aresample=48000,adelay={int(starts[i]*1000)}:all=1[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(mp3))) + f"amix=inputs={len(mp3)}:normalize=0,apad=whole_dur={total:.3f}[o]")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[o]", "-ac", "2", "-ar", "48000", wav])
    pcm = np.frombuffer(subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "12000", "-f", "s16le", "-"]), dtype=np.int16).astype(np.float32)
    nfr = int(total * FPS)
    hop = 12000 // FPS
    env = np.array([np.sqrt(np.mean(pcm[i * hop:(i + 1) * hop] ** 2) + 1) for i in range(nfr)])
    env = env / (np.percentile(env, 95) + 1e-6)

    # qatlamlar
    P = plates(background())
    title = title_layer(art["n"], art["title"])
    cards = [card_layer(s[1], s[2], s[3]) for s in segs]
    subs = []          # (boshlanish, tugash, rasm)
    for i, s in enumerate(segs):
        ch = sub_chunks(s[0].replace("ʻ", "‘"))
        tot = sum(c[1] for c in ch)
        t0 = starts[i]
        for lines, cnt in ch:
            t1 = t0 + durs[i] * cnt / tot
            subs.append((t0, t1, sub_layer(lines)))
            t0 = t1
        subs[-1] = (subs[-1][0], subs[-1][1] + GAP * 0.6, subs[-1][2])

    # ko‘z pirpiratish jadvali
    def blinks():
        b, t = set(), random.uniform(1, 3)
        while t < total:
            f0 = int(t * FPS)
            b.update(range(f0, f0 + 4))
            t += random.uniform(2.2, 4.5)
        return b
    bb, gb = blinks(), blinks()

    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
           "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "18", "-maxrate", "10M", "-bufsize", "20M", "-pix_fmt", "yuv420p",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-shortest", outpath]
    enc = None if preview is not None else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(max(x, 0), 1))
    mlevel, mhold = 0, 0
    frames = [preview] if preview is not None else range(nfr)
    for fi in frames:
        t = fi / FPS
        si = max(i for i in range(len(segs)) if starts[i] - 0.2 <= t or i == 0)
        speaking = starts[si] <= t <= starts[si] + durs[si]
        e = env[fi] if speaking else 0
        want = 2 if e > 0.55 else 1 if e > 0.16 else 0
        if mhold <= 0 or preview is not None:
            mlevel, mhold = want, 2
        mhold -= 1
        hand = 1 if speaking and math.sin(t * 5.2) > 0.2 else 0
        fr = P[(int(fi in bb), int(fi in gb), mlevel, hand)].copy()
        fr.paste(title, (0, 0), title)
        # kartochka: yangi segmentda pastdan yumshoq chiqadi
        k = ease((t - (starts[si] - 0.2)) / 0.45) if si > 0 else 1.0
        cimg, (cx, cy) = cards[si]
        if k < 1 and si > 0:
            pimg, _ = cards[si - 1]
            fr.paste(pimg, (cx, cy), pimg)
            a = cimg.copy()
            a.putalpha(a.getchannel("A").point(lambda v: int(v * k)))
            fr.paste(a, (cx, cy), a)
        else:
            fr.paste(cimg, (cx, cy), cimg)
        for t0, t1, simg in subs:
            if t0 <= t < t1:
                fr.paste(simg, (SUB[0], SUB[1]), simg)
                break
        # yumshoq kamera zoom
        z = 1.0 + 0.022 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 14.0))
        if z > 1.0005:
            cw_, ch_ = W / z, H / z
            ox, oy = (W - cw_) / 2, (H - ch_) * 0.55
            fr = fr.resize((W, H), Image.BICUBIC, box=(ox, oy, ox + cw_, oy + ch_))
        if preview is not None:
            fr.save(outpath)
            return
        enc.stdin.write(fr.tobytes())
    enc.stdin.close()
    enc.wait()
    print("tayyor", outpath, f"{total:.1f}s")


if __name__ == "__main__":
    main()
