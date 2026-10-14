from PIL import Image, ImageDraw, ImageFont
import random, math

PAL = {
    'k': (24, 14, 30), 'h': (40, 38, 58), 'H': (70, 68, 100),
    's': (246, 198, 146), 'S': (204, 140, 92),
    'y': (240, 192, 36), 'Y': (184, 130, 26), 'p': (250, 228, 120),
    'r': (210, 44, 40), 'R': (196, 38, 38), 'X': (130, 22, 26),
    'b': (176, 104, 48), 'L': (222, 150, 80), 'B': (100, 56, 30),
    'w': (250, 250, 246),
    'z': (166, 196, 178), 'Z': (108, 136, 126), 'E': (64, 76, 88),
    'c': (128, 188, 226), 'C': (82, 132, 182), 'e': (176, 62, 44),
    'n': (44, 50, 100), 'N': (26, 28, 64),
    'm': (130, 30, 52), 'M': (80, 16, 34),
    'o': (232, 180, 48), 'O': (170, 118, 30),
    'W': (226, 234, 250), 'G': (156, 172, 210), 'g': (238, 244, 255),
    'q': (140, 168, 146), 'Q': (92, 120, 102),
    'v': (96, 44, 128), 'V': (60, 24, 86), 'f': (40, 140, 124), 'j': (90, 200, 130),
}
OUT = PAL['k']


class Spr:
    def __init__(s, w, h, oy=0):
        s.w, s.h, s.oy = w, h, oy
        s.g = [[None] * w for _ in range(h)]

    def px(s, x, y, c):
        y += s.oy
        if 0 <= x < s.w and 0 <= y < s.h:
            s.g[y][x] = c

    def rect(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.px(x, y, c)

    def clear(s, *pts):
        for x, y in pts:
            s.g[y + s.oy][x] = None

    def outline(s):
        add = []
        for y in range(s.h):
            for x in range(s.w):
                if s.g[y][x] is None:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < s.w and 0 <= yy < s.h and s.g[yy][xx] not in (None, 'k_'):
                            add.append((x, y)); break
        for x, y in add:
            s.g[y][x] = 'k'

    def img(s, alpha=255):
        im = Image.new('RGBA', (s.w, s.h), (0, 0, 0, 0))
        for y in range(s.h):
            for x in range(s.w):
                c = s.g[y][x]
                if c:
                    im.putpixel((x, y), PAL[c] + (alpha,))
        return im


def taoist():
    s = Spr(26, 37, oy=5)
    # tall square Taoist hat: flat top, white vertical pleat stripes, taiji below
    s.rect(8, -3, 17, 7, 'h')
    s.rect(7, -4, 18, -3, 'h'); s.rect(7, -4, 18, -4, 'H')
    s.rect(8, -2, 9, 7, 'k')
    for x in (10, 12, 14, 16):
        s.rect(x, -3, x, 1, 'w')
    s.rect(10, 1, 17, 1, 'w')
    s.px(9, -3, 'H'); s.px(9, -1, 'H'); s.px(9, 1, 'H')
    s.rect(13, 3, 15, 4, 'w')  # white plaque (帽正)
    # head
    s.rect(7, 7, 17, 17, 's'); s.clear((7, 17), (17, 17), (7, 16))
    s.rect(7, 7, 9, 11, 'h')
    s.rect(7, 12, 8, 15, 'S')
    s.px(18, 13, 's')  # nose
    s.px(9, 12, 'S'); s.px(10, 12, 'S'); s.px(10, 13, 'S')  # ear
    # brows (separate), eyes, mouth, goatee
    s.rect(12, 9, 14, 9, 'k'); s.rect(16, 9, 17, 9, 'k')
    s.rect(13, 11, 13, 12, 'k'); s.rect(16, 11, 16, 12, 'k')
    s.rect(14, 14, 17, 14, 'h')
    s.rect(15, 16, 16, 16, 'k')
    s.px(15, 17, 'h'); s.px(16, 17, 'h'); s.px(15, 18, 'h')
    # robe
    s.rect(8, 18, 17, 27, 'y'); s.rect(7, 24, 18, 27, 'y')
    s.rect(8, 18, 9, 27, 'Y'); s.rect(7, 24, 7, 27, 'Y')
    s.rect(11, 18, 16, 18, 'w'); s.px(13, 19, 'w'); s.px(14, 19, 'w')
    s.px(15, 18, 'h'); s.px(15, 19, 'h')
    s.rect(8, 22, 17, 22, 'r'); s.rect(15, 23, 15, 25, 'r')
    s.rect(11, 20, 12, 20, 'k'); s.px(12, 21, 'w')  # tiny taiji hint
    # back arm with talisman
    s.rect(6, 19, 7, 23, 'Y'); s.rect(6, 24, 7, 24, 'S')
    s.rect(3, 21, 5, 27, 'p'); s.px(4, 22, 'r'); s.px(4, 24, 'r'); s.px(4, 25, 'r'); s.px(4, 26, 'r')
    # front arm raising peach-wood sword
    s.rect(16, 19, 19, 21, 'y'); s.rect(18, 16, 20, 19, 'y'); s.rect(18, 19, 19, 21, 'Y')
    s.rect(19, 14, 21, 16, 's')
    s.rect(20, 3, 21, 12, 'b'); s.rect(21, 4, 21, 12, 'L'); s.px(20, 2, 'b')
    s.rect(19, 13, 22, 13, 'B')
    s.px(22, 15, 'r'); s.px(22, 16, 'r'); s.px(23, 17, 'r')
    # shoes
    s.rect(8, 28, 11, 29, 'h'); s.rect(14, 28, 17, 29, 'h')
    s.rect(9, 28, 10, 28, 'w'); s.rect(15, 28, 16, 28, 'w')
    s.outline()
    return s


def zombie(robe='n', shade='N', talisman=True, jump=False):
    off = 1 if jump else 0
    H = 39 if jump else 34
    s = Spr(28, H, oy=off)
    R, P = s.rect, s.px
    # winter official hat: red tassel crown, gold button, thick black upturned brim
    R(11, 1, 13, 2, 'o')
    R(9, 3, 15, 5, 'R'); s.clear((9, 3), (15, 3))
    for x in (10, 12, 14): R(x, 4, x, 5, 'X')
    R(7, 6, 17, 8, 'h'); R(6, 7, 18, 8, 'h'); R(7, 6, 17, 6, 'H')
    # face (blue-grey), dark eye socket, fangs
    R(8, 9, 17, 17, 'z'); s.clear((8, 17), (17, 17))
    R(8, 9, 9, 16, 'Z'); P(18, 13, 'z')
    R(15, 11, 17, 12, 'E'); P(16, 12, 'k')
    R(14, 16, 17, 16, 'k'); P(15, 17, 'w'); P(17, 17, 'w')
    for x, y in [(7, 12), (7, 13), (6, 14), (6, 15), (6, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21)]:
        P(x, y, 'h')
    if talisman:  # yellow charm hanging from the brim over the face
        R(12, 9, 14, 15, 'p'); P(15, 9, 'p')
        P(13, 10, 'r'); P(13, 11, 'r'); P(12, 13, 'r'); P(13, 13, 'r'); P(13, 14, 'r')
    # robe: long, dark, light-blue collar
    R(8, 18, 17, 29, robe); R(7, 25, 18, 29, robe)
    if jump: R(6, 26, 19, 29, robe); R(6, 26, 6, 29, shade)
    R(8, 18, 9, 29, shade); R(7, 25, 7, 29, shade)
    R(9, 18, 16, 18, 'c'); P(9, 18, 'C')
    # mandarin square + court beads
    R(11, 21, 15, 25, 'O'); R(12, 22, 14, 24, 'f'); P(13, 23, 'w'); P(12, 22, 'w')
    for y in range(19, 27, 2): P(10, y, 'e'); P(16, y, 'e')
    for x in (11, 13, 15): P(x, 27, 'e')
    P(13, 28, 'o')
    # arms straight forward, light-blue horse-hoof cuffs, drooping hands, long nails
    R(15, 19, 21, 22, robe); R(15, 22, 21, 22, shade)
    R(22, 19, 23, 22, 'c'); R(22, 22, 23, 22, 'C')
    R(24, 20, 25, 23, 'z'); R(24, 23, 25, 23, 'Z')
    P(24, 24, 'k'); P(25, 24, 'k'); P(25, 25, 'k')
    # black boots, thick white soles
    R(9, 30, 16, 30, 'h'); R(9, 31, 16, 31, 'w')
    s.outline()
    return s


def ghost():
    s = Spr(24, 33)
    s.rect(7, 4, 16, 22, 'h'); s.clear((7, 4), (16, 4), (7, 5))
    s.rect(9, 3, 14, 3, 'h'); s.rect(9, 4, 13, 4, 'H')
    s.rect(11, 8, 16, 16, 'g'); s.rect(11, 8, 12, 15, 'G')
    s.px(17, 12, 'g')
    s.rect(14, 11, 15, 11, 'R'); s.px(15, 11, 'w')
    s.rect(14, 14, 15, 14, 'G')
    s.rect(11, 8, 13, 9, 'h')  # hair fringe across face
    s.rect(8, 17, 17, 24, 'W'); s.rect(8, 17, 10, 24, 'G')
    s.rect(9, 25, 16, 27, 'W'); s.rect(9, 25, 10, 27, 'G')
    s.rect(11, 28, 15, 29, 'W'); s.rect(13, 30, 15, 30, 'W'); s.px(16, 31, 'W')
    s.rect(7, 16, 9, 26, 'h'); s.rect(16, 16, 16, 20, 'h')
    s.rect(17, 17, 19, 21, 'W'); s.rect(17, 21, 19, 21, 'G')
    s.rect(19, 22, 19, 24, 'g'); s.px(18, 23, 'g')
    s.outline()
    return s


def king():
    s = Spr(38, 44)
    # peacock feather
    for x, y in [(11, 5), (10, 5), (9, 6), (8, 6), (7, 7), (6, 7), (5, 8), (4, 8), (3, 9), (2, 9)]:
        s.px(x, y, 'f'); s.px(x, y + 1, 'f')
    s.px(4, 8, 'o'); s.px(4, 9, 'j')
    s.rect(16, 1, 18, 2, 'o')
    s.rect(12, 3, 23, 6, 'R'); s.clear((12, 3), (23, 3))
    for x in (13, 15, 17, 19, 21): s.rect(x, 4, x, 6, 'X')
    s.rect(10, 7, 25, 9, 'h'); s.rect(9, 8, 26, 9, 'h'); s.rect(10, 7, 25, 7, 'H')
    # white hair
    s.rect(9, 10, 13, 27, 'W'); s.rect(9, 18, 10, 27, 'G')
    # face
    s.rect(12, 10, 25, 22, 'q'); s.clear((25, 22), (12, 22))
    s.rect(12, 10, 14, 21, 'Q'); s.px(26, 16, 'q'); s.px(26, 17, 'q')
    s.px(16, 12, 'k'); s.px(17, 12, 'k'); s.px(18, 13, 'k')
    s.px(21, 13, 'k'); s.px(22, 12, 'k'); s.px(23, 12, 'k')
    s.rect(17, 14, 18, 15, 'R'); s.rect(22, 14, 23, 15, 'R')
    s.px(18, 14, 'p'); s.px(23, 14, 'p')
    s.rect(19, 18, 24, 20, 'k')
    s.px(20, 18, 'w'); s.px(20, 19, 'w'); s.px(23, 18, 'w'); s.px(23, 19, 'w')
    # beard
    s.rect(17, 21, 23, 25, 'W'); s.rect(18, 26, 22, 26, 'W'); s.rect(19, 27, 21, 28, 'W'); s.rect(17, 21, 18, 25, 'G')
    # robe
    s.rect(10, 23, 26, 38, 'v'); s.rect(9, 33, 27, 38, 'v')
    s.rect(10, 23, 12, 38, 'V'); s.rect(9, 33, 9, 38, 'V')
    s.rect(9, 38, 27, 38, 'o')
    s.rect(14, 30, 22, 34, 'o'); s.clear((14, 30), (22, 30), (14, 34), (22, 34))
    s.rect(16, 31, 20, 33, 'R'); s.px(18, 32, 'o')
    s.rect(10, 35, 26, 35, 'O'); s.px(15, 35, 'j'); s.px(21, 35, 'j')
    s.rect(14, 23, 16, 23, 'c')
    for y in range(26, 36, 2): s.px(13, y, 'e'); s.px(23, y, 'e')
    for x in (15, 17, 19, 21): s.px(x, 36, 'e')
    s.px(18, 37, 'o')
    # arms + long nails
    s.rect(21, 23, 31, 27, 'v'); s.rect(21, 27, 31, 27, 'V'); s.rect(30, 23, 31, 27, 'c'); s.rect(30, 27, 31, 27, 'C')
    s.rect(32, 24, 34, 29, 'q'); s.rect(32, 29, 34, 29, 'Q')
    s.px(32, 30, 'k'); s.px(33, 30, 'k'); s.px(34, 30, 'k'); s.px(33, 31, 'k'); s.px(34, 31, 'k'); s.px(34, 32, 'k')
    # boots
    s.rect(12, 39, 24, 40, 'h'); s.rect(12, 41, 24, 41, 'w')
    s.outline()
    return s


SPRITES = [
    ('道士', '主角 · 桃木剑 + 黄符', taoist()),
    ('僵尸', '普通 · 慢，数量多', zombie()),
    ('跳尸', '红衣 · 会大跳扑人', zombie('m', 'M', jump=True)),
    ('游魂', '快 · 血少 · 穿墙', ghost()),
    ('尸王', 'Boss · 最后一分钟', king()),
]

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def sheet():
    sc = 8
    cellw, cellh = 38 * sc + 40, 44 * sc + 40
    W = cellw * len(SPRITES) + 40
    Hh = cellh + 150
    im = Image.new('RGB', (W, Hh), (30, 22, 48))
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FONT, 44, index=2)
    f2 = ImageFont.truetype(FONT, 24, index=2)
    for i, (name, desc, sp) in enumerate(SPRITES):
        x0 = 20 + i * cellw
        d.rectangle([x0 + 8, 20, x0 + cellw - 8, 20 + cellh], fill=(42, 32, 66))
        spr = sp.img().resize((sp.w * sc, sp.h * sc), Image.NEAREST)
        sx = x0 + (cellw - spr.width) // 2
        sy = 20 + cellh - 20 - spr.height
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([sx + spr.width * 0.2, 20 + cellh - 34, sx + spr.width * 0.8, 20 + cellh - 10], fill=(10, 6, 20, 140))
        im.paste(sh, (0, 0), sh)
        im.paste(spr, (sx, sy), spr)
        d.text((x0 + cellw // 2, 20 + cellh + 40), name, font=f1, fill=(244, 214, 110), anchor='mm')
        d.text((x0 + cellw // 2, 20 + cellh + 95), desc, font=f2, fill=(200, 190, 225), anchor='mm')
    im.save('characters.png')


def scene():
    random.seed(7)
    W, H = 512, 320
    im = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    # sky
    for y in range(52):
        t = y / 52
        d.line([(0, y), (W, y)], fill=(int(16 + 30 * t), int(10 + 14 * t), int(40 + 30 * t)))
    for _ in range(90):
        x, y = random.randrange(W), random.randrange(40)
        im.putpixel((x, y), (200, 190, 240, 255))
    # moon
    mx = W - 80
    d.ellipse([mx, 3, mx + 28, 31], fill=(90, 70, 70))
    d.ellipse([mx + 2, 5, mx + 26, 29], fill=(246, 212, 96))
    d.ellipse([mx + 13, 10, mx + 18, 15], fill=(226, 190, 80)); d.ellipse([mx + 6, 19, mx + 10, 23], fill=(226, 190, 80))
    # mountains
    pts = [(0, 52)]
    for x in range(0, W + 1, 4):
        pts.append((x, int(36 + 8 * math.sin(x / 23) + 5 * math.sin(x / 9))))
    pts.append((W, 52)); d.polygon(pts, fill=(38, 26, 64))
    # crumbled wall
    d.rectangle([0, 46, W, 58], fill=(76, 64, 98))
    for y in (46, 52):
        for x in range(-((y // 6) % 2) * 6, W, 12):
            d.rectangle([x, y, x + 11, y + 5], outline=(44, 34, 62))
    d.rectangle([0, 45, W, 45], fill=(110, 98, 136))
    for gx in list(range(60, 68)) + list(range(180, 185)) + list(range(330, 340)) + list(range(452, 456)):
        d.line([(gx, 45), (gx, 50 + (gx % 3))], fill=(44, 34, 70))
    # ground
    d.rectangle([0, 59, W, H], fill=(58, 42, 80))
    for _ in range(4200):
        x, y = random.randrange(W), random.randrange(59, H)
        im.putpixel((x, y), random.choice([(70, 52, 96, 255), (46, 33, 64, 255), (64, 48, 88, 255)]))
    # grass tufts
    for _ in range(140):
        x, y = random.randrange(W), random.randrange(62, H)
        for dx, hh in ((0, 2), (1, 3), (2, 2)):
            d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 86, 84))
    # dead tree (left)
    tr = (26, 18, 36)
    def tree(ox, oy, m=1):
        d.ellipse([ox + 12, oy + 78, ox + 34, oy + 84], fill=(38, 26, 52))
        d.rectangle([ox + 20, oy + 40, ox + 24, oy + 80], fill=tr)
        for (a, b) in [((22, 50), (8, 36)), ((22, 46), (36, 30)), ((12, 40), (6, 30)), ((32, 34), (40, 26)), ((22, 60), (34, 54))]:
            if m < 0: a, b = (44 - a[0], a[1]), (44 - b[0], b[1])
            d.line([(ox + a[0], oy + a[1]), (ox + b[0], oy + b[1])], fill=tr, width=2)
    tree(20, 0); tree(W - 70, 4, -1); tree(14, 200); tree(W - 60, 196, -1)

    def grave(x, y, tilt=0, charm=False, broken=False):
        d.ellipse([x - 16, y - 8, x + 16, y + 9], fill=(24, 14, 30))
        d.ellipse([x - 15, y - 7, x + 15, y + 8], fill=(98, 72, 92))
        d.ellipse([x - 12, y - 6, x + 8, y + 2], fill=(118, 92, 112))
        sx, sy = x - 5 + tilt, y - 4
        hgt = 9 if broken else 14
        d.rectangle([sx - 1, sy - hgt - 1, sx + 11, sy + 1], fill=(24, 14, 30))
        d.rectangle([sx, sy - hgt, sx + 10, sy], fill=(146, 140, 166))
        d.rectangle([sx + 8, sy - hgt, sx + 10, sy], fill=(110, 104, 132))
        if not broken:
            d.rectangle([sx + 1, sy - hgt - 2, sx + 9, sy - hgt - 1], fill=(146, 140, 166))
            d.line([(sx + 1, sy - hgt - 3), (sx + 9, sy - hgt - 3)], fill=(24, 14, 30))
        else:
            d.line([(sx, sy - hgt), (sx + 4, sy - hgt + 2), (sx + 10, sy - hgt - 1)], fill=(24, 14, 30))
        for yy in range(sy - hgt + 3, sy - 1, 2):
            d.line([(sx + 4, yy), (sx + 6, yy)], fill=(60, 54, 80))
        if charm:
            d.rectangle([sx + 2, sy - hgt + 1, sx + 6, sy - hgt + 9], fill=(250, 228, 120))
            d.line([(sx + 4, sy - hgt + 2), (sx + 4, sy - hgt + 8)], fill=(210, 44, 40))

    spots = []
    tries = 0
    while len(spots) < 20 and tries < 5000:
        tries += 1
        x, y = random.randrange(40, W - 40), random.randrange(80, H - 14)
        if (x - 256) ** 2 / 1.6 + (y - 200) ** 2 < 70 ** 2: continue
        if any((x - a) ** 2 + (y - b) ** 2 < 46 ** 2 for a, b in spots): continue
        spots.append((x, y))
    for x, y in sorted(spots, key=lambda p: p[1]):
        r = random.random()
        grave(x, y, 0, r < 0.25, 0.25 <= r < 0.45)
    # white funeral lantern on a pole
    for lx in (160, 380):
        d.line([(lx, 60), (lx, 84)], fill=(26, 18, 36), width=2)
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for r in range(18, 4, -2): gd.ellipse([lx - r, 65 - r, lx + r, 65 + r], fill=(255, 236, 190, 10))
        im.alpha_composite(glow)
        d.rectangle([lx - 5, 60, lx + 5, 70], fill=(24, 14, 30)); d.rectangle([lx - 4, 61, lx + 4, 69], fill=(236, 236, 226))
        d.line([(lx - 4, 65), (lx + 4, 65)], fill=(200, 200, 190)); d.line([(lx - 2, 62), (lx - 2, 68)], fill=(60, 50, 60))
    # paper money
    for _ in range(80):
        x, y = random.randrange(10, W - 10), random.randrange(64, H - 4)
        c = random.choice([(238, 232, 210), (232, 200, 90)])
        d.rectangle([x, y, x + 2, y + 2], fill=c); im.putpixel((x + 1, y + 1), (58, 42, 80, 255))
    # fog
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
    for i in range(18):
        x, y = random.randrange(-60, W), random.randrange(80, H)
        fd.ellipse([x, y, x + 150, y + 16], fill=(170, 160, 210, 34))
    im.alpha_composite(fog)

    def place(sp, cx, by, flip=False, alpha=255, glowc=None):
        s = sp.img(alpha)
        if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([cx - 9, by - 2, cx + 9, by + 2], fill=(14, 8, 24, 130))
        im.alpha_composite(sh)
        if glowc:
            g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(g).ellipse([cx - 16, by - s.height - 4, cx + 16, by], fill=glowc)
            im.alpha_composite(g)
        im.alpha_composite(s, (cx - s.width // 2, by - s.height))

    T, Z, J, G, K = [x[2] for x in SPRITES]
    actors = [
        (Z, 330, 196, True), (Z, 356, 168, True), (Z, 150, 178, False), (Z, 176, 246, False),
        (Z, 98, 120, False), (Z, 300, 120, True), (Z, 330, 270, True), (Z, 70, 266, False),
        (J, 196, 140, False), (J, 410, 242, True),
        (K, 446, 160, True),
    ]
    for sp, x, y, fl in sorted(actors + [(T, 256, 204, False)], key=lambda a: a[2]):
        place(sp, x, y, flip=fl)
    place(G, 226, 108, alpha=215, glowc=(120, 200, 230, 40))
    place(G, 420, 300, flip=True, alpha=215, glowc=(120, 200, 230, 40))
    # flying talismans
    for tx, ty in ((276, 182), (296, 178)):
        d.rectangle([tx, ty, tx + 4, ty + 7], fill=(24, 14, 30)); d.rectangle([tx + 1, ty + 1, tx + 3, ty + 6], fill=(250, 228, 120))
        im.putpixel((tx + 2, ty + 3), (210, 44, 40, 255))
    # vignette
    v = Image.new('RGBA', (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(v)
    for i in range(14):
        vd.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(8, 4, 16, 90 - i * 6))
    im.alpha_composite(v)
    im.convert('RGB').resize((W * 3, H * 3), Image.NEAREST).save('graveyard.png')


sheet()
scene()
