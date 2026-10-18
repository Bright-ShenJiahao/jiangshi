"""第二章·日本：大正年间的深山神社村（夜）。开阔的中央广场 + 一条通向神社的参道，
西边竹林、东边墓地、南边茅草屋村落和水田，西南角一个池塘和太鼓桥。
build() 返回 (bg图, sprites字典, data字典)，接口和 map_gen5.build 一致。"""
import math, random
from PIL import Image, ImageDraw

K = (24, 14, 30)
W, H = 2000, 1500
CELL = 8

# ---------------- 调色板（夜里偏蓝绿） ----------------
GROUND = [(38, 50, 66), (34, 46, 62), (42, 56, 70)]
PATH = (118, 108, 110); PATH_D = (96, 88, 94)
RED, RED_D, RED_L = (190, 52, 46), (128, 34, 36), (226, 96, 76)
STONE, STONE_D, STONE_L = (128, 126, 140), (88, 86, 104), (166, 164, 176)
WOOD, WOOD_D = (96, 66, 50), (64, 44, 40)
STRAW, STRAW_D, STRAW_L = (128, 104, 62), (92, 72, 46), (156, 130, 78)
WALL, WALL_D = (176, 160, 132), (132, 116, 100)
GLOW = (250, 206, 110)
PINK, PINK_D, PINK_L = (214, 142, 172), (168, 96, 130), (240, 190, 206)
BAM, BAM_D, BAM_L = (66, 122, 86), (40, 82, 64), (112, 168, 112)


def canvas(w, h):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def box(d, x0, y0, x1, y1, fill, line=K):
    d.rectangle([x0, y0, x1, y1], fill=line); d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=fill)


def shadow(d, cx, cy, rx, ry=None):
    d.ellipse([cx - rx, cy - (ry or rx // 3), cx + rx, cy + (ry or rx // 3)], fill=(20, 26, 40, 140))


# ---------------- 物件精灵：返回 (图, 锚点x, 锚点y)，锚点 = 脚底中心 ----------------
def torii(big=False):
    w, h = (92, 80) if big else (68, 60)
    im, d = canvas(w, h); cx = w // 2; px = 14 if big else 11; pw = 4 if big else 3
    shadow(d, cx, h - 3, w // 2 - 2)
    for x in (cx - px - 14 + (6 if not big else 0), cx + px + 14 - (6 if not big else 0)):
        pass
    xs = (cx - (w // 2 - 12), cx + (w // 2 - 12))
    for x in xs:
        box(d, x - pw, 16, x + pw, h - 6, RED); d.line([(x - pw + 1, 17), (x - pw + 1, h - 7)], fill=RED_L)
        d.line([(x + pw - 1, 17), (x + pw - 1, h - 7)], fill=RED_D)
        box(d, x - pw - 2, h - 8, x + pw + 2, h - 3, STONE_D)
        d.line([(x - pw, h - 7), (x + pw, h - 7)], fill=STONE_L)
    # 贯（下横梁）
    box(d, xs[0] - pw, 26, xs[1] + pw, 31, RED)
    d.line([(xs[0], 27), (xs[1], 27)], fill=RED_L)
    # 笠木 + 岛木
    d.polygon([(2, 14), (w - 3, 14), (w - 8, 20), (8, 20)], fill=K)
    d.polygon([(4, 14), (w - 5, 14), (w - 9, 19), (9, 19)], fill=(40, 30, 38))
    d.polygon([(0, 8), (w - 1, 8), (w - 3, 14), (2, 14)], fill=K)
    d.polygon([(2, 9), (w - 3, 9), (w - 5, 13), (4, 13)], fill=(52, 40, 48))
    d.line([(8, 20), (w - 9, 20)], fill=K)
    box(d, cx - 6, 20, cx + 6, 28, (40, 36, 44))                      # 额束
    d.rectangle([cx - 4, 22, cx + 4, 26], fill=(196, 170, 96))
    return im, cx, h - 3


def lantern_stone(lit=True):
    im, d = canvas(20, 38); cx = 10
    shadow(d, cx, 35, 8)
    box(d, cx - 6, 30, cx + 6, 35, STONE_D); d.line([(cx - 5, 31), (cx + 5, 31)], fill=STONE_L)
    box(d, cx - 2, 20, cx + 2, 30, STONE); d.line([(cx - 1, 21), (cx - 1, 29)], fill=STONE_L)
    box(d, cx - 6, 18, cx + 6, 21, STONE_L)
    box(d, cx - 5, 9, cx + 5, 18, STONE_D)
    d.rectangle([cx - 3, 11, cx + 3, 16], fill=GLOW if lit else (30, 24, 34))
    d.line([(cx, 11), (cx, 16)], fill=(150, 110, 60))
    d.polygon([(cx - 9, 9), (cx + 9, 9), (cx + 5, 3), (cx - 5, 3)], fill=K)
    d.polygon([(cx - 8, 8), (cx + 8, 8), (cx + 4, 4), (cx - 4, 4)], fill=STONE)
    d.line([(cx - 4, 4), (cx + 4, 4)], fill=STONE_L)
    box(d, cx - 2, 0, cx + 2, 3, STONE_L)
    return im, cx, 35


def sakura(var=0):
    r = random.Random(var + 7)
    im, d = canvas(78, 84); cx, by = 39, 80
    shadow(d, cx, by - 1, 22)
    d.polygon([(cx - 6, by), (cx - 3, by - 34), (cx + 3, by - 34), (cx + 6, by)], fill=K)
    d.polygon([(cx - 4, by - 1), (cx - 2, by - 33), (cx + 2, by - 33), (cx + 4, by - 1)], fill=(70, 50, 54))
    d.line([(cx, by - 30), (cx - 16, by - 46)], fill=K, width=4); d.line([(cx, by - 28), (cx + 17, by - 44)], fill=K, width=4)
    blobs = [(0, -58, 26), (-20, -48, 17), (20, -47, 18), (-8, -72, 15), (11, -70, 15)]
    for ox, oy, rr in blobs: d.ellipse([cx + ox - rr - 1, by + oy - rr - 1, cx + ox + rr + 1, by + oy + rr + 1], fill=K)
    for i, (ox, oy, rr) in enumerate(blobs): d.ellipse([cx + ox - rr, by + oy - rr, cx + ox + rr, by + oy + rr], fill=PINK_D if i % 2 else PINK)
    for _ in range(60):
        x, y = cx + r.randint(-30, 30), by + r.randint(-80, -34)
        if im.getpixel((x, y))[3] and im.getpixel((x, y))[:3] != K: d.point((x, y), fill=r.choice([PINK_L, PINK, PINK_D]))
    return im, cx, by


def bamboo(var=0):
    r = random.Random(var * 5 + 3)
    im, d = canvas(40, 92); by = 88
    shadow(d, 20, by, 16)
    for sx, hh in [(10, 72), (18, 84), (26, 76), (33, 64)]:
        sx += r.randint(-1, 1)
        d.rectangle([sx - 2, by - hh, sx + 2, by], fill=K); d.rectangle([sx - 1, by - hh, sx + 1, by], fill=BAM)
        d.line([(sx - 1, by - hh), (sx - 1, by)], fill=BAM_L)
        for y in range(by - 8, by - hh, -11): d.line([(sx - 2, y), (sx + 2, y)], fill=BAM_D)
        for k in range(3):
            y = by - hh + 4 + k * 8; s = 1 if (k + sx) % 2 else -1
            d.line([(sx, y), (sx + s * 9, y - 5)], fill=K, width=3); d.line([(sx, y), (sx + s * 8, y - 5)], fill=BAM_L, width=1)
    return im, 20, by


def willow():
    im, d = canvas(70, 82); cx, by = 35, 78
    shadow(d, cx, by - 1, 18)
    d.rectangle([cx - 4, by - 36, cx + 4, by], fill=K); d.rectangle([cx - 3, by - 36, cx + 3, by], fill=(66, 54, 52))
    for ox, oy, rr in [(0, -44, 20), (-16, -38, 12), (16, -38, 12)]: d.ellipse([cx + ox - rr - 1, by + oy - rr - 1, cx + ox + rr + 1, by + oy + rr + 1], fill=K)
    for ox, oy, rr in [(0, -44, 20), (-16, -38, 12), (16, -38, 12)]: d.ellipse([cx + ox - rr, by + oy - rr, cx + ox + rr, by + oy + rr], fill=(44, 92, 78))
    for x in range(cx - 30, cx + 31, 5):
        ln = 26 + int(10 * math.sin(x * 0.7)); top = by - 44 + int(abs(x - cx) * 0.35)
        d.line([(x, top), (x + (1 if x % 2 else -1), top + ln)], fill=K, width=3); d.line([(x, top), (x + (1 if x % 2 else -1), top + ln)], fill=(76, 132, 104), width=1)
    return im, cx, by


def gravestone(var=0):
    hh = 22 + (var % 3) * 4
    im, d = canvas(20, hh + 12); cx = 10; by = hh + 10
    shadow(d, cx, by, 9)
    box(d, cx - 8, by - 5, cx + 8, by, STONE_D); box(d, cx - 6, by - 9, cx + 6, by - 4, STONE)
    box(d, cx - 5, by - hh, cx + 5, by - 8, STONE); d.line([(cx - 4, by - hh + 1), (cx - 4, by - 9)], fill=STONE_L)
    d.line([(cx + 4, by - hh + 1), (cx + 4, by - 9)], fill=STONE_D)
    d.polygon([(cx - 5, by - hh), (cx + 5, by - hh), (cx, by - hh - 4)], fill=K); d.polygon([(cx - 4, by - hh), (cx + 4, by - hh), (cx, by - hh - 3)], fill=STONE_L)
    for y in range(by - hh + 4, by - 12, 4): d.line([(cx, y), (cx, y + 1)], fill=STONE_D)      # 刻字
    if var % 2:
        d.rectangle([cx + 6, by - 14, cx + 9, by - 10], fill=(220, 190, 90)); d.point((cx + 7, by - 15), fill=(255, 240, 160))  # 供蜡烛
    return im, cx, by


def sotoba():
    im, d = canvas(14, 44); cx = 7; by = 42
    shadow(d, cx, by, 6)
    d.rectangle([cx - 3, 2, cx + 3, by], fill=K); d.rectangle([cx - 2, 3, cx + 2, by - 1], fill=(190, 172, 130))
    for y in (6, 10, 14, 18): d.line([(cx - 3, y), (cx + 3, y)], fill=K)
    for y in range(22, by - 4, 4): d.line([(cx, y), (cx, y + 1)], fill=WOOD_D)
    return im, cx, by


def jizo():
    im, d = canvas(20, 30); cx = 10; by = 28
    shadow(d, cx, by, 8)
    box(d, cx - 7, by - 4, cx + 7, by, STONE_D)
    box(d, cx - 4, by - 14, cx + 4, by - 4, STONE)
    d.rectangle([cx - 3, by - 11, cx + 3, by - 8], fill=RED); d.line([(cx - 3, by - 11), (cx + 3, by - 11)], fill=RED_L)  # 红围兜
    d.ellipse([cx - 5, by - 24, cx + 5, by - 13], fill=K); d.ellipse([cx - 4, by - 23, cx + 4, by - 14], fill=STONE_L)
    d.rectangle([cx - 5, by - 27, cx + 5, by - 22], fill=RED_D); d.rectangle([cx - 4, by - 26, cx + 4, by - 23], fill=RED)  # 红帽子
    d.point((cx - 2, by - 19), fill=K); d.point((cx + 2, by - 19), fill=K)
    return im, cx, by


def gorinto():
    im, d = canvas(22, 44); cx = 11; by = 42
    shadow(d, cx, by, 10)
    box(d, cx - 8, by - 6, cx + 8, by, STONE_D)
    box(d, cx - 6, by - 14, cx + 6, by - 6, STONE)
    d.ellipse([cx - 8, by - 24, cx + 8, by - 12], fill=K); d.ellipse([cx - 7, by - 23, cx + 7, by - 13], fill=STONE_L)
    d.polygon([(cx - 8, by - 24), (cx + 8, by - 24), (cx, by - 32)], fill=K); d.polygon([(cx - 6, by - 25), (cx + 6, by - 25), (cx, by - 30)], fill=STONE)
    d.ellipse([cx - 3, by - 40, cx + 3, by - 32], fill=K); d.ellipse([cx - 2, by - 39, cx + 2, by - 33], fill=STONE_L)
    return im, cx, by


def komainu(flip=False):
    im, d = canvas(26, 30); cx = 13; by = 28
    shadow(d, cx, by, 10)
    box(d, cx - 10, by - 6, cx + 10, by, STONE_D)
    box(d, cx - 6, by - 20, cx + 5, by - 6, STONE)
    d.ellipse([cx - 7, by - 29, cx + 6, by - 17], fill=K); d.ellipse([cx - 6, by - 28, cx + 5, by - 18], fill=STONE_L)
    d.rectangle([cx - 4, by - 23, cx - 2, by - 21], fill=K); d.rectangle([cx + 1, by - 23, cx + 3, by - 21], fill=K)
    d.polygon([(cx + 4, by - 20), (cx + 11, by - 10), (cx + 4, by - 10)], fill=STONE_D)       # 尾
    return (im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im), cx, by


def haiden():
    """神社拝殿：石台阶、红柱、双层黑瓦屋顶、注连绳、赛钱箱、灯笼"""
    w, h = 196, 150
    im, d = canvas(w, h); cx = w // 2
    shadow(d, cx, h - 4, 88, 8)
    for i in range(4):                                                      # 台阶
        box(d, cx - 34 - i * 4, h - 6 - i * 5, cx + 34 + i * 4, h - 1 - i * 5, STONE if i % 2 else STONE_L)
    bx0, bx1, by0, by1 = cx - 62, cx + 62, 60, h - 28
    box(d, bx0 - 6, by1 - 4, bx1 + 6, by1 + 3, STONE_D)                       # 基坛
    box(d, bx0, by0, bx1, by1 - 4, (60, 44, 46))
    for x in range(bx0 + 4, bx1, 12): d.line([(x, by0 + 2), (x, by1 - 6)], fill=(46, 34, 40))
    box(d, cx - 22, by0 + 16, cx + 22, by1 - 4, (30, 22, 30))                 # 正面暗处
    for x in (cx - 22, cx + 22): box(d, x - 3, by0 + 10, x + 3, by1 - 4, RED)
    for x in (bx0 + 3, bx1 - 3): box(d, x - 4, by0 + 6, x + 4, by1 - 2, RED); d.line([(x - 3, by0 + 7), (x - 3, by1 - 3)], fill=RED_L)
    box(d, bx0 - 2, by0 + 4, bx1 + 2, by0 + 12, RED)                          # 横梁
    for x in range(bx0 + 6, bx1, 14): d.rectangle([x, by0 + 5, x + 2, by0 + 10], fill=(220, 180, 90))
    # 注连绳
    d.line([(cx - 20, by0 + 22), (cx, by0 + 27), (cx + 20, by0 + 22)], fill=(214, 200, 150), width=2)
    for x in (cx - 12, cx, cx + 12): d.line([(x, by0 + 24), (x, by0 + 31)], fill=(240, 236, 220))
    # 赛钱箱
    box(d, cx - 12, by1 - 12, cx + 12, by1 - 4, WOOD); d.line([(cx - 10, by1 - 11), (cx + 10, by1 - 11)], fill=(30, 22, 28), width=1)
    for x in range(cx - 10, cx + 11, 3): d.line([(x, by1 - 10), (x, by1 - 6)], fill=WOOD_D)
    # 屋顶：唐破风 + 两层瓦
    d.polygon([(2, by0 + 6), (w - 3, by0 + 6), (w - 24, by0 - 20), (24, by0 - 20)], fill=K)
    d.polygon([(6, by0 + 4), (w - 7, by0 + 4), (w - 26, by0 - 18), (26, by0 - 18)], fill=(46, 44, 62))
    for x in range(14, w - 10, 6): d.line([(x, by0 + 3), (x + (cx - x) // 4, by0 - 17)], fill=(66, 62, 86))
    d.polygon([(26, by0 - 18), (w - 27, by0 - 18), (w - 50, by0 - 44), (50, by0 - 44)], fill=K)
    d.polygon([(29, by0 - 19), (w - 30, by0 - 19), (w - 52, by0 - 42), (52, by0 - 42)], fill=(40, 38, 58))
    for x in range(36, w - 30, 6): d.line([(x, by0 - 19), (x + (cx - x) // 4, by0 - 42)], fill=(60, 56, 80))
    d.line([(52, by0 - 44), (w - 53, by0 - 44)], fill=(150, 130, 70), width=2)   # 栋
    for x in (46, w - 47): d.polygon([(x - 3, by0 - 44), (x + 3, by0 - 44), (x, by0 - 52)], fill=(190, 160, 80))  # 鸱尾
    for x in (cx - 50, cx + 50):                                              # 吊灯笼
        d.line([(x, by0 + 12), (x, by0 + 18)], fill=K); box(d, x - 5, by0 + 18, x + 5, by0 + 32, (230, 120, 70)); d.line([(x - 4, by0 + 25), (x + 4, by0 + 25)], fill=(250, 190, 110))
    return im, cx, h - 3


def thatched_house(w=96, var=0):
    """茅草屋（合掌造风格）：陡峭的大茅草屋顶，白墙木格，拉门透出灯光"""
    r = random.Random(var + 11)
    bh = 38; rh = 54
    im, d = canvas(w + 20, bh + rh + 10); x0, ytop = 10, 2
    shadow(d, x0 + w // 2, bh + rh + 6, w // 2 + 6, 7)
    yb = ytop + rh                                                         # 屋檐线
    # 墙
    box(d, x0 + 4, yb, x0 + w - 4, yb + bh, WALL)
    d.rectangle([x0 + 5, yb + bh - 6, x0 + w - 5, yb + bh - 1], fill=WALL_D)
    for x in range(x0 + 14, x0 + w - 8, 14): d.line([(x, yb + 1), (x, yb + bh - 7)], fill=WOOD_D)     # 木柱
    d.line([(x0 + 5, yb + 14), (x0 + w - 5, yb + 14)], fill=WOOD_D)
    for i in range(2):                                                      # 拉门
        sx = x0 + 18 + i * (w - 62) // 1
        box(d, sx, yb + 18, sx + 26, yb + bh - 8, GLOW if (i + var) % 2 == 0 else (200, 168, 100))
        for gx in range(sx + 6, sx + 26, 6): d.line([(gx, yb + 19), (gx, yb + bh - 9)], fill=WOOD_D)
        for gy in range(yb + 24, yb + bh - 8, 6): d.line([(sx + 1, gy), (sx + 25, gy)], fill=WOOD_D)
    # 屋顶：厚茅草
    d.polygon([(x0 - 8, yb + 6), (x0 + w + 8, yb + 6), (x0 + w // 2 + 12, ytop), (x0 + w // 2 - 12, ytop)], fill=K)
    d.polygon([(x0 - 6, yb + 4), (x0 + w + 6, yb + 4), (x0 + w // 2 + 10, ytop + 2), (x0 + w // 2 - 10, ytop + 2)], fill=STRAW)
    for y in range(ytop + 6, yb + 3, 5):
        t = (y - ytop) / rh
        xa, xb = x0 + w // 2 - 10 - t * (w // 2 - 4 - 0), x0 + w // 2 + 10 + t * (w // 2 - 4)
        d.line([(xa + 2, y), (xb - 2, y)], fill=STRAW_D)
    for _ in range(50):
        y = r.randint(ytop + 4, yb + 2); t = (y - ytop) / rh
        xa, xb = int(x0 + w // 2 - 10 - t * (w // 2 - 4)), int(x0 + w // 2 + 10 + t * (w // 2 - 4))
        d.point((r.randint(xa + 2, xb - 2), y), fill=r.choice([STRAW_L, STRAW_D]))
    d.line([(x0 + w // 2 - 10, ytop + 2), (x0 + w // 2 + 10, ytop + 2)], fill=STRAW_L, width=2)
    d.line([(x0 + w // 2 - 6, ytop - 2), (x0 + w // 2 + 6, ytop - 2)], fill=K, width=2)
    d.line([(x0 - 6, yb + 4), (x0 + w + 6, yb + 4)], fill=K)
    # 檐下阴影
    d.rectangle([x0 - 4, yb + 5, x0 + w + 4, yb + 8], fill=(40, 32, 38))
    return im, x0 + w // 2, yb + bh + 4


def chochin(on=True):
    im, d = canvas(14, 26); cx = 7
    d.line([(cx, 0), (cx, 4)], fill=K)
    d.ellipse([cx - 6, 4, cx + 6, 22], fill=K); d.ellipse([cx - 5, 5, cx + 5, 21], fill=(226, 90, 70) if on else (90, 50, 50))
    for y in (9, 13, 17): d.line([(cx - 4, y), (cx + 4, y)], fill=(150, 52, 48))
    d.rectangle([cx - 3, 3, cx + 3, 5], fill=K); d.rectangle([cx - 3, 21, cx + 3, 23], fill=K)
    return im, cx, 24


def fox_statue():
    im, d = canvas(24, 34); cx = 12; by = 32
    shadow(d, cx, by, 9)
    box(d, cx - 8, by - 6, cx + 8, by, STONE_D)
    box(d, cx - 5, by - 18, cx + 4, by - 6, STONE)
    d.polygon([(cx - 6, by - 18), (cx - 3, by - 30), (cx, by - 20), (cx + 3, by - 30), (cx + 6, by - 18)], fill=K)
    d.polygon([(cx - 5, by - 19), (cx - 3, by - 28), (cx, by - 21), (cx + 3, by - 28), (cx + 5, by - 19)], fill=STONE_L)
    d.rectangle([cx - 3, by - 16, cx + 3, by - 13], fill=RED)                          # 红围兜
    d.polygon([(cx + 4, by - 14), (cx + 12, by - 8), (cx + 4, by - 6)], fill=STONE_D)  # 尾
    return im, cx, by


def rock(var=0):
    r = random.Random(var)
    im, d = canvas(34, 24); cx = 17; by = 22
    shadow(d, cx, by, 14)
    pts = [(cx - 14, by), (cx - 12, by - 10), (cx - 4, by - 16 - r.randint(0, 3)), (cx + 6, by - 14), (cx + 14, by - 6), (cx + 13, by)]
    d.polygon(pts, fill=K); d.polygon([(x + (1 if x < cx else -1), y + (1 if y < by else 0)) for x, y in pts], fill=STONE_D)
    d.line([(cx - 8, by - 9), (cx, by - 14), (cx + 6, by - 12)], fill=STONE)
    return im, cx, by


def cedar():
    """杉：高大的深绿锥形树"""
    im, d = canvas(56, 122); cx, by = 28, 118
    shadow(d, cx, by - 1, 18)
    d.rectangle([cx - 4, by - 18, cx + 4, by], fill=K); d.rectangle([cx - 3, by - 18, cx + 3, by], fill=(62, 46, 46))
    for i, (yy, ww) in enumerate([(by - 14, 24), (by - 34, 21), (by - 54, 18), (by - 74, 14), (by - 94, 9)]):
        d.polygon([(cx - ww - 1, yy + 1), (cx + ww + 1, yy + 1), (cx, yy - 28)], fill=K)
        d.polygon([(cx - ww, yy), (cx + ww, yy), (cx, yy - 26)], fill=(28, 58, 58) if i % 2 else (34, 70, 66))
        d.polygon([(cx - ww, yy), (cx - ww // 2, yy), (cx, yy - 26)], fill=(22, 46, 50))
    return im, cx, by


def chozuya():
    """手水舎：小亭子 + 石水盆"""
    im, d = canvas(66, 58); cx, by = 33, 56
    shadow(d, cx, by - 1, 28, 6)
    for x in (cx - 24, cx + 24): box(d, x - 3, 20, x + 3, by - 4, WOOD)
    d.polygon([(2, 22), (w := 64, 22), (56, 6), (10, 6)], fill=K); d.polygon([(5, 21), (61, 21), (55, 8), (11, 8)], fill=(50, 46, 66))
    for x in range(10, 58, 5): d.line([(x, 20), (x + (33 - x) // 5, 9)], fill=(70, 66, 90))
    box(d, cx - 18, by - 14, cx + 18, by - 4, STONE); d.rectangle([cx - 15, by - 13, cx + 15, by - 9], fill=(36, 70, 110))
    d.line([(cx - 14, by - 12), (cx + 6, by - 12)], fill=(90, 150, 190))
    d.line([(cx + 12, by - 22), (cx + 12, by - 12)], fill=WOOD_D); d.rectangle([cx + 10, by - 24, cx + 20, by - 22], fill=WOOD)  # 竹勺
    return im, cx, by


def scarecrow():
    im, d = canvas(30, 50); cx, by = 15, 48
    shadow(d, cx, by, 7)
    d.rectangle([cx - 1, 14, cx + 1, by], fill=K); d.rectangle([cx, 15, cx, by - 1], fill=WOOD)
    d.line([(cx - 13, 22), (cx + 13, 22)], fill=K, width=3); d.line([(cx - 12, 22), (cx + 12, 22)], fill=WOOD, width=1)
    d.polygon([(cx - 9, 22), (cx + 9, 22), (cx + 6, 38), (cx - 6, 38)], fill=K); d.polygon([(cx - 8, 23), (cx + 8, 23), (cx + 5, 37), (cx - 5, 37)], fill=(120, 92, 70))
    d.ellipse([cx - 6, 7, cx + 6, 19], fill=K); d.ellipse([cx - 5, 8, cx + 5, 18], fill=(196, 170, 120))
    d.point((cx - 2, 12), fill=K); d.point((cx + 2, 12), fill=K); d.line([(cx - 2, 15), (cx + 2, 15)], fill=K)
    d.polygon([(cx - 10, 9), (cx + 10, 9), (cx + 4, 1), (cx - 4, 1)], fill=K); d.polygon([(cx - 8, 8), (cx + 8, 8), (cx + 3, 2), (cx - 3, 2)], fill=STRAW)
    for x in (cx - 12, cx + 12): d.line([(x, 23), (x + (-1 if x < cx else 1), 31)], fill=STRAW, width=2)
    return im, cx, by


def haystack():
    im, d = canvas(34, 34); cx, by = 17, 32
    shadow(d, cx, by, 13)
    d.polygon([(cx - 13, by), (cx - 8, by - 20), (cx, by - 30), (cx + 8, by - 20), (cx + 13, by)], fill=K)
    d.polygon([(cx - 11, by - 1), (cx - 7, by - 19), (cx, by - 28), (cx + 7, by - 19), (cx + 11, by - 1)], fill=STRAW)
    for y in range(by - 24, by - 2, 5): d.line([(cx - 10 + (by - y) // 6 * 0, y), (cx + 10, y + 2)], fill=STRAW_D)
    d.line([(cx - 10, by - 12), (cx + 10, by - 12)], fill=WOOD_D, width=2)
    return im, cx, by


def hokora():
    """池中小岛上的弁天社（小祠）"""
    im, d = canvas(56, 62); cx, by = 28, 60
    shadow(d, cx, by - 1, 22, 5)
    box(d, cx - 18, by - 8, cx + 18, by - 1, STONE_D)
    box(d, cx - 13, by - 30, cx + 13, by - 8, (60, 44, 46))
    for x in (cx - 13, cx + 13): box(d, x - 2, by - 30, x + 2, by - 8, RED)
    box(d, cx - 7, by - 24, cx + 7, by - 10, (240, 200, 110)); d.line([(cx, by - 24), (cx, by - 10)], fill=WOOD_D)
    d.polygon([(cx - 24, by - 28), (cx + 24, by - 28), (cx + 10, by - 48), (cx - 10, by - 48)], fill=K)
    d.polygon([(cx - 22, by - 29), (cx + 22, by - 29), (cx + 9, by - 46), (cx - 9, by - 46)], fill=(46, 44, 62))
    d.line([(cx - 9, by - 46), (cx + 9, by - 46)], fill=(190, 160, 80), width=2)
    return im, cx, by


SPRITE_FUNCS = {
    'jp_haiden2': hokora,
    'jp_cedar': cedar, 'jp_chozu': chozuya, 'jp_scare': scarecrow, 'jp_hay': haystack,
    'jp_torii': lambda: torii(False), 'jp_toriiB': lambda: torii(True), 'jp_lantern': lantern_stone,
    'jp_sakura0': lambda: sakura(0), 'jp_sakura1': lambda: sakura(1), 'jp_bamboo0': lambda: bamboo(0), 'jp_bamboo1': lambda: bamboo(1),
    'jp_willow': willow, 'jp_grave0': lambda: gravestone(0), 'jp_grave1': lambda: gravestone(1), 'jp_grave2': lambda: gravestone(2),
    'jp_sotoba': sotoba, 'jp_jizo': jizo, 'jp_gorinto': gorinto, 'jp_komaL': komainu, 'jp_komaR': lambda: komainu(True),
    'jp_haiden': haiden, 'jp_house0': lambda: thatched_house(96, 0), 'jp_house1': lambda: thatched_house(80, 1), 'jp_house2': lambda: thatched_house(112, 2),
    'jp_chochin': chochin, 'jp_fox': fox_statue, 'jp_rock0': lambda: rock(0), 'jp_rock1': lambda: rock(1),
}


# ---------------- 地面与地形 ----------------
def road(d, pts, w=30, col=PATH):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(math.hypot(x1 - x0, y1 - y0) / 3) + 1
        for i in range(n + 1):
            x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
            d.ellipse([x - w / 2 - 2, y - w / 2 - 2, x + w / 2 + 2, y + w / 2 + 2], fill=PATH_D)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(math.hypot(x1 - x0, y1 - y0) / 3) + 1
        for i in range(n + 1):
            x, y = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)


def build(seed=21, with_objs=True):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), (36, 48, 64, 255)); d = ImageDraw.Draw(im)
    blocks = []                                           # 碰撞矩形
    for _ in range(90000): im.putpixel((random.randrange(W), random.randrange(H)), random.choice(GROUND) + (255,))
    for _ in range(1400):
        x, y = random.randrange(W), random.randrange(H)
        for dx, hh in ((0, 2), (1, 4), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 84, 82))

    # --- 北：远山与神社山丘 ---
    d.rectangle([0, 0, W, 190], fill=(26, 38, 52))
    for k, col in enumerate([(30, 44, 60), (24, 36, 50), (20, 30, 44)]):
        pts = [(0, 190)]
        for x in range(0, W + 40, 40): pts.append((x, 120 - k * 18 + int(40 * math.sin(x / 190 + k * 2) + 20 * math.sin(x / 73 + k))))
        pts.append((W, 190)); d.polygon(pts, fill=col)
    d.rectangle([0, 188, W, 196], fill=K)
    # 神社台地（石垣）
    SX0, SX1, SY0, SY1 = 700, 1300, 196, 470
    d.rectangle([SX0, SY0, SX1, SY1], fill=(52, 62, 76))
    for _ in range(14000): im.putpixel((random.randrange(SX0, SX1), random.randrange(SY0, SY1)), random.choice([(60, 72, 86, 255), (46, 56, 70, 255), (54, 70, 76, 255)]))
    d.rectangle([SX0, SY1, SX1, SY1 + 26], fill=K); d.rectangle([SX0 + 2, SY1 + 1, SX1 - 2, SY1 + 24], fill=STONE_D)
    for y in (SY1 + 8, SY1 + 16):
        d.line([(SX0 + 2, y), (SX1 - 2, y)], fill=(70, 68, 86))
        for x in range(SX0 + (6 if y == SY1 + 8 else 14), SX1, 18): d.line([(x, y - 7 if y == SY1 + 16 else y), (x, y + 7 if y == SY1 + 8 else y)], fill=(70, 68, 86))
    blocks.append((SX0, SY0 - 20, SX1, SY1 + 26))
    GATE = (940, 1060)                                    # 石阶缺口（参道上去）
    d.rectangle([GATE[0], SY1 - 2, GATE[1], SY1 + 28], fill=PATH_D)
    for i in range(6): d.rectangle([GATE[0] + i * 2, SY1 + i * 5, GATE[1] - i * 2, SY1 + i * 5 + 4], fill=PATH if i % 2 else (136, 126, 128))
    blocks.remove((SX0, SY0 - 20, SX1, SY1 + 26))
    blocks.append((SX0, SY0 - 20, GATE[0] - 2, SY1 + 26)); blocks.append((GATE[1] + 2, SY0 - 20, SX1, SY1 + 26))
    # 台地铺石
    d.rectangle([968, 440, 1032, SY1], fill=PATH_D); d.rectangle([972, 440, 1028, SY1], fill=PATH)
    # --- 参道（从南到神社） ---
    SPINE = [(1000, 1420), (1000, 1100), (1000, 700), (1000, SY1)]
    road(d, SPINE, 64)
    # 中央广场（圆形）
    d.ellipse([820, 640, 1180, 900], fill=PATH_D); d.ellipse([824, 644, 1176, 896], fill=PATH)
    for _ in range(600):
        a, r = random.random() * 6.283, random.random() ** 0.5
        im.putpixel((int(1000 + 170 * r * math.cos(a)), int(770 + 120 * r * math.sin(a))), random.choice([(104, 96, 100, 255), (130, 120, 120, 255)]))
    d.ellipse([990 - 3, 760, 1010 + 3, 780], fill=K)
    # 东西两条岔路
    road(d, [(1000, 790), (1300, 800), (1500, 700), (1640, 560)], 40)       # → 墓地
    road(d, [(1000, 790), (700, 800), (520, 740), (380, 620)], 40)          # → 竹林
    road(d, [(1000, 1150), (1250, 1150), (1450, 1130)], 40)                 # → 村落
    road(d, [(1000, 1150), (800, 1170), (640, 1160), (590, 1146)], 40)                   # → 池塘/桥

    # --- 西北：竹林地块（暗绿地面）---
    BX0, BY0, BX1, BY1 = 70, 280, 640, 880
    for _ in range(26000):
        x, y = random.randrange(BX0, BX1), random.randrange(BY0, BY1)
        if (x - 360) ** 2 / 300 ** 2 + (y - 580) ** 2 / 310 ** 2 < 1 and im.getpixel((x, y))[:3] in [(38, 50, 66), (34, 46, 62), (42, 56, 70)]: im.putpixel((x, y), random.choice([(30, 52, 56, 255), (26, 44, 52, 255), (36, 62, 62, 255)]))
    # --- 东北：墓地地块（石板/荒草）---
    for _ in range(26000):
        x, y = random.randrange(1380, 1920), random.randrange(260, 860)
        if (x - 1650) ** 2 / 270 ** 2 + (y - 560) ** 2 / 300 ** 2 < 1 and im.getpixel((x, y))[:3] in [(38, 50, 66), (34, 46, 62), (42, 56, 70)]: im.putpixel((x, y), random.choice([(44, 50, 70, 255), (38, 42, 62, 255), (50, 58, 76, 255)]))

    # --- 西南：池塘 + 太鼓桥 ---
    PX, PY, PRX, PRY = 330, 1140, 250, 150
    d.ellipse([PX - PRX - 4, PY - PRY - 4, PX + PRX + 4, PY + PRY + 4], fill=K)
    d.ellipse([PX - PRX, PY - PRY, PX + PRX, PY + PRY], fill=(24, 44, 78))
    for _ in range(5000):
        a, r = random.random() * 6.283, random.random() ** 0.5
        im.putpixel((int(PX + PRX * r * math.cos(a)), int(PY + PRY * r * math.sin(a))), random.choice([(32, 58, 98, 255), (20, 38, 70, 255), (44, 78, 120, 255)]))
    for _ in range(26):
        a, r = random.random() * 6.283, random.random() ** 0.5 * 0.85; x, y = int(PX + PRX * r * math.cos(a)), int(PY + PRY * r * math.sin(a))
        d.ellipse([x - 7, y - 3, x + 7, y + 3], fill=(40, 100, 80)); d.line([(x, y), (x + 7, y)], fill=(24, 44, 78))
        if random.random() < 0.4: d.ellipse([x - 2, y - 2, x + 2, y + 1], fill=PINK_L)
    for k in range(4): d.arc([PX - PRX + 40 + k * 60, PY - 40 + k * 12, PX - PRX + 100 + k * 60, PY + 10 + k * 12], 200, 340, fill=(80, 130, 170))   # 月光波纹
    # 小岛（弁天社）+ 太鼓桥：东岸 → 岛
    IX, IY, IRX, IRY = PX - 10, PY, 82, 54
    d.ellipse([IX - IRX - 3, IY - IRY - 3, IX + IRX + 3, IY + IRY + 3], fill=K); d.ellipse([IX - IRX, IY - IRY, IX + IRX, IY + IRY], fill=(46, 74, 66))
    for _ in range(900):
        a_, r_ = random.random() * 6.283, random.random() ** 0.5
        im.putpixel((int(IX + IRX * r_ * math.cos(a_)), int(IY + IRY * r_ * math.sin(a_))), random.choice([(56, 88, 74, 255), (40, 66, 60, 255), (70, 104, 84, 255)]))
    bx0, bx1 = IX + IRX - 6, PX + PRX + 6                 # 桥两端
    bc, bh = (bx0 + bx1) // 2, (bx1 - bx0) // 2
    by = PY
    for i in range(-bh, bh + 1):
        t = i / bh; yy = by - int(20 * (1 - t * t))
        d.line([(bc + i, yy - 5), (bc + i, yy + 7)], fill=RED if abs(i) % 10 > 1 else RED_D)
        d.point((bc + i, yy - 5), fill=RED_L)
    for i in range(-bh, bh + 1, 14):
        t = i / bh; yy = by - int(20 * (1 - t * t)); d.rectangle([bc + i - 2, yy - 16, bc + i + 2, yy - 5], fill=RED_D)
    for i in range(-bh, bh + 1):
        t = i / bh; yy = by - int(20 * (1 - t * t)); d.point((bc + i, yy - 16), fill=RED_L); d.point((bc + i, yy - 17), fill=K)
    for sx in (bx0, bx1): box(d, sx - 5, by + 2, sx + 5, by + 12, STONE_D)
    water_block = (PX, PY, PRX, PRY, IX, IY, IRX, IRY, bx0, bx1, by)
    # --- 南：梯田 / 水田 ---
    for rowi in range(3):
        for coli in range(5):
            x0, y0 = 90 + coli * 140, 1330 + rowi * 52
            if x0 > 600 or y0 > 1480: continue
            d.rectangle([x0, y0, x0 + 128, y0 + 44], fill=(60, 56, 56)); d.rectangle([x0 + 3, y0 + 3, x0 + 125, y0 + 41], fill=(30, 54, 74))
            for xx in range(x0 + 8, x0 + 122, 9):
                for yy in (y0 + 12, y0 + 24, y0 + 36): d.line([(xx, yy), (xx, yy - 5)], fill=(70, 128, 84)); d.point((xx + 1, yy - 3), fill=(120, 176, 110))
            d.line([(x0 + 4, y0 + 6), (x0 + 60, y0 + 6)], fill=(60, 96, 128))
            blocks.append((x0, y0, x0 + 128, y0 + 44))
    # --- 墓地围栏（竹垣） ---
    # --- 边界树 ---
    for x in range(0, W, 20):
        for y0 in (0, H - 20):
            d.ellipse([x - 12, y0 - 6 + random.randint(-4, 4), x + 12, y0 + 22], fill=(22, 40, 48))
    for y in range(0, H, 20):
        for x0 in (0, W - 20):
            d.ellipse([x0 - 6 + random.randint(-4, 4), y - 12, x0 + 22, y + 12], fill=(22, 40, 48))
    blocks += [(0, 0, W, 24), (0, H - 20, W, H), (0, 0, 22, H), (W - 22, 0, W, H)]

    # ---------------- 物件 ----------------
    SP = {k: f() for k, f in SPRITE_FUNCS.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    # 神社
    put('jp_haiden', 1000, 440, (-62, -80, 62, 0))
    put('jp_komaL', 936, 462, (-8, -6, 8, 0)); put('jp_komaR', 1064, 462, (-8, -6, 8, 0))
    for x in (790, 880, 1120, 1210): put('jp_lantern', x, 400, (-5, -5, 5, 0))
    for x, y in ((760, 300), (1240, 300)): put('jp_sakura0', x, y, (-6, -6, 6, 0))
    put('jp_fox', 800, 260, (-7, -5, 7, 0)); put('jp_fox', 1200, 260, (-7, -5, 7, 0))
    for x, y in ((730, 330), (1270, 330), (710, 440), (1290, 440)): put('jp_cedar', x, y, (-5, -6, 5, 0))
    put('jp_chozu', 870, 470 - 40, (-26, -18, 26, 0))
    # 参道：鸟居 + 石灯笼
    for i, y in enumerate((1330, 1170, 1010, 540)):
        put('jp_torii', 1000, y, None); blocks.append((1000 - 24, y - 12, 1000 - 16, y)); blocks.append((1000 + 16, y - 12, 1000 + 24, y))
    for y in range(1380, 480, -90):
        if abs(y - 770) < 170: continue
        for sx in (-54, 54): put('jp_lantern', 1000 + sx, y, (-5, -5, 5, 0))
    # 中央广场：大鸟居 + 提灯
    put('jp_toriiB', 1000, 690, None); blocks.append((1000 - 34, 676, 1000 - 24, 690)); blocks.append((1000 + 24, 676, 1000 + 34, 690))
    for ox, oy in ((-150, 700), (150, 700), (-176, 800), (176, 800), (-120, 860), (120, 860)): put('jp_lantern', 1000 + ox, oy + (0 if oy < 760 else 20), (-5, -5, 5, 0))
    # 樱花
    for x, y in ((880, 1260), (1120, 1280), (760, 960), (1260, 980), (880, 590), (1120, 600), (600, 1010), (1300, 920), (1520, 880), (500, 520), (1010, 1440)):
        put('jp_sakura%d' % (x % 2), x, y, (-5, -6, 5, 0))
    # 竹林
    for _ in range(190):
        x, y = random.randint(110, 620), random.randint(330, 870)
        if (x - 360) ** 2 / 270 ** 2 + (y - 590) ** 2 / 290 ** 2 > 1: continue
        if any(abs(x - o['x']) < 22 and abs(y - o['y']) < 14 for o in objs): continue
        # 不堵住通往竹林的路
        if abs((y - 740) * 140 - (x - 520) * -120) / 184 < 34 and 380 < x < 700: continue
        put('jp_bamboo%d' % random.randint(0, 1), x, y, (-4, -6, 4, 0))
    put('jp_jizo', 392, 640, (-6, -5, 6, 0)); put('jp_rock0', 220, 520, (-12, -8, 12, 0)); put('jp_rock1', 480, 420, (-12, -8, 12, 0))
    # 墓地
    graves = []
    for r_ in range(7):
        for c_ in range(8):
            x, y = 1480 + c_ * 52 + (r_ % 2) * 18, 380 + r_ * 66
            if (x - 1650) ** 2 / 260 ** 2 + (y - 560) ** 2 / 290 ** 2 > 1: continue
            if abs((y - 640 + (x - 1500) * 0.55)) < 36 and x < 1640: continue          # 留出路
            if random.random() < 0.2: continue
            x += random.randint(-6, 6); y += random.randint(-6, 6)
            put('jp_grave%d' % random.randint(0, 2), x, y, (-8, -6, 8, 0)); graves.append([x, y])
            if random.random() < 0.35: put('jp_sotoba', x + 14, y + 4, None)
    put('jp_gorinto', 1700, 330, (-9, -6, 9, 0)); put('jp_gorinto', 1560, 320, (-9, -6, 9, 0))
    put('jp_jizo', 1480, 660, (-6, -5, 6, 0)); put('jp_jizo', 1500, 665, (-6, -5, 6, 0)); put('jp_jizo', 1520, 660, (-6, -5, 6, 0))
    # 村落：茅草屋
    for k, (x, y, key) in enumerate([(1400, 1000, 'jp_house0'), (1560, 1060, 'jp_house2'), (1740, 1010, 'jp_house1'), (1470, 1270, 'jp_house1'), (1640, 1300, 'jp_house0'), (1830, 1260, 'jp_house2')]):
        put(key, x, y, (-40, -26, 40, 0))
        put('jp_chochin', x - 34, y - 32, None); put('jp_chochin', x + 34, y - 32, None)
    put('jp_sakura1', 1330, 1180, (-5, -6, 5, 0)); put('jp_sakura0', 1760, 1170, (-5, -6, 5, 0))
    for x, y in ((1380, 1130), (1700, 1160), (1560, 1200)): put('jp_hay', x, y, (-10, -6, 10, 0))
    for x, y in ((150, 1362), (330, 1414), (500, 1366)): put('jp_scare', x, y, (-3, -4, 3, 0))
    # 池塘柳树 + 岩
    for x, y in ((120, 1050), (560, 960), (110, 1270), (570, 1290), (330, 960)): put('jp_willow', x, y, (-5, -6, 5, 0))
    put('jp_torii', 280, 1130, None); put('jp_haiden2', 322, 1160, (-18, -22, 18, 0))
    put('jp_rock0', 600, 1130, (-12, -8, 12, 0)); put('jp_rock1', 80, 1180, (-12, -8, 12, 0))
    # 散落的石头、灯
    for _ in range(18):
        x, y = random.randint(60, 1940), random.randint(220, 1440)
        if any(abs(x - o['x']) < 40 and abs(y - o['y']) < 30 for o in objs): continue
        if any(b[0] - 20 < x < b[2] + 20 and b[1] - 20 < y < b[3] + 20 for b in blocks): continue
        if abs(x - 1000) < 90: continue
        put('jp_rock%d' % random.randint(0, 1), x, y, (-12, -8, 12, 0))

    # ---------------- 通行网格 ----------------
    cols, rows = W // CELL, H // CELL
    grid = [[0] * cols for _ in range(rows)]
    for (x0, y0, x1, y1) in blocks:
        for r_ in range(max(0, y0 // CELL), min(rows, y1 // CELL + 1)):
            for c_ in range(max(0, x0 // CELL), min(cols, x1 // CELL + 1)): grid[r_][c_] = 1
    PX_, PY_, PRX_, PRY_, IX_, IY_, IRX_, IRY_, bx0_, bx1_, by_ = water_block
    for r_ in range(rows):
        for c_ in range(cols):
            x, y = c_ * CELL + 4, r_ * CELL + 4
            if ((x - PX_) / PRX_) ** 2 + ((y - PY_) / PRY_) ** 2 < 1.0:
                island = ((x - IX_) / (IRX_ - 4)) ** 2 + ((y - IY_) / (IRY_ - 4)) ** 2 < 1.0
                bridge = bx0_ - 4 <= x <= bx1_ + 4 and abs(y - by_) <= 12
                if not island and not bridge: grid[r_][c_] = 1
    # 物件的脚底碰撞已在 blocks 里；确保出生区、参道可走
    for r_ in range(int(660 // CELL), int(900 // CELL)):
        for c_ in range(int(860 // CELL), int(1140 // CELL)): grid[r_][c_] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for v in grid[r_]) if False else ''.join('1' if v else '0' for row in grid for v in row),
                objs=objs, w=W, h=H, start=[1000, 790], boss=[400, 250], shrine=[1000, 330], graves=graves)
    return im, sprites, data, SP


def preview(path, scale=1.0, crop=None):
    im, sprites, data, SP = build()
    full = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        spr, ax, ay = SP[o['img']]
        full.alpha_composite(spr, (int(o['x'] - ax), int(o['y'] - ay)))
    # 夜色灯光：给灯笼/提灯加暖光晕
    glow = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for o in data['objs']:
        if o['img'] in ('jp_lantern', 'jp_chochin'):
            for k, rr in enumerate((30, 20, 11)): g.ellipse([o['x'] - rr, o['y'] - 24 - rr * 0.8, o['x'] + rr, o['y'] - 24 + rr * 0.8], fill=(255, 196, 100, 16 + k * 8))
        if o['img'] == 'jp_haiden': g.ellipse([o['x'] - 70, o['y'] - 70, o['x'] + 70, o['y']], fill=(255, 190, 90, 26))
    full.alpha_composite(glow)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'jp_preview.png', 0.5)
