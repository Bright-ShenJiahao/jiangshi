"""World for 暂时停止呼吸: flat background + standalone objects (trees, houses, church) + collision grid."""
import random, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
CELL = 8
TOWN_H = 520   # 任家镇：地图上方新加的一块
K = (24, 14, 30)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(sz): return ImageFont.truetype(FONT, sz, index=2)


def river_x(y): return 215 + 38 * math.sin(y / 170) + 14 * math.sin(y / 53)


RIVER_W = 64
LOOP = (330, 540)          # 龙吐珠：河在这一段分成两股，围住一个圆土丘（旧坐标 y）
EXT = 320                  # 地图往左扩出的宽度
TOMB = (210, 650)          # 老太爷的坟：蜻蜓点水穴（最终坐标，在西边高山上）
def loop_off(y):
    if not (LOOP[0] < y < LOOP[1]): return 0.0
    return 74 * math.sin(math.pi * (y - LOOP[0]) / (LOOP[1] - LOOP[0]))
def channels(y):
    """[(center, width)] of water at this (old-coordinate) y"""
    cx, o = river_x(y), loop_off(y)
    if o < 18: return [(cx + o, RIVER_W)]
    w = max(34, RIVER_W - o * 0.6)
    return [(cx - 6, w), (cx + 2 * o, w)]
def in_water(x, y, pad=0):
    return any(abs(x - c) < w / 2 + pad for c, w in channels(y))
BRIDGE = (590, 646)
# 教堂周围的十字架坟墓
CROSSES = [(1300, 210), (1340, 260), (1296, 310), (1336, 360), (1300, 392), (1520, 214), (1562, 262), (1514, 304), (1560, 350), (1520, 388), (1376, 150), (1470, 150)]
WALL_Y = 104
WALL_X = (300, 1160)
PLAT_X, PLAT_Y = 1270, 400
STAIRS = (1400, 1448)
ROAD = [(0, 606), (150, 618), (300, 618), (520, 640), (760, 612), (1000, 566), (1250, 520), (1424, 500), (1424, 440), (1424, 346)]
ROAD_N = [(760, 612), (748, 400), (740, 104)]
CHURCH = (1424, 320)          # door-bottom anchor


def canvas(w, h):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


# ---------------- object sprites ----------------
def tree_img(burnt=False):
    im, d = canvas(30, 48); x, y = 15, 46
    d.ellipse([x - 11, y - 2, x + 11, y + 2], fill=(30, 20, 44))
    if burnt:
        d.rectangle([x - 3, y - 24, x + 3, y], fill=K); d.rectangle([x - 2, y - 23, x + 2, y], fill=(30, 24, 28))
        for a, b in [((0, -20), (-10, -34)), ((0, -22), (9, -38)), ((-5, -28), (-12, -30)), ((0, -14), (8, -20)), ((0, -24), (0, -42))]:
            d.line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], fill=K, width=3)
            d.line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], fill=(36, 30, 34), width=1)
        for (ox, oy) in [(-9, -33), (8, -36), (3, -18), (-2, -40)]: im.putpixel((x + ox, y + oy), (255, 140, 40, 255))
        return im
    d.rectangle([x - 3, y - 12, x + 3, y], fill=K); d.rectangle([x - 2, y - 12, x + 2, y], fill=(70, 46, 40))
    for (ox, oy, r) in [(0, -24, 13), (-7, -18, 9), (7, -18, 9), (0, -32, 8)]:
        d.ellipse([x + ox - r - 1, y + oy - r - 1, x + ox + r + 1, y + oy + r + 1], fill=K)
    for (ox, oy, r, c) in [(0, -24, 13, (32, 58, 62)), (-7, -18, 9, (22, 40, 46)), (7, -18, 9, (32, 58, 62)), (0, -32, 8, (46, 80, 80)), (-3, -28, 4, (46, 80, 80))]:
        d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=c)
    return im


def house_img(w, h, plaque=None, lanterns=False, ruin=False, lc=(236, 236, 226)):
    roof = 18
    im, d = canvas(w + 16, h + roof + 8); x0, y0 = 8, 2
    if ruin:
        d.rectangle([x0, y0 + roof + 8, x0 + w, y0 + roof + h], fill=K)
        d.rectangle([x0 + 1, y0 + roof + 9, x0 + w - 1, y0 + roof + h - 1], fill=(48, 40, 46))
        pts = [(x0 + 1, y0 + roof + 9)]
        for x in range(x0 + 4, x0 + w, 6): pts.append((x, y0 + roof + 9 - random.randint(0, 12)))
        pts += [(x0 + w - 1, y0 + roof + 9)]
        d.polygon(pts + [(x0 + w - 1, y0 + roof + 14), (x0 + 1, y0 + roof + 14)], fill=(40, 32, 38))
        d.line(pts, fill=K)
        for _ in range(6):
            bx = random.randint(x0 + 4, x0 + w - 10); by = random.randint(y0 + roof + 16, y0 + roof + h - 4)
            d.line([(bx, by), (bx + random.randint(6, 12), by + random.randint(-3, 3))], fill=(20, 14, 18), width=2)
        for _ in range(8): im.putpixel((random.randint(x0 + 2, x0 + w - 2), random.randint(y0 + roof + 12, y0 + roof + h - 2)), (255, 120, 40, 255))
        return im, x0, y0 + roof + h
    d.rectangle([x0, y0 + roof, x0 + w, y0 + roof + h], fill=K)
    d.rectangle([x0 + 1, y0 + roof + 1, x0 + w - 1, y0 + roof + h - 1], fill=(150, 138, 140))
    d.rectangle([x0 + 1, y0 + roof + h - 6, x0 + w - 1, y0 + roof + h - 1], fill=(110, 100, 108))
    d.polygon([(x0 - 6, y0 + roof + 2), (x0 + w + 6, y0 + roof + 2), (x0 + w - 4, y0), (x0 + 4, y0)], fill=K)
    d.polygon([(x0 - 4, y0 + roof), (x0 + w + 4, y0 + roof), (x0 + w - 5, y0 + 2), (x0 + 5, y0 + 2)], fill=(52, 50, 72))
    for x in range(x0, x0 + w, 5): d.line([(x, y0 + 3), (x - 2, y0 + roof - 1)], fill=(70, 68, 92))
    dx = x0 + w // 2
    d.rectangle([dx - 7, y0 + roof + h - 20, dx + 7, y0 + roof + h - 1], fill=K); d.rectangle([dx - 6, y0 + roof + h - 19, dx + 6, y0 + roof + h - 1], fill=(70, 44, 36))
    for wx in (x0 + 8, x0 + w - 18):
        d.rectangle([wx, y0 + roof + 8, wx + 10, y0 + roof + 16], fill=K); d.rectangle([wx + 1, y0 + roof + 9, wx + 9, y0 + roof + 15], fill=(60, 40, 40))
        d.line([(wx + 5, y0 + roof + 9), (wx + 5, y0 + roof + 15)], fill=K)
    if plaque:
        d.rectangle([dx - 15, y0 + roof + 2, dx + 15, y0 + roof + 13], fill=K); d.rectangle([dx - 14, y0 + roof + 3, dx + 14, y0 + roof + 12], fill=(30, 26, 30))
        d.text((dx, y0 + roof + 7), plaque, font=font(10), fill=(236, 230, 210), anchor='mm')
    if lanterns:
        for lx in (dx - 22, dx + 22):
            d.rectangle([lx - 4, y0 + roof + 4, lx + 4, y0 + roof + 14], fill=K); d.rectangle([lx - 3, y0 + roof + 5, lx + 3, y0 + roof + 13], fill=lc)
    return im, x0, y0 + roof + h


def paifang_img():
    """任家镇牌坊：两根柱、三层檐、匾额"""
    im, d = canvas(104, 86)
    for x in (16, 84):
        d.rectangle([x - 5, 24, x + 5, 84], fill=K); d.rectangle([x - 4, 25, x + 4, 84], fill=(150, 46, 40)); d.rectangle([x - 4, 25, x - 2, 84], fill=(110, 30, 28))
        d.rectangle([x - 8, 78, x + 8, 85], fill=K); d.rectangle([x - 7, 79, x + 7, 84], fill=(120, 116, 128))
    d.rectangle([10, 34, 94, 40], fill=K); d.rectangle([11, 35, 93, 39], fill=(150, 46, 40))
    d.rectangle([30, 40, 74, 56], fill=K); d.rectangle([31, 41, 73, 55], fill=(30, 26, 36))
    d.text((52, 48), '任家镇', font=font(11), fill=(240, 200, 90), anchor='mm')
    for y0, x0, x1 in ((22, 2, 102), (10, 14, 90)):
        d.polygon([(x0, y0 + 10), (x1, y0 + 10), (x1 - 8, y0), (x0 + 8, y0)], fill=K)
        d.polygon([(x0 + 2, y0 + 9), (x1 - 2, y0 + 9), (x1 - 9, y0 + 1), (x0 + 9, y0 + 1)], fill=(52, 50, 72))
        d.line([(x0 - 2, y0 + 10), (x0 + 4, y0 + 6)], fill=K, width=2); d.line([(x1 + 2, y0 + 10), (x1 - 4, y0 + 6)], fill=K, width=2)
    d.rectangle([48, 2, 56, 10], fill=K); d.rectangle([49, 3, 55, 9], fill=(232, 180, 48))
    return im, 52, 85


def teahouse_img():
    """酒楼：三层飞檐楼阁，二楼挑出酒旗，门口红灯笼和酒坛，窗里透暖黄灯光"""
    Wd, Hd = 112, 150
    im, d = canvas(Wd, Hd)
    ROOF, ROOF2, ROOFH = (38, 70, 78), (24, 46, 54), (70, 110, 112)
    WALL, WALL2, PIL, WIN = (132, 72, 52), (104, 54, 42), (160, 48, 42), (255, 208, 100)
    def eave(x0, x1, y, th=9):          # 飞檐：宽屋顶，两端上翘
        d.polygon([(x0 - 8, y + th - 2), (x0 + 2, y + th), (x1 - 2, y + th), (x1 + 8, y + th - 2), (x1 + 4, y + th + 2), (x0 - 4, y + th + 2)], fill=K)
        d.polygon([(x0 + 4, y), (x1 - 4, y), (x1 + 6, y + th - 2), (x0 - 6, y + th - 2)], fill=K)
        d.polygon([(x0 + 5, y + 1), (x1 - 5, y + 1), (x1 + 4, y + th - 3), (x0 - 4, y + th - 3)], fill=ROOF)
        for x in range(x0 - 2, x1 + 4, 5): d.line([(x, y + 2), (x - 2, y + th - 3)], fill=ROOFH)
        d.line([(x0 - 4, y + th - 3), (x1 + 4, y + th - 3)], fill=ROOF2, width=1)
    def floor(x0, x1, y0, y1, windows, rail=False, lit=True):
        d.rectangle([x0, y0, x1, y1], fill=K); d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=WALL)
        d.rectangle([x0 + 1, y1 - 4, x1 - 1, y1 - 1], fill=WALL2)
        for px in (x0 + 2, x1 - 5): d.rectangle([px, y0 + 1, px + 3, y1 - 1], fill=PIL)
        for wx in windows:
            d.rectangle([wx, y0 + 6, wx + 11, y1 - 7], fill=K); d.rectangle([wx + 1, y0 + 7, wx + 10, y1 - 8], fill=WIN if lit else (60, 40, 40))
            d.line([(wx + 6, y0 + 7), (wx + 6, y1 - 8)], fill=K); d.line([(wx + 1, (y0 + y1) // 2), (wx + 10, (y0 + y1) // 2)], fill=K)
        if rail:
            d.rectangle([x0 - 3, y1 - 8, x1 + 3, y1 - 6], fill=K); d.rectangle([x0 - 2, y1 - 7, x1 + 2, y1 - 7], fill=PIL)
            for x in range(x0 - 1, x1 + 2, 4): d.line([(x, y1 - 6), (x, y1 - 1)], fill=K)
    # 三楼（最窄）
    eave(34, 78, 4, 10); floor(38, 74, 14, 40, [43, 56], False)
    d.rectangle([54, 0, 58, 5], fill=K); d.rectangle([55, 1, 57, 4], fill=(232, 180, 48))      # 宝顶
    # 二楼
    eave(24, 88, 38, 9); floor(28, 84, 47, 80, [34, 50, 66], True)
    # 一楼（最宽）
    eave(14, 98, 78, 10); floor(18, 94, 88, 138, [24, 76], False, True)
    # 门：大门敞开，里面是亮的
    dx = 56
    d.rectangle([dx - 11, 104, dx + 11, 138], fill=K); d.rectangle([dx - 10, 105, dx + 10, 138], fill=(70, 30, 26)); d.rectangle([dx - 7, 108, dx + 7, 138], fill=(255, 190, 90))
    d.line([(dx, 108), (dx, 138)], fill=K)
    d.rectangle([dx - 15, 90, dx + 15, 101], fill=K); d.rectangle([dx - 14, 91, dx + 14, 100], fill=(30, 26, 30))      # 匾额
    d.text((dx, 96), '酒楼', font=font(10), fill=(240, 200, 90), anchor='mm')
    # 红灯笼
    for lx in (dx - 24, dx + 24, 30, 82):
        d.line([(lx, 100 if lx in (dx - 24, dx + 24) else 80), (lx, 104 if lx in (dx - 24, dx + 24) else 86)], fill=K)
        ly = 104 if lx in (dx - 24, dx + 24) else 86
        d.rectangle([lx - 4, ly, lx + 4, ly + 9], fill=K); d.rectangle([lx - 3, ly + 1, lx + 3, ly + 8], fill=(214, 52, 42)); d.line([(lx, ly + 1), (lx, ly + 8)], fill=(255, 150, 90))
    # 酒坛
    for jx in (6, 100):
        d.ellipse([jx - 7, 122, jx + 7, 139], fill=K); d.ellipse([jx - 6, 123, jx + 6, 138], fill=(120, 72, 44)); d.rectangle([jx - 4, 119, jx + 4, 124], fill=K); d.rectangle([jx - 3, 120, jx + 3, 123], fill=(190, 40, 40))
        d.rectangle([jx - 3, 129, jx + 3, 134], fill=(226, 220, 196))
    # 台阶
    d.rectangle([dx - 16, 138, dx + 16, 143], fill=K); d.rectangle([dx - 15, 139, dx + 15, 142], fill=(130, 124, 132))
    # 酒旗：从二楼左侧挑出的竖幡，红底白字，下摆锯齿
    d.line([(14, 44), (14, 112)], fill=K, width=3); d.line([(14, 46), (2, 46)], fill=K, width=2)
    pts = [(1, 48), (13, 48), (13, 100), (10, 95), (7, 100), (4, 95), (1, 100)]
    d.polygon(pts, fill=K)
    d.polygon([(3, 50), (11, 50), (11, 97), (9, 93), (7, 97), (5, 93), (3, 97)], fill=(198, 44, 40))
    d.text((7, 66), '酒', font=font(10), fill=(250, 240, 220), anchor='mm')
    d.text((7, 80), '旗', font=font(1), fill=(198, 44, 40), anchor='mm')
    return im, Wd // 2, Hd - 4


def plant_img(var=0):
    """芭蕉（独立物件，能挡住人）"""
    im, d = canvas(56, 50); x, y = 28, 48
    d.ellipse([x - 12, y - 2, x + 12, y + 2], fill=(30, 20, 44))
    d.rectangle([x - 2, y - 22, x + 2, y], fill=K); d.rectangle([x - 1, y - 21, x + 1, y], fill=(80, 100, 60))
    leaves = [(-2.4, 26), (-1.9, 30), (-1.3, 30), (-0.8, 26), (-1.6, 22)]
    if var == 1: leaves = [(-2.6, 24), (-2.0, 28), (-1.2, 32), (-0.6, 24), (-1.7, 20)]
    if var == 2: leaves = [(-2.3, 28), (-1.7, 26), (-1.1, 28), (-0.9, 22), (-2.8, 20)]
    for ang, ln in leaves:
        ex, ey = x + math.cos(ang) * ln, y - 20 + math.sin(ang) * ln * 0.8
        nx, ny = -(ey - (y - 20)) / ln * 6, (ex - x) / ln * 6
        poly = [(x, y - 20), (x + (ex - x) * 0.5 + nx, (y - 20) + (ey - (y - 20)) * 0.5 + ny), (ex, ey), (x + (ex - x) * 0.5 - nx, (y - 20) + (ey - (y - 20)) * 0.5 - ny)]
        d.polygon(poly, fill=K); d.polygon([(a * 0.96 + x * 0.04, b * 0.96 + (y - 20) * 0.04) for a, b in poly], fill=(46, 96, 58))
        d.line([(x, y - 20), (ex, ey)], fill=(80, 140, 80))
    return im


def church_img():
    im, d = canvas(132, 250); c, b = 66, 228          # b = door bottom
    d.rectangle([8, 124, 124, 172], fill=K); d.rectangle([9, 125, 123, 171], fill=(58, 60, 82))
    for x in range(10, 123, 5): d.line([(x, 126), (x, 170)], fill=(48, 50, 70))
    d.rectangle([22, 150, 110, b], fill=K); d.rectangle([23, 151, 109, b - 1], fill=(178, 172, 182))
    d.polygon([(20, 152), (112, 152), (c, 126)], fill=K); d.polygon([(24, 151), (108, 151), (c, 129)], fill=(160, 154, 168))
    d.rectangle([c - 15, 70, c + 15, 150], fill=K); d.rectangle([c - 14, 71, c + 14, 149], fill=(186, 180, 190))
    d.polygon([(c - 17, 72), (c + 17, 72), (c, 30)], fill=K); d.polygon([(c - 14, 71), (c + 14, 71), (c, 34)], fill=(60, 62, 86))
    d.rectangle([c - 2, 8, c + 2, 32], fill=K); d.rectangle([c - 7, 13, c + 7, 17], fill=K)
    d.rectangle([c - 1, 9, c + 1, 31], fill=(200, 190, 150)); d.rectangle([c - 6, 14, c + 6, 16], fill=(200, 190, 150))
    d.ellipse([c - 8, 80, c + 8, 96], fill=K); d.ellipse([c - 6, 82, c + 6, 94], fill=(90, 40, 60))
    d.line([(c - 5, 88), (c + 5, 88)], fill=K); d.line([(c, 83), (c, 93)], fill=K)
    d.rectangle([c - 5, 106, c + 5, 128], fill=K); d.pieslice([c - 5, 101, c + 5, 111], 180, 360, fill=K)
    for wx in (32, 90):
        d.rectangle([wx, 172, wx + 9, 196], fill=K); d.pieslice([wx, 166, wx + 9, 178], 180, 360, fill=K)
        d.rectangle([wx + 1, 173, wx + 8, 195], fill=(70, 50, 70))
        for yy in (178, 188): d.line([(wx - 2, yy), (wx + 11, yy + 3)], fill=(120, 86, 56), width=2)
    d.rectangle([c - 13, b - 38, c + 13, b], fill=K); d.pieslice([c - 13, b - 52, c + 13, b - 26], 180, 360, fill=K)
    d.rectangle([c - 11, b - 37, c + 11, b - 1], fill=(80, 46, 30)); d.pieslice([c - 11, b - 50, c + 11, b - 28], 180, 360, fill=(80, 46, 30))
    for yy, sl in ((b - 32, 4), (b - 20, -4), (b - 9, 3)):
        d.line([(c - 17, yy), (c + 17, yy + sl)], fill=K, width=5); d.line([(c - 16, yy), (c + 16, yy + sl)], fill=(140, 100, 60), width=3)
    d.line([(c - 11, b - 28), (c + 11, b - 14)], fill=(150, 150, 160), width=2); d.line([(c + 11, b - 28), (c - 11, b - 14)], fill=(150, 150, 160), width=2)
    d.rectangle([c - 3, b - 24, c + 3, b - 18], fill=(110, 110, 120))
    for x in (c - 17, c + 12):
        d.rectangle([x, b - 30, x + 5, b - 20], fill=K); d.rectangle([x + 1, b - 29, x + 4, b - 21], fill=(240, 220, 110)); d.line([(x + 2, b - 28), (x + 2, b - 22)], fill=(200, 40, 30))
    for x in range(2, 130, 8):
        d.rectangle([x, b + 6, x + 3, b + 19], fill=K); d.rectangle([x + 1, b + 7, x + 2, b + 18], fill=(90, 90, 104))
    d.line([(2, b + 10), (130, b + 10)], fill=(90, 90, 104))
    return im, c, b


def villager_spr(g):
    Spr, PAL = g['Spr'], g['PAL']
    PAL.update({'a': (200, 168, 96), 'A': (150, 120, 64), 'c': (64, 96, 156), 'C': (42, 64, 112)})
    s = Spr(22, 30)
    s.rect(3, 5, 17, 6, 'a'); s.rect(6, 3, 14, 4, 'a'); s.rect(8, 2, 12, 2, 'A'); s.rect(3, 6, 17, 6, 'A')
    s.rect(7, 7, 13, 12, 's'); s.rect(7, 7, 8, 12, 'S'); s.px(11, 9, 'k'); s.px(12, 11, 'k'); s.px(14, 10, 's')
    s.rect(6, 13, 13, 21, 'c'); s.rect(6, 13, 7, 21, 'C'); s.rect(6, 17, 13, 17, 'C')
    s.rect(12, 14, 15, 16, 'c'); s.px(16, 15, 's')
    s.px(17, 16, 'k'); s.rect(16, 17, 18, 20, 'p'); s.rect(16, 18, 18, 18, 'r')
    s.rect(7, 22, 12, 24, 'C'); s.rect(7, 25, 8, 26, 'h'); s.rect(11, 25, 12, 26, 'h')
    s.outline()
    return s.img()


# ---------------- world ----------------
def build(seed=11):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), (58, 42, 80, 255)); d = ImageDraw.Draw(im)
    blocks = []
    def block(x0, y0, x1, y1): blocks.append((x0, y0, x1, y1))
    objs = []          # {k, x, y(base), img, ax, ay, ...}
    sprites = {'tree': tree_img(), 'treeB': tree_img(True)}

    for _ in range(46000):
        im.putpixel((random.randrange(W), random.randrange(H)), random.choice([(70, 52, 96, 255), (46, 33, 64, 255), (64, 48, 88, 255)]))
    d.rectangle([PLAT_X, 0, W, PLAT_Y], fill=(46, 56, 72))
    for _ in range(12000):
        im.putpixel((random.randrange(PLAT_X, W), random.randrange(0, PLAT_Y)), random.choice([(56, 68, 84, 255), (38, 46, 62, 255), (50, 76, 72, 255)]))
    for _ in range(700):
        x, y = random.randrange(W), random.randrange(H)
        for dx, hh in ((0, 2), (1, 3), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 86, 84))

    def road(pts, w=30):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 3) + 1
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                d.ellipse([x - w / 2, y - w / 2.6, x + w / 2, y + w / 2.6], fill=(98, 80, 94))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 6) + 1
            for i in range(n):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                for c, p in (((120, 100, 112, 255), 0.6), ((78, 62, 80, 255), 0.3)):
                    if random.random() < p:
                        px_, py_ = int(x + random.randint(-9, 9)), int(y + random.randint(-6, 6))
                        if 0 <= px_ < W and 0 <= py_ < H: im.putpixel((px_, py_), c)
    road(ROAD); road(ROAD_N, 26)

    # mass grave: irregular dark patches + bones
    mg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(mg)
    for _ in range(40):
        x, y = random.randrange(930, 1500), random.randrange(840, 1160); r = random.randint(30, 80)
        md.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(18, 8, 22, 22))
    im.alpha_composite(mg)
    for _ in range(70):
        x, y = random.randrange(940, 1500), random.randrange(850, 1160)
        d.line([(x, y), (x + random.choice([-4, 4]), y + random.choice([-2, 2]))], fill=(220, 214, 200))

    # river + bridge
    for y in range(H):
        for cx, rw in channels(y):
            d.line([(cx - rw / 2 - 4, y), (cx + rw / 2 + 4, y)], fill=(40, 34, 52))
        for cx, rw in channels(y):
            d.line([(cx - rw / 2, y), (cx + rw / 2, y)], fill=(30, 46, 84))
            if y % 3 == 0:
                x = cx + random.uniform(-rw / 2 + 4, rw / 2 - 8); d.line([(x, y), (x + random.randint(3, 7), y)], fill=(60, 92, 140))
            if not (BRIDGE[0] - 2 < y < BRIDGE[1] + 2) and y % 8 == 0:
                block(int(cx - rw / 2 - 2), y, int(cx + rw / 2 + 2), y + 8)
    # 龙吐珠：环中间的圆土丘 + 一颗圆石（珠）
    ly = (LOOP[0] + LOOP[1]) // 2; lx = int(river_x(ly) + loop_off(ly) - 3)
    PEARL = (lx, ly)
    _cL, _wL = channels(ly)[0]; HB = [int(_cL - _wL / 2 - 14), ly - 7, int(_cL + _wL / 2 + 16), ly + 7]      # 隐形桥：横跨左边那股河
    d.ellipse([lx - 30, ly - 22, lx + 30, ly + 22], fill=(70, 56, 64)); d.ellipse([lx - 26, ly - 19, lx + 26, ly + 17], fill=(92, 76, 80))
    d.ellipse([lx - 9, ly - 14, lx + 9, ly + 2], fill=K); d.ellipse([lx - 8, ly - 13, lx + 8, ly + 1], fill=(200, 196, 214)); d.ellipse([lx - 5, ly - 11, lx - 1, ly - 7], fill=(250, 250, 255))
    d.text((lx, ly + 10), '珠', font=font(9), fill=(230, 210, 150), anchor='mm')
    by0, by1 = BRIDGE; bx = river_x((by0 + by1) / 2); bx0, bx1 = int(bx - RIVER_W / 2 - 16), int(bx + RIVER_W / 2 + 16)
    d.rectangle([bx0, by0 - 2, bx1, by1 + 6], fill=K); d.rectangle([bx0 + 1, by0, bx1 - 1, by1], fill=(132, 126, 150))
    for x in range(bx0 + 4, bx1 - 4, 10): d.line([(x, by0 + 3), (x, by1 - 3)], fill=(110, 104, 130))
    d.rectangle([bx0 + 1, by1, bx1 - 1, by1 + 5], fill=(90, 84, 110))
    for yy in (by0 - 4, by1 - 4):
        d.rectangle([bx0, yy, bx1, yy + 4], fill=K); d.rectangle([bx0 + 1, yy + 1, bx1 - 1, yy + 3], fill=(170, 164, 186))
        for x in range(bx0 + 2, bx1, 12): d.rectangle([x, yy - 4, x + 3, yy + 2], fill=K); d.rectangle([x + 1, yy - 3, x + 2, yy + 1], fill=(170, 164, 186))
    block(bx0, by0 - 8, bx1, by0 - 2); block(bx0, by1 + 1, bx1, by1 + 8)

    # plateau cliff + stairs
    face = 30
    d.rectangle([PLAT_X, PLAT_Y, W, PLAT_Y + face], fill=(46, 36, 52))
    for x in range(PLAT_X, W, 7): d.line([(x, PLAT_Y + 2), (x + random.randint(-2, 2), PLAT_Y + face - 2)], fill=(36, 28, 42))
    d.rectangle([PLAT_X, PLAT_Y - 2, W, PLAT_Y + 1], fill=(112, 112, 136))
    d.rectangle([PLAT_X - 8, 0, PLAT_X, PLAT_Y + face], fill=(46, 36, 52)); d.rectangle([PLAT_X - 1, 0, PLAT_X + 1, PLAT_Y], fill=(112, 112, 136))
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([PLAT_X - 8, PLAT_Y + face, W, PLAT_Y + face + 12], fill=(10, 6, 20, 100))
    im.alpha_composite(sh)
    sx0, sx1 = STAIRS
    d.rectangle([sx0, PLAT_Y - 4, sx1, PLAT_Y + face + 2], fill=K)
    for i, y in enumerate(range(PLAT_Y - 3, PLAT_Y + face + 1, 5)):
        d.rectangle([sx0 + 1, y, sx1 - 1, y + 4], fill=(150 - i * 6, 144 - i * 6, 168 - i * 6)); d.line([(sx0 + 1, y + 4), (sx1 - 1, y + 4)], fill=(80, 74, 98))
    block(PLAT_X - 8, 0, PLAT_X + 2, PLAT_Y + face)
    block(PLAT_X, PLAT_Y - 2, sx0, PLAT_Y + face); block(sx1, PLAT_Y - 2, W, PLAT_Y + face)

    # 城墙取消：原城墙处变成荒地，任家镇移到地图上方新加的一大块
    cimg, cax, cay = church_img(); sprites['church'] = cimg
    objs.append(dict(k='church', x=CHURCH[0], y=CHURCH[1], img='church', ax=cax, ay=cay, rect=[CHURCH[0] - 60, CHURCH[1] - 110, CHURCH[0] + 60, CHURCH[1] + 20], burn=False))
    block(CHURCH[0] - 58, CHURCH[1] - 104, CHURCH[0] + 58, CHURCH[1] + 20)
    bats = (CHURCH[0], CHURCH[1] - 205)

    # trees along the roads (objects)
    trees = []
    for (x0, y0), (x1, y1) in list(zip(ROAD, ROAD[1:]))[2:7]:
        L = math.hypot(x1 - x0, y1 - y0); nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        for t in range(20, int(L) - 10, 44):
            x, y = x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L
            if abs(x - 760) < 50 or abs(x - 300) < 60: continue
            for side in (-1, 1): trees.append((int(x + nx * 30 * side), int(y + ny * 26 * side)))
    for y in range(206, 590, 46):
        if abs(y - 400) < 20: continue
        for side in (-1, 1): trees.append((int(752 - (y - 104) * 0.04 + side * 30), y))
    trees = [(x, y) for x, y in trees if not (x > PLAT_X - 10 and y < PLAT_Y + 40) and not in_water(x, y, 16)]
    for x, y in trees:
        objs.append(dict(k='tree', x=x, y=y, img='tree', ax=15, ay=46)); block(x - 3, y - 4, x + 3, y + 1)

    # border forest + dead trees baked into background
    def bgtree(x, y, dead=False):
        if dead:
            tr = (26, 18, 36)
            d.ellipse([x - 10, y - 2, x + 10, y + 3], fill=(38, 26, 52)); d.rectangle([x - 2, y - 36, x + 2, y], fill=tr)
            for a, b in [((0, -26), (-12, -40)), ((0, -30), (12, -46)), ((-8, -35), (-14, -44)), ((0, -14), (10, -20))]:
                d.line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], fill=tr, width=2)
            return
        for (ox, oy, r) in [(0, -24, 13), (-7, -18, 9), (7, -18, 9), (0, -32, 8)]:
            d.ellipse([x + ox - r - 1, y + oy - r - 1, x + ox + r + 1, y + oy + r + 1], fill=K)
        for (ox, oy, r, c) in [(0, -24, 13, (24, 40, 48)), (-7, -18, 9, (16, 26, 34)), (7, -18, 9, (24, 40, 48)), (0, -32, 8, (34, 56, 62))]:
            d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=c)
    border = []
    for x in range(10, W, 26): border.append((x + random.randint(-4, 4), H - 4 - random.randint(0, 10)))
    for y in range(PLAT_Y + 60, H, 26): border.append((W - 10 + random.randint(-4, 4), y))
    block(0, H - 22, W, H); block(W - 22, PLAT_Y + 40, W, H); block(W - 4, 0, W, PLAT_Y + 40)
    deads = [(random.randrange(320, 1150), random.randrange(720, 1150)) for _ in range(8)] + [(80, 380), (1250, 700)]
    border = [(x, y) for x, y in border if not in_water(x, y, 14)]

    graves, coffins, flags = [], [], []
    def free(x, y, r):
        if (x - 760) ** 2 + (y - 612) ** 2 < 70 ** 2: return False
        for pts in (ROAD, ROAD_N):
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2; t = max(0, min(1, ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / L2))
                if (x - (x0 + (x1 - x0) * t)) ** 2 + (y - (y0 + (y1 - y0) * t)) ** 2 < (r + 38) ** 2: return False
        if in_water(x, y, r + 10): return False
        if x > PLAT_X - 20 and y < PLAT_Y + 50: return False
        if y < 200: return False
        if any((x - a) ** 2 + (y - b) ** 2 < (r + 26) ** 2 for a, b in trees + graves + coffins + deads): return False
        return True
    for _ in range(30000):
        if len(graves) >= 46: break
        x, y = random.randrange(320, 1150), (random.randrange(660, 860) if random.random() < 0.6 else random.randrange(220, 1150))
        if x > 940 and y > 820: continue
        if free(x, y, 16): graves.append((x, y))
    for _ in range(20000):
        if len(coffins) >= 12: break
        x, y = random.randrange(960, 1460), random.randrange(860, 1140)
        if free(x, y, 18): coffins.append((x, y))
    for _ in range(8000):
        if len(flags) >= 14: break
        x, y = random.randrange(930, 1500), random.randrange(830, 1150)
        if all((x - a) ** 2 + (y - b) ** 2 > 24 ** 2 for a, b in coffins + flags): flags.append((x, y))

    def grave(x, y, charm=False, broken=False):
        d.ellipse([x - 16, y - 8, x + 16, y + 9], fill=K); d.ellipse([x - 15, y - 7, x + 15, y + 8], fill=(98, 72, 92)); d.ellipse([x - 12, y - 6, x + 8, y + 2], fill=(118, 92, 112))
        sx, sy = x - 5, y - 4; hgt = 9 if broken else 14
        d.rectangle([sx - 1, sy - hgt - 1, sx + 11, sy + 1], fill=K); d.rectangle([sx, sy - hgt, sx + 10, sy], fill=(146, 140, 166)); d.rectangle([sx + 8, sy - hgt, sx + 10, sy], fill=(110, 104, 132))
        if not broken: d.rectangle([sx + 1, sy - hgt - 2, sx + 9, sy - hgt - 1], fill=(146, 140, 166)); d.line([(sx + 1, sy - hgt - 3), (sx + 9, sy - hgt - 3)], fill=K)
        else: d.line([(sx, sy - hgt), (sx + 4, sy - hgt + 2), (sx + 10, sy - hgt - 1)], fill=K)
        for yy in range(sy - hgt + 3, sy - 1, 2): d.line([(sx + 4, yy), (sx + 6, yy)], fill=(60, 54, 80))
        if charm: d.rectangle([sx + 2, sy - hgt + 1, sx + 6, sy - hgt + 9], fill=(250, 228, 120)); d.line([(sx + 4, sy - hgt + 2), (sx + 4, sy - hgt + 8)], fill=(210, 44, 40))
        block(sx - 1, sy - 3, sx + 11, sy + 1)

    def coffin(x, y, opened):
        d.ellipse([x - 18, y + 2, x + 18, y + 8], fill=(30, 20, 44))
        pts = [(x - 17, y - 4), (x + 15, y - 7), (x + 17, y + 3), (x - 15, y + 6)]
        d.polygon([(a - 1 if a < x else a + 1, b - 1 if b < y else b + 1) for a, b in pts], fill=K); d.polygon(pts, fill=(78, 40, 30))
        if opened:
            d.polygon([(x - 13, y - 2), (x + 12, y - 5), (x + 13, y + 1), (x - 12, y + 4)], fill=(20, 10, 16))
            d.polygon([(x - 6, y - 14), (x + 22, y - 18), (x + 24, y - 12), (x - 4, y - 8)], fill=K); d.polygon([(x - 5, y - 13), (x + 21, y - 17), (x + 22, y - 13), (x - 4, y - 9)], fill=(100, 54, 38))
        else:
            d.line([(x - 15, y - 2), (x + 14, y - 5)], fill=(120, 66, 44))
            d.rectangle([x - 3, y - 4, x + 1, y + 2], fill=(240, 220, 110)); d.line([(x - 1, y - 3), (x - 1, y + 1)], fill=(200, 40, 30))
        block(x - 16, y - 6, x + 16, y + 4)

    def flag(x, y):
        d.line([(x, y), (x, y - 34)], fill=K, width=2)
        d.polygon([(x + 1, y - 33), (x + 9, y - 31), (x + 7, y - 22), (x + 10, y - 12), (x + 1, y - 16)], fill=K)
        d.polygon([(x + 1, y - 32), (x + 8, y - 30), (x + 6, y - 22), (x + 8, y - 14), (x + 1, y - 17)], fill=(226, 226, 220))

    def cross(x, y, tilt=0):
        d.ellipse([x - 13, y - 5, x + 13, y + 7], fill=K); d.ellipse([x - 12, y - 4, x + 12, y + 6], fill=(70, 76, 92)); d.ellipse([x - 9, y - 3, x + 7, y + 2], fill=(86, 92, 110))
        cx, top = x + tilt, y - 26
        d.rectangle([cx - 3, top - 1, cx + 3, y + 1], fill=K); d.rectangle([cx - 2, top, cx + 2, y], fill=(176, 176, 190)); d.rectangle([cx + 1, top, cx + 2, y], fill=(132, 132, 150))
        d.rectangle([cx - 9, top + 5, cx + 9, top + 11], fill=K); d.rectangle([cx - 8, top + 6, cx + 8, top + 10], fill=(176, 176, 190)); d.rectangle([cx - 8, top + 9, cx + 8, top + 10], fill=(132, 132, 150))
        block(x - 4, y - 3, x + 4, y + 1)

    def grandpa(x, y):
        """蜻蜓点水穴：长而大的坟包，中间一个很窄的竖坑；坑口盖着一层石灰（风水先生阴了任家），旁边黄土堆、三脚架、无字碑"""
        d.ellipse([x - 62, y - 22, x + 62, y + 24], fill=(70, 52, 60)); d.ellipse([x - 54, y - 18, x + 50, y + 14], fill=(88, 66, 74))
        for dx, dy in ((-44, 6), (40, 8), (-30, -12), (36, -8)): d.ellipse([x + dx - 9, y + dy - 5, x + dx + 9, y + dy + 4], fill=(150, 120, 60)); d.ellipse([x + dx - 6, y + dy - 4, x + dx + 4, y + dy + 1], fill=(176, 144, 76))
        # 石灰层：坑口周围一大片灰白，裂成几块
        d.ellipse([x - 26, y - 12, x + 26, y + 14], fill=(206, 206, 200)); d.ellipse([x - 22, y - 9, x + 20, y + 10], fill=(226, 226, 220))
        for a, b in (((-18, -4), (-6, 2)), ((8, -8), (18, 4)), ((-10, 8), (4, 4))): d.line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], fill=(160, 158, 156))
        for _ in range(40): d.point((x + random.randint(-38, 38), y + random.randint(-14, 16)), fill=(236, 236, 230))
        # 窄竖坑（四尺 × 三尺），坑底干的
        d.rectangle([x - 6, y - 7, x + 6, y + 8], fill=K); d.rectangle([x - 5, y - 6, x + 5, y + 7], fill=(18, 10, 16)); d.line([(x - 5, y + 6), (x + 5, y + 6)], fill=(200, 200, 196))
        top = (x, y - 46)
        for fx, fy in ((x - 22, y + 10), (x + 22, y + 10), (x + 2, y - 14)): d.line([top, (fx, fy)], fill=K, width=3); d.line([top, (fx, fy)], fill=(110, 72, 40), width=1)
        d.rectangle([x - 3, y - 49, x + 3, y - 43], fill=K); d.rectangle([x - 2, y - 48, x + 2, y - 44], fill=(150, 146, 160))
        d.line([(x, y - 43), (x, y - 2)], fill=(200, 180, 130))
        tx, ty = x + 40, y - 10
        d.rectangle([tx - 7, ty - 18, tx + 7, ty], fill=K); d.rectangle([tx - 6, ty - 17, tx + 6, ty - 1], fill=(146, 140, 166)); d.rectangle([tx + 3, ty - 17, tx + 6, ty - 1], fill=(110, 104, 132))
        block(tx - 8, ty - 4, tx + 8, ty + 1)

    def plantain(x, y):
        """芭蕉：几片宽大的叶子"""
        d.ellipse([x - 12, y - 2, x + 12, y + 3], fill=(30, 20, 44))
        d.rectangle([x - 2, y - 22, x + 2, y], fill=K); d.rectangle([x - 1, y - 21, x + 1, y], fill=(80, 100, 60))
        for ang, ln in ((-2.4, 26), (-1.9, 30), (-1.3, 30), (-0.8, 26), (-1.6, 22)):
            ex, ey = x + math.cos(ang) * ln, y - 20 + math.sin(ang) * ln * 0.8
            nx, ny = -(ey - (y - 20)) / ln * 6, (ex - x) / ln * 6
            poly = [(x, y - 20), (x + (ex - x) * 0.5 + nx, (y - 20) + (ey - (y - 20)) * 0.5 + ny), (ex, ey), (x + (ex - x) * 0.5 - nx, (y - 20) + (ey - (y - 20)) * 0.5 - ny)]
            d.polygon(poly, fill=K); d.polygon([(a * 0.96 + x * 0.04, b * 0.96 + (y - 20) * 0.04) for a, b in poly], fill=(46, 96, 58))
            d.line([(x, y - 20), (ex, ey)], fill=(80, 140, 80))
        block(x - 3, y - 3, x + 3, y + 1)

    def signpost(x, y):
        d.ellipse([x - 8, y - 2, x + 8, y + 3], fill=(30, 20, 44))
        d.rectangle([x - 2, y - 56, x + 2, y], fill=K); d.rectangle([x - 1, y - 55, x + 1, y], fill=(120, 80, 50))
        f = font(9)
        # 任家镇: board with arrow pointing up (towards the wall)
        x0, yy, w = x - 17, y - 50, 34
        poly = [(x0, yy), (x - 4, yy), (x, yy - 7), (x + 4, yy), (x0 + w, yy), (x0 + w, yy + 11), (x0, yy + 11)]
        d.polygon(poly, fill=K); d.polygon([(x0 + 1, yy + 1), (x - 4, yy + 1), (x, yy - 5), (x + 4, yy + 1), (x0 + w - 1, yy + 1), (x0 + w - 1, yy + 10), (x0 + 1, yy + 10)], fill=(176, 130, 80))
        d.text((x, yy + 6), '任家镇', font=f, fill=(40, 22, 14), anchor='mm')
        # 腾腾镇: board pointing left (towards the bridge)
        x1, yy = x + 4, y - 34
        poly = [(x1 - 40, yy + 5.5), (x1 - 34, yy), (x1, yy), (x1, yy + 11), (x1 - 34, yy + 11)]
        d.polygon(poly, fill=K); d.polygon([(x1 - 38, yy + 5.5), (x1 - 33, yy + 1), (x1 - 1, yy + 1), (x1 - 1, yy + 10), (x1 - 33, yy + 10)], fill=(176, 130, 80))
        d.text((x1 - 17, yy + 6), '腾腾镇', font=f, fill=(40, 22, 14), anchor='mm')
        block(x - 3, y - 3, x + 3, y + 1)

    items = [('td', x, y) for x, y in border] + [('dd', x, y) for x, y in deads] + [('g', x, y) for x, y in graves] + \
            [('c', x, y) for x, y in coffins] + [('f', x, y) for x, y in flags] + [('s', 806, 668)] + \
            [('x', x, y) for x, y in CROSSES]
    for k, x, y in sorted(items, key=lambda t: t[2]):
        if k == 'td': bgtree(x, y)
        elif k == 'dd': bgtree(x, y, True)
        elif k == 'g': r = random.random(); grave(x, y, r < 0.25, 0.25 <= r < 0.45)
        elif k == 'c': coffin(x, y, random.random() < 0.35)
        elif k == 'f': flag(x, y)
        elif k == 's': signpost(x, y)
        elif k == 'x': cross(x, y, (x * 7 + y) % 3 - 1)
        elif k == 'c2': coffin(x, y, x in (1045, 1090))
        elif k == 'tomb': grandpa(x, y)
        elif k == 'pl': plantain(x, y)
    for (x, y) in [(560, 668), (980, 600), (1240, 590), (720, 300)]:
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        for r in range(22, 4, -2): gd.ellipse([x - r, y - 19 - r, x + r, y - 19 + r], fill=(255, 236, 190, 9))
        im.alpha_composite(glow)
        d.line([(x, y - 24), (x, y)], fill=(26, 18, 36), width=2)
        d.rectangle([x - 5, y - 24, x + 5, y - 14], fill=K); d.rectangle([x - 4, y - 23, x + 4, y - 15], fill=(236, 236, 226))
        block(x - 2, y - 3, x + 2, y + 1)
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
    for _ in range(110):
        x, y = random.randrange(-60, W), random.randrange(0, H); fd.ellipse([x, y, x + 170, y + 16], fill=(170, 160, 210, 22))
    im.alpha_composite(fog)

    # ================= 任家镇（地图上方新加的一块）=================
    DY = TOWN_H
    big = Image.new('RGBA', (W, H + DY), (58, 42, 80, 255)); big.alpha_composite(im, (0, DY))
    im = big; d = ImageDraw.Draw(im)
    blocks[:] = [(x0, y0 + DY, x1, y1 + DY) for x0, y0, x1, y1 in blocks]
    for o in objs:
        o['y'] += DY
        if 'rect' in o: o['rect'] = [o['rect'][0], o['rect'][1] + DY, o['rect'][2], o['rect'][3] + DY]
    graves[:] = [(x, y + DY) for x, y in graves]; coffins[:] = [(x, y + DY) for x, y in coffins]
    bats = (bats[0], bats[1] + DY)
    random.seed(77)
    for _ in range(9000): im.putpixel((random.randrange(W), random.randrange(DY)), random.choice([(70, 52, 96, 255), (46, 33, 64, 255), (64, 48, 88, 255)]))
    for _ in range(140):
        x, y = random.randrange(W), random.randrange(DY)
        for dx, hh in ((0, 2), (1, 3), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 86, 84))
    # 河继续往上流
    for y in range(0, DY):
        cx = river_x(y - DY)
        d.line([(cx - RIVER_W / 2 - 4, y), (cx + RIVER_W / 2 + 4, y)], fill=(40, 34, 52)); d.line([(cx - RIVER_W / 2, y), (cx + RIVER_W / 2, y)], fill=(30, 46, 84))
        if y % 5 == 0: xx = cx + random.uniform(-RIVER_W / 2 + 4, RIVER_W / 2 - 8); d.line([(xx, y), (xx + random.randint(3, 7), y)], fill=(60, 92, 140))
        if y % 8 == 0: block(int(cx - RIVER_W / 2 - 2), y, int(cx + RIVER_W / 2 + 2), y + 8)
    # 高台上沿（教堂高台北边的石壁）
    d.rectangle([PLAT_X - 8, DY - 8, W, DY + 2], fill=K); d.rectangle([PLAT_X - 7, DY - 7, W, DY], fill=(110, 104, 128)); block(PLAT_X - 8, DY - 10, W, DY + 2)
    # 街道：东西主街 + 南北中轴，接到原来往北的路
    road([(300, 262), (760, 258), (1180, 262), (1580, 258)], 30)
    road([(740, 40), (740, 262), (740, DY + 110)], 28)
    # 上边界树林
    for x in range(0, W, 22):
        tx, ty = x + random.randint(-3, 3), 14 + random.randint(0, 8)
        if abs(tx - river_x(ty - DY)) > RIVER_W / 2 + 14: bgtree(tx, ty)
    block(0, 0, W, 30)
    RED = (220, 60, 50)
    hn = [10]
    def house(x0, y0, w, h, plaque=None, lan=False, lc=(236, 236, 226)):
        img, ax, ay = house_img(w, h, plaque, lan, lc=lc); key = f'town{hn[0]}'; hn[0] += 1; sprites[key] = img
        objs.append(dict(k='house', x=x0 + w // 2, y=y0 + 18 + h, img=key, ax=ax + w // 2, ay=ay, rect=[x0, y0, x0 + w, y0 + 18 + h], burn=False))
        block(x0 - 2, y0 + 10, x0 + w + 2, y0 + 18 + h)
    def wall(x0, y0, x1, y1, col=(120, 112, 120), top=(90, 84, 92)):
        d.rectangle([x0 - 1, y0 - 4, x1 + 1, y1 + 1], fill=K); d.rectangle([x0, y0 - 3, x1, y1], fill=col); d.rectangle([x0, y0 - 3, x1, y0 - 1], fill=top); block(x0, y0 - 2, x1, y1)
    def floor(x0, y0, x1, y1, c=(78, 66, 80), c2=(70, 58, 72)):
        d.rectangle([x0, y0, x1, y1], fill=c)
        for x in range(x0 + 4, x1, 9): d.line([(x, y0 + 2), (x, y1 - 1)], fill=c2)
    def lantern_post(x, y, c=(220, 60, 50)):
        d.line([(x, y), (x, y - 22)], fill=K, width=2); d.rectangle([x - 4, y - 30, x + 4, y - 20], fill=K); d.rectangle([x - 3, y - 29, x + 3, y - 21], fill=c); block(x - 2, y - 3, x + 2, y + 1)
    def lion(x, y):
        d.ellipse([x - 8, y - 2, x + 8, y + 6], fill=(30, 20, 44)); d.rectangle([x - 6, y - 16, x + 6, y + 2], fill=K); d.rectangle([x - 5, y - 15, x + 5, y + 1], fill=(140, 138, 150))
        d.rectangle([x - 4, y - 14, x + 4, y - 8], fill=(170, 168, 180)); d.point((x - 2, y - 12), fill=K); d.point((x + 2, y - 12), fill=K); block(x - 6, y - 6, x + 6, y + 4)
    def stall(x, y, c):
        d.rectangle([x - 18, y - 4, x + 18, y + 8], fill=K); d.rectangle([x - 17, y - 3, x + 17, y + 7], fill=(110, 80, 60))
        d.polygon([(x - 22, y - 6), (x + 22, y - 6), (x + 18, y - 18), (x - 18, y - 18)], fill=K); d.polygon([(x - 20, y - 7), (x + 20, y - 7), (x + 17, y - 17), (x - 17, y - 17)], fill=c)
        for i in range(-16, 18, 8): d.line([(x + i, y - 17), (x + i - 2, y - 7)], fill=(240, 230, 210))
        block(x - 18, y - 2, x + 18, y + 8)
    # ---- 主街北侧 ----
    # 任府大宅院：院墙 + 正堂 + 院子里两棵树
    floor(296, 150, 566, 236, (84, 72, 70), (76, 64, 62)); wall(290, 74, 296, 244); wall(564, 74, 570, 244); wall(290, 238, 408, 244); wall(452, 238, 570, 244)
    house(345, 78, 170, 56, '任府', True, RED)
    for gx in (404, 456): lantern_post(gx, 246)
    bgtree(318, 228); bgtree(540, 228)
    # 衙门
    house(588, 154, 112, 48, '衙门', True, RED); lion(578, 248); lion(712, 248)
    # 中轴北端：祠堂
    house(692, 36, 96, 40, '祠堂', True, RED)
    # 茶楼
    timg, tax, tay = teahouse_img(); sprites['town_tea'] = timg
    objs.append(dict(k='house', x=830, y=246, img='town_tea', ax=tax, ay=tay, rect=[774, 100, 886, 246], burn=False)); block(784, 196, 878, 246)
    # 铺子一排
    house(900, 186, 70, 40, '米铺'); house(984, 186, 86, 40, '棺材铺'); house(1084, 190, 66, 36)
    # 义庄院落
    house(1196, 184, 80, 42, '纸扎'); house(1300, 188, 70, 38, '酒'); house(1380, 192, 56, 34)
    house(1450, 186, 74, 40); house(1530, 194, 56, 32)
    # ---- 主街南侧 ----
    d.ellipse([594, 300, 618, 314], fill=K); d.ellipse([596, 301, 616, 312], fill=(110, 108, 124)); d.ellipse([600, 303, 612, 310], fill=(20, 30, 50)); block(594, 302, 618, 314)   # 水井
    stall(640, 330, (180, 50, 50)); stall(690, 380, (60, 90, 140)); stall(640, 430, (170, 130, 50))
    for lx in (1480,): lantern_post(lx, 286)
    # 义庄院落：主街南侧、中轴路东边。正堂在北面背靠主街，院门开在北墙左侧
    floor(820, 300, 1140, 470)
    wall(814, 296, 820, 476); wall(1140, 296, 1146, 476); wall(814, 296, 1146, 302); wall(814, 470, 952, 476); wall(1008, 470, 1146, 476)
    house(915, 300, 130, 44, '义庄', True)
    for gx in (950, 1010): lantern_post(gx, 478, (236, 236, 226))
    road([(980, 480), (980, DY - 6), (900, DY - 6), (760, DY - 6)], 18)
    for cx, cy in ((860, 400), (940, 410), (1020, 404), (1100, 396), (880, 448)): coffin(cx, cy, cx in (940, 1100))
    # 义庄东边：几间民房和一小块菜地
    house(1190, 316, 70, 36); house(1290, 322, 60, 32); house(1180, 410, 64, 32)
    for r_ in range(4):
        yy = 420 + r_ * 14
        d.rectangle([1280, yy, 1420, yy + 8], fill=(70, 54, 50))
        for x in range(1284, 1418, 9): d.line([(x, yy + 1), (x + 2, yy - 3)], fill=(70, 130, 80)); d.point((x + 1, yy - 4), fill=(110, 170, 100))
    # 戏台广场：任府正门前，戏台在北，台口朝南，台前几排空板凳
    seats = []
    GX0, GX1, GY0, GY1 = 296, 566, 282, DY - 14
    d.rectangle([GX0, GY0, GX1, GY1], fill=(84, 72, 76))
    for x in range(GX0 + 6, GX1, 12): d.line([(x, GY0 + 2), (x, GY1 - 2)], fill=(76, 64, 70))
    for y in range(GY0 + 6, GY1, 12): d.line([(GX0 + 2, y), (GX1 - 2, y)], fill=(76, 64, 70))
    SC = (GX0 + GX1) // 2; sx0, sx1, sy0, sy1 = SC - 70, SC + 70, GY0 + 22, GY0 + 86
    d.rectangle([sx0 - 2, sy1 - 24, sx1 + 2, sy1 + 2], fill=K); d.rectangle([sx0, sy1 - 22, sx1, sy1], fill=(110, 70, 50))
    for x in range(sx0 + 4, sx1, 10): d.line([(x, sy1 - 21), (x, sy1 - 1)], fill=(90, 56, 40))
    d.rectangle([sx0, sy1 - 24, sx1, sy1 - 22], fill=(150, 100, 70))
    d.rectangle([sx0 + 8, sy0, sx1 - 8, sy1 - 24], fill=(40, 20, 28))
    for x in (sx0 + 4, sx1 - 8):
        d.rectangle([x - 1, sy0 - 4, x + 5, sy1 - 22], fill=K); d.rectangle([x, sy0 - 3, x + 4, sy1 - 23], fill=(170, 40, 36))
    d.rectangle([sx0 + 8, sy0, sx1 - 8, sy0 + 9], fill=(150, 30, 30))
    for x in range(sx0 + 10, sx1 - 8, 8): d.line([(x, sy0 + 9), (x + 4, sy0 + 15)], fill=(150, 30, 30), width=2)
    d.polygon([(sx0 - 14, sy0 - 2), (sx1 + 14, sy0 - 2), (sx1 - 2, sy0 - 26), (sx0 + 2, sy0 - 26)], fill=K)
    d.polygon([(sx0 - 11, sy0 - 4), (sx1 + 11, sy0 - 4), (sx1 - 4, sy0 - 24), (sx0 + 4, sy0 - 24)], fill=(52, 50, 72))
    d.line([(sx0 - 14, sy0 - 2), (sx0 - 20, sy0 - 10)], fill=K, width=3); d.line([(sx1 + 14, sy0 - 2), (sx1 + 20, sy0 - 10)], fill=K, width=3)
    d.rectangle([SC - 18, sy0 - 22, SC + 18, sy0 - 8], fill=K); d.rectangle([SC - 17, sy0 - 21, SC + 17, sy0 - 9], fill=(30, 26, 36))
    d.text((SC, sy0 - 15), '戏台', font=font(10), fill=(240, 200, 90), anchor='mm')
    for lx in (sx0 + 2, sx0 + 40, sx1 - 40, sx1 - 2):
        d.line([(lx, sy0 - 2), (lx, sy0 + 4)], fill=K); d.ellipse([lx - 5, sy0 + 3, lx + 5, sy0 + 15], fill=K); d.ellipse([lx - 4, sy0 + 4, lx + 4, sy0 + 14], fill=(220, 50, 40)); d.line([(lx - 4, sy0 + 9), (lx + 4, sy0 + 9)], fill=(240, 200, 90))
    block(sx0 - 2, sy1 - 26, sx1 + 2, sy1 + 2)
    # 台前几排空板凳
    for r_, y in enumerate(range(sy1 + 26, GY1 - 30, 26)):
        for x in range(SC - 64 + (r_ % 2) * 6, SC + 64, 34):
            d.rectangle([x - 1, y - 1, x + 27, y + 4], fill=K); d.rectangle([x, y, x + 26, y + 2], fill=(130, 84, 56)); d.rectangle([x, y + 2, x + 26, y + 3], fill=(100, 62, 40))
            d.rectangle([x + 2, y + 4, x + 3, y + 8], fill=K); d.rectangle([x + 23, y + 4, x + 24, y + 8], fill=K)
            seats.extend([(x + 7, y + 3), (x + 19, y + 3)])
    for x in (GX0 + 10, GX1 - 10):
        d.line([(x, GY0 + 16), (x, GY0 - 18)], fill=K, width=3); d.line([(x, GY0 + 15), (x, GY0 - 17)], fill=(120, 80, 50))
        d.ellipse([x - 6, GY0 - 18, x + 6, GY0 - 4], fill=K); d.ellipse([x - 5, GY0 - 17, x + 5, GY0 - 5], fill=(220, 50, 40)); d.line([(x - 5, GY0 - 11), (x + 5, GY0 - 11)], fill=(240, 200, 90))
        block(x - 2, GY0 + 12, x + 2, GY0 + 16)
    stage = (SC, sy1 - 22)
    # 牌坊：镇子南口
    pimg, pax, pay = paifang_img(); sprites['paifang'] = pimg
    PFY = DY + 160          # 牌坊挪到镇子南边的林荫道口
    objs.append(dict(k='house', x=740, y=PFY, img='paifang', ax=pax, ay=pay, rect=[688, PFY - 84, 792, PFY], burn=False))
    block(694, PFY - 10, 708, PFY + 1); block(772, PFY - 10, 786, PFY + 1)
    H2 = H + DY
    # ================= 地图往左扩：西边的青山、高坡上的老太爷坟、芭蕉林、戏台广场 =================
    W2 = W + EXT
    big = Image.new('RGBA', (W2, H2), (58, 42, 80, 255)); big.alpha_composite(im, (EXT, 0)); im = big; d = ImageDraw.Draw(im)
    blocks[:] = [(x0 + EXT, y0, x1 + EXT, y1) for x0, y0, x1, y1 in blocks]
    for o in objs:
        o['x'] += EXT
        if 'rect' in o: o['rect'] = [o['rect'][0] + EXT, o['rect'][1], o['rect'][2] + EXT, o['rect'][3]]
    graves[:] = [(x + EXT, y) for x, y in graves]; coffins[:] = [(x + EXT, y) for x, y in coffins]
    bats = (bats[0] + EXT, bats[1])
    random.seed(909)
    for _ in range(int(46000 * EXT / W)): im.putpixel((random.randrange(EXT + 4), random.randrange(H2)), random.choice([(70, 52, 96, 255), (46, 33, 64, 255), (64, 48, 88, 255)]))
    for _ in range(260):
        x, y = random.randrange(EXT), random.randrange(H2)
        for dx, hh in ((0, 2), (1, 3), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 86, 84))
    rx = lambda y: EXT + river_x(y - DY)          # 河中心（最终坐标）
    # --- 青山：西北一整片山，挡在镇子和坟山之间，坟背靠着它
    MT0, MT1 = 10, 250
    for layer, col in enumerate(((34, 56, 52), (44, 74, 64))):
        pts = [(0, MT1 + 20 - layer * 10)]
        for x in range(0, EXT + 150, 14):
            h = 120 + 50 * math.sin(x / 55 + layer) + 30 * math.sin(x / 23) - layer * 30
            pts.append((x, MT0 + 150 - h + layer * 40))
        pts += [(EXT + 150, MT1 + 20 - layer * 10)]
        d.polygon(pts, fill=K); d.polygon([(a, b + 2) for a, b in pts], fill=col)
    for _ in range(60):
        x = random.randrange(10, EXT + 140); y = random.randrange(MT0 + 70, MT1)
        d.line([(x, y), (x + 4, y - 3)], fill=(70, 110, 90))
    block(0, 0, EXT + 150, MT1 - 10)
    # --- 高坡：老太爷的坟在坡顶，背靠青山；南边是崖壁，东侧有石阶上去
    PX0, PX1, PY0, PY1 = 40, 400, MT1 - 10, MT1 + 170
    d.rectangle([PX0, PY0, PX1, PY1], fill=(78, 70, 74))
    for _ in range(2500): im.putpixel((random.randrange(PX0, PX1), random.randrange(PY0, PY1)), random.choice([(88, 80, 82, 255), (70, 62, 68, 255), (66, 92, 74, 255)]))
    face = 34
    d.rectangle([PX0, PY1, PX1, PY1 + face], fill=(52, 40, 50))
    for x in range(PX0, PX1, 7): d.line([(x, PY1 + 2), (x + random.randint(-2, 2), PY1 + face - 2)], fill=(40, 30, 40))
    d.rectangle([PX0, PY1 - 2, PX1, PY1 + 1], fill=(120, 116, 130))
    d.rectangle([PX1, PY0, PX1 + 8, PY1 + face], fill=(52, 40, 50)); d.rectangle([PX1 - 1, PY0, PX1 + 1, PY1], fill=(120, 116, 130))
    sx0, sx1 = 330, 372
    d.rectangle([sx0, PY1 - 4, sx1, PY1 + face + 2], fill=K)
    for k2, y in enumerate(range(PY1 - 3, PY1 + face + 1, 5)):
        d.rectangle([sx0 + 1, y, sx1 - 1, y + 4], fill=(150 - k2 * 6, 144 - k2 * 6, 168 - k2 * 6)); d.line([(sx0 + 1, y + 4), (sx1 - 1, y + 4)], fill=(80, 74, 98))
    block(PX0, PY1 - 2, sx0, PY1 + face); block(sx1, PY1 - 2, PX1 + 8, PY1 + face); block(PX1, PY0, PX1 + 8, PY1 + face)
    for x, y in ((70, PY0 + 30), (380, PY0 + 24), (60, PY1 - 30)): bgtree(x, y)
    TOMB = (210, (PY0 + PY1) // 2 - 6)
    grandpa(TOMB[0], TOMB[1])
    # --- 小土路：石桥西头往北，穿过芭蕉林直通坟坡石阶
    bxw = int(rx(BRIDGE[0] + DY) - RIVER_W / 2 - 30)
    TR = [(bxw, BRIDGE[0] + DY + 22), (bxw - 60, BRIDGE[0] + DY - 60), (300, PY1 + face + 60), ((sx0 + sx1) // 2, PY1 + face + 6)]
    road(TR, 22)
    def near_trail(x, y, r=26):
        for (x0, y0), (x1, y1) in zip(TR, TR[1:]):
            L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2; t = max(0, min(1, ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / L2))
            if (x - (x0 + (x1 - x0) * t)) ** 2 + (y - (y0 + (y1 - y0) * t)) ** 2 < r * r: return True
        return False
    # --- 芭蕉林：坡下一大片，一直到河边
    PL = []
    for _ in range(9000):
        if len(PL) >= 120: break
        x, y = random.randrange(30, int(rx(1000)) - 50), random.randrange(PY1 + face + 30, H2 - 40)
        if abs(x - rx(y)) < RIVER_W / 2 + 26 or (y > DY + 590 and y < DY + 650 and x > EXT - 40) or near_trail(x, y): continue
        if all((x - a) ** 2 + (y - b) ** 2 > 26 ** 2 for a, b in PL): PL.append((x, y))
    for v in range(3): sprites['plant%d' % v] = plant_img(v)
    for k2, (x, y) in enumerate(PL):
        objs.append(dict(k='plant', x=x, y=y, img='plant%d' % (k2 % 3), ax=28, ay=48)); block(x - 3, y - 3, x + 3, y + 1)
    # --- 左边界、下边界
    for y in range(MT1 + 10, H2, 26): bgtree(10 + random.randint(-4, 4), y)
    for x in range(10, EXT, 26): bgtree(x + random.randint(-4, 4), H2 - 4 - random.randint(0, 10))
    block(0, 0, 22, H2); block(0, H2 - 22, EXT, H2)
    cols, rows = W2 // CELL, H2 // CELL
    grid = bytearray(cols * rows)
    for x0, y0, x1, y1 in blocks:
        for cy in range(max(0, int(y0) // CELL), min(rows - 1, int(y1) // CELL) + 1):
            for cx in range(max(0, int(x0) // CELL), min(cols - 1, int(x1) // CELL) + 1):
                grid[cy * cols + cx] = 1
    river = [round(river_x(y - DY) + EXT, 1) for y in range(0, H2, 8)]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for v in grid), objs=objs,
                graves=graves, coffins=coffins, river=river, riverW=RIVER_W, pearl=[PEARL[0] + EXT, PEARL[1] + DY - 6], hb=[HB[0] + EXT, HB[1] + DY, HB[2] + EXT, HB[3] + DY], bridge=[BRIDGE[0] + DY, BRIDGE[1] + DY], bats=bats,
                road=[(x + EXT, y + DY) for x, y in ROAD], roadN=[(x + EXT, y + DY) for x, y in ROAD_N], w=W2, h=H2, townH=DY, extX=EXT, plants=PL, seats=[(x + EXT, y) for x, y in seats], yzGate=[980 + EXT, 494], renDoor=[430 + EXT, 160], citang=[740 + EXT, 104], vhome=[CHURCH[0] + EXT, CHURCH[1] + 42 + DY], tombPlat=[PX0, PY0, PX1, PY1], plantZone=[30, PY1 + 64, int(rx(1000)) - 30, H2 - 30], tomb=list(TOMB), plantain=[200, DY + 900], stage=[stage[0] + EXT, stage[1]], loop=[LOOP[0] + DY, LOOP[1] + DY], yamen=[644 + EXT, 232], paifang=[740 + EXT, DY + 160],
                yz=[[860 + EXT, 400, 0], [940 + EXT, 410, 1], [1020 + EXT, 404, 0], [1100 + EXT, 396, 1], [880 + EXT, 448, 0]], town=[30, 30, W2 - 10, DY])
    return im, sprites, data


if __name__ == '__main__':
    im, sprites, data = build()
    out = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        s = sprites[o['img']]; out.alpha_composite(s, (o['x'] - o['ax'], o['y'] - o['ay']))
    out.convert('RGB').save('map2.png'); print(len(data['objs']), len(data['graves']), len(data['coffins']))
