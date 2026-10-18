"""第三章·下南洋：民国初年海峡殖民地的码头城市（槟城/马六甲风）。南面是海港与栈桥、帆船和汽船；
中央唐人街是粉彩色的小娘惹(峇峇娘惹)骑楼，街北是天后宫；西边马来甘榜高脚屋；东边华人义山；西北丛林里藏着降头师的屋子。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw
import map_jp as J
import map_heian as Hn
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW, STRAW, STRAW_D, STRAW_L

W, H = 2200, 1600
CELL = 8
SEA, SEA_D, SEA_L = (22, 62, 80), (16, 46, 64), (60, 120, 140)
SAND = [(70, 66, 62), (64, 60, 58), (76, 70, 64)]
# 小娘惹粉彩（夜里略压暗）
PASTEL = [(196, 128, 144), (100, 176, 170), (218, 188, 108), (116, 146, 200), (132, 188, 144), (156, 134, 186)]
TERRA, TERRA_D = (160, 80, 56), (120, 56, 44)
PALM, PALM_D, PALM_L = (44, 110, 70), (28, 76, 56), (84, 150, 96)


def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)


def shophouse(w=72, hue=0, floors=2, var=0):
    """小娘惹骑楼：底层是五脚基拱廊（亮柱+暗室），二层是绿色百叶窗，顶部是带圆形灰泥浮雕的曲线山墙"""
    r = random.Random(var * 7 + hue)
    col = PASTEL[hue % len(PASTEL)]; cd = shade(col, 0.75); cl = shade(col, 1.18)
    fh = 40
    h = fh * floors + 40
    im, d = canvas(w + 12, h); x0 = 6; cx = (w + 12) // 2; by = h - 4
    shadow(d, cx, by, w // 2 + 4, 5)
    top = by - fh * floors
    d.rectangle([x0, top, x0 + w, by], fill=K); d.rectangle([x0 + 1, top + 1, x0 + w - 1, by - 1], fill=col)
    # 山墙（曲线）
    for i in range(w + 1):
        t = (i / w) * 2 - 1; yy = top - int(10 * (1 - t * t)) - (4 if abs(t) < 0.35 else 0)
        d.line([(x0 + i, yy), (x0 + i, top + 1)], fill=K if i in (0, w) else col)
        d.point((x0 + i, yy - 1), fill=K)
    d.ellipse([cx - 7, top - 12, cx + 7, top + 2], fill=cl); d.ellipse([cx - 4, top - 9, cx + 4, top - 1], fill=cd)     # 圆形浮雕
    d.line([(x0 + 3, top + 4), (x0 + w - 3, top + 4)], fill=cl); d.line([(x0 + 3, top + 7), (x0 + w - 3, top + 7)], fill=cd)
    for k in range(floors):
        y1 = top + k * fh + 10; y2 = y1 + fh - 18
        if k == floors - 1:                                                               # 底层拱廊
            n = max(2, w // 24)
            for i in range(n):
                ax = x0 + 6 + i * (w - 12) // n; aw = (w - 12) // n - 4
                d.rectangle([ax, y1 + 4, ax + aw, by - 2], fill=(26, 20, 30))
                d.ellipse([ax - 1, y1 + 2, ax + aw + 1, y1 + 12], fill=(26, 20, 30)); d.rectangle([ax, y1 + 8, ax + aw, by - 2], fill=(26, 20, 30))
                d.rectangle([ax + 2, by - 24, ax + aw - 2, by - 3], fill=(236, 190, 100) if r.random() < 0.6 else (50, 40, 52))      # 铺面灯火
                d.line([(ax + aw // 2, by - 24), (ax + aw // 2, by - 3)], fill=(110, 80, 54))
            for i in range(n + 1):
                px = x0 + 4 + i * (w - 8) // n; d.rectangle([px - 2, y1 + 2, px + 2, by - 1], fill=cl); d.line([(px + 2, y1 + 2), (px + 2, by - 1)], fill=cd)
        else:
            n = max(2, w // 26)
            for i in range(n):
                wx = x0 + 8 + i * (w - 16) // n; ww = (w - 16) // n - 6
                d.rectangle([wx - 1, y1 - 1, wx + ww + 1, y2 + 1], fill=K)
                lit = r.random() < 0.5
                d.rectangle([wx, y1, wx + ww, y2], fill=(240, 200, 110) if lit else (46, 80, 70))
                for yy in range(y1 + 1, y2, 3): d.line([(wx, yy), (wx + ww, yy)], fill=(34, 64, 56) if not lit else (190, 140, 70))      # 百叶
                d.rectangle([wx - 3, y1, wx - 2, y2], fill=(50, 110, 80)); d.rectangle([wx + ww + 2, y1, wx + ww + 3, y2], fill=(50, 110, 80))
        d.line([(x0 + 1, top + (k + 1) * fh + 8 - (fh if False else 0)), (x0 + w - 1, top + (k + 1) * fh + 8)], fill=cl) if k < floors - 1 else None
    # 装饰瓷砖带
    ty = by - 8
    for i in range(0, w, 6): d.rectangle([x0 + 1 + i, ty, x0 + 4 + i, ty + 4], fill=[(80, 150, 190), (220, 190, 100), (200, 90, 100)][(i // 6) % 3])
    return im, cx, by


def palm(var=0):
    r = random.Random(var + 31)
    im, d = canvas(46, 82); cx, by = 23, 78
    shadow(d, cx, by, 12)
    lean = r.choice([-6, -4, 4, 6])
    pts = [(cx + lean * (t / 10) ** 2 * 2, by - t * 5.2) for t in range(11)]
    for (a, b) in zip(pts, pts[1:]): d.line([a, b], fill=K, width=5); d.line([a, b], fill=(110, 82, 58), width=3)
    for i, (a, b) in enumerate(zip(pts, pts[1:])): d.line([(a[0] - 1, a[1]), (b[0] - 1, b[1])], fill=(140, 106, 72)) if i % 2 == 0 else None
    tx, ty = pts[-1]
    for ang in range(-170, 11, 30):
        a = math.radians(ang + r.randint(-6, 6)); L = r.randint(18, 24)
        ex, ey = tx + L * math.cos(a), ty + L * math.sin(a) * 0.6 + 6 * abs(math.cos(a))
        mx, my = tx + L * 0.5 * math.cos(a), ty + L * 0.5 * math.sin(a) * 0.6 - 5
        d.line([(tx, ty), (mx, my), (ex, ey)], fill=K, width=4); d.line([(tx, ty), (mx, my), (ex, ey)], fill=PALM, width=2)
        d.line([(mx, my), (ex, ey)], fill=PALM_L, width=1)
    for ox in (-2, 2): d.ellipse([tx + ox - 3, ty + 1, tx + ox + 3, ty + 7], fill=K); d.ellipse([tx + ox - 2, ty + 2, tx + ox + 2, ty + 6], fill=(150, 120, 60))   # 椰子
    return im, cx, by


def banana():
    im, d = canvas(40, 50); cx, by = 20, 48
    shadow(d, cx, by, 12)
    for ang, L in ((-150, 22), (-120, 26), (-90, 24), (-60, 26), (-30, 22)):
        a = math.radians(ang); ex, ey = cx + L * math.cos(a), by - 8 + L * math.sin(a)
        d.line([(cx, by - 4), (ex, ey)], fill=K, width=6); d.line([(cx, by - 4), (ex, ey)], fill=(50, 120, 74), width=4); d.line([(cx, by - 4), (ex, ey)], fill=(96, 160, 100), width=1)
    d.rectangle([cx - 2, by - 8, cx + 2, by], fill=K); d.rectangle([cx - 1, by - 8, cx + 1, by], fill=(90, 130, 70))
    return im, cx, by


def banyan():
    """榕树：巨大的树冠 + 垂下的气根"""
    im, d = canvas(110, 108); cx, by = 55, 104
    shadow(d, cx, by - 1, 34, 8)
    for ox in (-20, -8, 8, 22): d.rectangle([cx + ox - 3, by - 40, cx + ox + 3, by], fill=K); d.rectangle([cx + ox - 2, by - 40, cx + ox + 2, by], fill=(86, 70, 62))
    for ox, oy, rr in [(0, -60, 36), (-30, -50, 24), (30, -50, 24), (-14, -78, 22), (16, -76, 22)]: d.ellipse([cx + ox - rr - 1, by + oy - rr - 1, cx + ox + rr + 1, by + oy + rr + 1], fill=K)
    for i, (ox, oy, rr) in enumerate([(0, -60, 36), (-30, -50, 24), (30, -50, 24), (-14, -78, 22), (16, -76, 22)]): d.ellipse([cx + ox - rr, by + oy - rr, cx + ox + rr, by + oy + rr], fill=(36, 88, 66) if i % 2 else (44, 104, 76))
    for x in range(cx - 50, cx + 51, 8):
        top = by - 46 + int(abs(x - cx) * 0.3); d.line([(x, top), (x + 1, top + 24 + (x % 3) * 6)], fill=(96, 78, 66), width=1)
    return im, cx, by


def stilt_house(var=0):
    """甘榜高脚屋：棕榈叶(亚答)屋顶、木板墙、高脚楼梯"""
    im, d = canvas(84, 92); cx, by = 42, 88
    shadow(d, cx, by, 30, 5)
    for x in (cx - 28, cx - 10, cx + 10, cx + 28): d.rectangle([x - 2, by - 28, x + 2, by], fill=K); d.rectangle([x - 1, by - 28, x + 1, by], fill=WOOD)
    box(d, cx - 34, by - 32, cx + 34, by - 26, WOOD_D)
    box(d, cx - 30, by - 58, cx + 30, by - 32, (130, 98, 70))
    for x in range(cx - 28, cx + 30, 5): d.line([(x, by - 56), (x, by - 34)], fill=(104, 76, 56))
    box(d, cx - 8, by - 54, cx + 8, by - 34, (30, 22, 30)); d.rectangle([cx - 6, by - 52, cx + 6, by - 36], fill=(240, 196, 100))
    box(d, cx + 14, by - 50, cx + 26, by - 42, (240, 196, 100))
    d.polygon([(cx - 42, by - 54), (cx + 42, by - 54), (cx + 22, by - 86), (cx - 22, by - 86)], fill=K)
    d.polygon([(cx - 40, by - 55), (cx + 40, by - 55), (cx + 21, by - 84), (cx - 21, by - 84)], fill=STRAW)
    for y in range(by - 82, by - 56, 4):
        t = (by - 55 - y) / 29; d.line([(cx - 40 + t * 19 + 2, y), (cx + 40 - t * 19 - 2, y)], fill=STRAW_D)
    for x in range(cx - 36, cx + 38, 5): d.line([(x, by - 56), (x - 1, by - 52)], fill=STRAW_L)
    d.line([(cx + 30, by - 28), (cx + 40, by)], fill=K, width=3); d.line([(cx + 30, by - 28), (cx + 40, by)], fill=WOOD, width=1)
    return im, cx, by


def temple():
    """天后宫（华人会馆/妈祖庙）：红墙、双层黄琉璃屋顶、燕尾脊、石狮"""
    w, h = 220, 176
    im, d = canvas(w + 40, h); cx = (w + 40) // 2; x0, x1 = 20, w + 20; by = h - 4
    shadow(d, cx, by, w // 2 + 8, 8)
    for i in range(3): box(d, cx - 40 - i * 6, by - 4 - i * 6, cx + 40 + i * 6, by - i * 6, STONE if i % 2 else STONE_L)
    box(d, x0 - 4, by - 26, x1 + 4, by - 18, STONE_D)
    box(d, x0, by - 84, x1, by - 26, (168, 50, 46)); d.rectangle([x0 + 1, by - 84, x1 - 1, by - 80], fill=(120, 34, 36))
    Hn.pillars(d, x0 + 6, x1 - 6, by - 82, by - 26, 6, col=(200, 70, 56))
    box(d, cx - 24, by - 74, cx + 24, by - 26, (30, 20, 26)); d.rectangle([cx - 22, by - 72, cx + 22, by - 28], fill=(240, 190, 96))
    for gx in (cx - 14, cx - 4, cx + 6, cx + 16): d.line([(gx, by - 72), (gx, by - 28)], fill=(150, 90, 50))
    d.rectangle([cx - 20, by - 82, cx + 20, by - 74], fill=(30, 22, 30)); d.text((cx, by - 78), '天后宫', fill=(244, 214, 120), anchor='mm', font=J.ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 9, index=2)) if hasattr(J, 'ImageFont') else None
    YEL, YD, YL = (200, 150, 64), (150, 104, 44), (236, 196, 100)
    Hn.roof(d, x0 - 8, x1 + 8, by - 84, by - 112, YEL, YD, YL, 16, 12)
    Hn.roof(d, x0 + 26, x1 - 26, by - 112, by - 142, YEL, YD, YL, 14, 12)
    d.line([(x0 + 34, by - 142), (x1 - 34, by - 142)], fill=YL, width=2)
    for sx in (x0 + 22, x1 - 22):                                                  # 燕尾脊
        d.polygon([(sx - 2, by - 142), (sx + 4, by - 142), (sx + 12 * (1 if sx > cx else -1), by - 156), (sx + 6 * (1 if sx > cx else -1), by - 146)], fill=(60, 140, 120))
    d.ellipse([cx - 8, by - 152, cx + 8, by - 140], fill=(60, 140, 120)); d.ellipse([cx - 4, by - 148, cx + 4, by - 142], fill=(236, 196, 100))
    return im, cx, by


def junk():
    """帆船（中式三桅夹板船）"""
    im, d = canvas(170, 150); cx, by = 85, 140
    d.polygon([(cx - 70, by - 26), (cx + 70, by - 26), (cx + 54, by), (cx - 56, by)], fill=K)
    d.polygon([(cx - 68, by - 25), (cx + 68, by - 25), (cx + 52, by - 2), (cx - 54, by - 2)], fill=(92, 56, 44))
    d.line([(cx - 68, by - 25), (cx + 68, by - 25)], fill=(150, 100, 64), width=2); d.line([(cx - 60, by - 10), (cx + 56, by - 10)], fill=(60, 36, 34))
    d.rectangle([cx + 40, by - 40, cx + 66, by - 26], fill=K); d.rectangle([cx + 41, by - 39, cx + 65, by - 27], fill=(120, 70, 50))
    d.ellipse([cx - 66, by - 18, cx - 58, by - 10], fill=(236, 226, 190))                       # 船眼
    for mx, mh, mw in ((cx - 34, 108, 40), (cx + 4, 120, 46), (cx + 38, 92, 32)):
        d.rectangle([mx - 1, by - 26 - mh, mx + 1, by - 26], fill=K)
        d.polygon([(mx + 2, by - 24 - mh + 6), (mx + 2 + mw, by - 24 - mh + 12), (mx + 2 + mw, by - 34), (mx + 2, by - 32)], fill=K)
        d.polygon([(mx + 3, by - 24 - mh + 8), (mx + 1 + mw, by - 24 - mh + 13), (mx + 1 + mw, by - 36), (mx + 3, by - 34)], fill=(150, 76, 52))
        for yy in range(by - 24 - mh + 16, by - 36, 12): d.line([(mx + 2, yy), (mx + mw, yy + 2)], fill=(104, 50, 40))
    return im, cx, by


def steamer():
    """汽船"""
    im, d = canvas(230, 130); cx, by = 115, 122
    d.polygon([(cx - 104, by - 34), (cx + 100, by - 34), (cx + 84, by), (cx - 86, by)], fill=K)
    d.polygon([(cx - 102, by - 33), (cx + 98, by - 33), (cx + 82, by - 2), (cx - 84, by - 2)], fill=(30, 34, 46))
    d.rectangle([cx - 100, by - 34, cx + 98, by - 28], fill=(160, 50, 46))
    for x in range(cx - 80, cx + 78, 14): d.ellipse([x, by - 22, x + 5, by - 17], fill=(236, 200, 110))
    box(d, cx - 56, by - 62, cx + 50, by - 34, (210, 206, 196)); box(d, cx - 30, by - 84, cx + 28, by - 62, (200, 196, 186))
    for x in range(cx - 52, cx + 46, 10): d.rectangle([x, by - 56, x + 5, by - 48], fill=(240, 200, 110))
    for x in range(cx - 24, cx + 24, 9): d.rectangle([x, by - 78, x + 4, by - 70], fill=(240, 200, 110))
    for fx in (cx - 14, cx + 20):
        box(d, fx - 8, by - 112, fx + 8, by - 84, (40, 40, 52)); d.rectangle([fx - 8, by - 98, fx + 8, by - 94], fill=(200, 60, 52))
        d.ellipse([fx - 12, by - 134, fx + 12, by - 112], fill=(60, 64, 80, 160))
    d.line([(cx - 70, by - 34), (cx - 70, by - 92)], fill=K, width=2)
    return im, cx, by


def crates():
    im, d = canvas(44, 40); cx, by = 22, 38
    shadow(d, cx, by, 18, 4)
    for (x, y, w_, h_) in ((cx - 18, by - 16, 18, 16), (cx + 2, by - 14, 16, 14), (cx - 10, by - 30, 18, 14)):
        box(d, x, y, x + w_, y + h_, (140, 104, 70)); d.line([(x + 1, y + 1), (x + w_ - 1, y + h_ - 1)], fill=WOOD_D); d.line([(x + w_ - 1, y + 1), (x + 1, y + h_ - 1)], fill=WOOD_D)
    return im, cx, by


def barrel():
    im, d = canvas(24, 32); cx, by = 12, 30
    shadow(d, cx, by, 9, 3)
    d.rectangle([cx - 8, by - 22, cx + 8, by], fill=K); d.rectangle([cx - 7, by - 21, cx + 7, by - 1], fill=(120, 84, 58))
    for y in (by - 17, by - 6): d.line([(cx - 7, y), (cx + 7, y)], fill=(60, 50, 56))
    d.ellipse([cx - 8, by - 26, cx + 8, by - 18], fill=K); d.ellipse([cx - 7, by - 25, cx + 7, by - 19], fill=(150, 108, 74))
    return im, cx, by


def godown():
    """仓库（铁皮屋顶）"""
    im, d = canvas(130, 94); cx, by = 65, 90
    shadow(d, cx, by, 54, 6)
    box(d, cx - 52, by - 46, cx + 52, by, (130, 118, 104))
    for x in range(cx - 48, cx + 50, 8): d.line([(x, by - 44), (x, by - 2)], fill=(104, 94, 84))
    box(d, cx - 16, by - 38, cx + 16, by, (50, 40, 44)); d.line([(cx, by - 38), (cx, by)], fill=K)
    d.polygon([(cx - 58, by - 44), (cx + 58, by - 44), (cx + 44, by - 80), (cx - 44, by - 80)], fill=K)
    d.polygon([(cx - 56, by - 45), (cx + 56, by - 45), (cx + 43, by - 78), (cx - 43, by - 78)], fill=(100, 108, 120))
    for x in range(cx - 52, cx + 54, 6): d.line([(x, by - 45), (x + (cx - x) // 4, by - 78)], fill=(74, 80, 92))
    return im, cx, by


def gaslamp():
    im, d = canvas(20, 56); cx, by = 10, 54
    shadow(d, cx, by, 6, 2)
    d.rectangle([cx - 1, 12, cx + 1, by], fill=K); d.rectangle([cx, 12, cx, by - 1], fill=(70, 70, 86))
    box(d, cx - 4, by - 4, cx + 4, by, (60, 60, 76))
    d.ellipse([cx - 5, 2, cx + 5, 14], fill=K); d.ellipse([cx - 4, 3, cx + 4, 13], fill=(250, 214, 120))
    d.polygon([(cx - 6, 4), (cx + 6, 4), (cx, 0)], fill=K)
    return im, cx, by


def rickshaw():
    im, d = canvas(48, 40); cx, by = 24, 38
    shadow(d, cx, by, 16, 3)
    box(d, cx - 12, by - 22, cx + 10, by - 8, (40, 36, 50)); d.polygon([(cx - 14, by - 22), (cx + 12, by - 22), (cx + 6, by - 34), (cx - 6, by - 34)], fill=K); d.polygon([(cx - 12, by - 23), (cx + 10, by - 23), (cx + 5, by - 32), (cx - 5, by - 32)], fill=(60, 44, 40))
    d.ellipse([cx - 4, by - 14, cx + 16, by + 2], outline=K, width=2); d.ellipse([cx - 2, by - 12, cx + 14, by], outline=(150, 150, 160))
    d.line([(cx - 12, by - 12), (cx - 28, by - 8)], fill=K, width=2)
    return im, cx, by


def chinese_tomb():
    """华人义山的圆弧墓（福建风）：半圆围护 + 墓碑 + 土丘"""
    im, d = canvas(68, 52); cx, by = 34, 50
    shadow(d, cx, by, 26, 5)
    d.ellipse([cx - 28, by - 36, cx + 28, by + 2], fill=K); d.ellipse([cx - 26, by - 34, cx + 26, by], fill=(78, 80, 98))
    d.ellipse([cx - 18, by - 28, cx + 18, by - 4], fill=(48, 62, 56)); d.ellipse([cx - 12, by - 24, cx + 12, by - 10], fill=(58, 82, 66))
    box(d, cx - 8, by - 40, cx + 8, by - 22, STONE); d.polygon([(cx - 8, by - 40), (cx + 8, by - 40), (cx, by - 46)], fill=STONE_L)
    for y in range(by - 38, by - 24, 4): d.line([(cx, y), (cx, y + 1)], fill=STONE_D)
    for ox in (-24, 24): box(d, cx + ox - 3, by - 20, cx + ox + 3, by, STONE_L)
    return im, cx, by


def shaman_hut():
    """降头师的小屋：黑色木屋、红布、骷髅杆、绿色蜡烛火"""
    im, d = canvas(110, 112); cx, by = 55, 108
    shadow(d, cx, by, 40, 6)
    box(d, cx - 34, by - 50, cx + 34, by, (50, 38, 44))
    for x in range(cx - 32, cx + 34, 6): d.line([(x, by - 48), (x, by - 2)], fill=(36, 26, 34))
    box(d, cx - 10, by - 40, cx + 10, by, (16, 12, 20)); d.rectangle([cx - 8, by - 38, cx + 8, by - 2], fill=(34, 20, 44))
    d.rectangle([cx - 8, by - 38, cx + 8, by - 28], fill=(160, 40, 44)); d.line([(cx - 8, by - 28), (cx + 8, by - 28)], fill=(220, 190, 90))   # 红布门帘
    for x in (cx - 24, cx + 24): d.ellipse([x - 4, by - 36, x + 4, by - 28], fill=(70, 220, 130)); d.ellipse([x - 2, by - 34, x + 2, by - 30], fill=(190, 255, 210))
    d.polygon([(cx - 46, by - 48), (cx + 46, by - 48), (cx + 26, by - 90), (cx - 26, by - 90)], fill=K)
    d.polygon([(cx - 44, by - 49), (cx + 44, by - 49), (cx + 25, by - 88), (cx - 25, by - 88)], fill=(70, 62, 56))
    for y in range(by - 86, by - 50, 5):
        t = (by - 49 - y) / 39; d.line([(cx - 44 + t * 19 + 2, y), (cx + 44 - t * 19 - 2, y)], fill=(50, 44, 40))
    for sx in (cx - 40, cx + 40):                                                   # 骷髅杆
        d.line([(sx, by), (sx, by - 62)], fill=K, width=3); d.line([(sx, by), (sx, by - 62)], fill=(120, 96, 70), width=1)
        d.ellipse([sx - 6, by - 74, sx + 6, by - 60], fill=K); d.ellipse([sx - 5, by - 73, sx + 5, by - 61], fill=(226, 220, 200))
        d.rectangle([sx - 3, by - 70, sx - 1, by - 67], fill=K); d.rectangle([sx + 1, by - 70, sx + 3, by - 67], fill=K)
    return im, cx, by


def lantern_red():
    im, d = canvas(16, 30); cx = 8
    d.line([(cx, 0), (cx, 4)], fill=K); d.ellipse([cx - 7, 4, cx + 7, 24], fill=K); d.ellipse([cx - 6, 5, cx + 6, 23], fill=(226, 70, 56))
    for y in (10, 14, 18): d.line([(cx - 5, y), (cx + 5, y)], fill=(150, 40, 40))
    d.line([(cx, 24), (cx, 29)], fill=(236, 200, 90), width=2)
    return im, cx, 28


SPRITES = {k: v for k, v in J.SPRITE_FUNCS.items() if k in ('jp_rock0', 'jp_rock1', 'jp_gorinto', 'jp_jizo', 'jp_lantern', 'jp_chochin')}
SPRITES.update({'hn_stall0': lambda: Hn.market_stall(0), 'hn_stall1': lambda: Hn.market_stall(1)})
SPRITES.update({'ny_house%d' % i: (lambda i=i: shophouse(72 + (i % 3) * 12, i, 2, i)) for i in range(6)})
SPRITES.update({'ny_house3f%d' % i: (lambda i=i: shophouse(84, i + 2, 3, i + 9)) for i in range(3)})
SPRITES.update({'ny_palm0': lambda: palm(0), 'ny_palm1': lambda: palm(1), 'ny_palm2': lambda: palm(2), 'ny_banana': banana, 'ny_banyan': banyan,
                'ny_stilt0': lambda: stilt_house(0), 'ny_temple': temple, 'ny_junk': junk, 'ny_steamer': steamer, 'ny_crates': crates, 'ny_barrel': barrel,
                'ny_godown': godown, 'ny_lamp': gaslamp, 'ny_rickshaw': rickshaw, 'ny_tomb': chinese_tomb, 'ny_shaman': shaman_hut, 'ny_redlantern': lantern_red})


def build(seed=57):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), SAND[0] + (255,)); d = ImageDraw.Draw(im)
    blocks = []
    for _ in range(110000): im.putpixel((random.randrange(W), random.randrange(H)), random.choice(SAND) + (255,))
    for _ in range(900):
        x, y = random.randrange(W), random.randrange(150, 1100)
        for dx, hh in ((0, 2), (1, 4), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(58, 96, 78))
    for _ in range(26000):
        x, y = random.randrange(W), random.randrange(300, 1100)
        if (x < 560 or x > 1640) and random.random() < 0.9: im.putpixel((x, y), random.choice([(54, 74, 62, 255), (46, 66, 58, 255), (60, 82, 66, 255)]))
    # 北部丛林带
    for _ in range(36000):
        x, y = random.randrange(W), random.randrange(0, 300)
        if y < 300 - 60 * math.sin(x / 190) * 0.5 - 40: im.putpixel((x, y), random.choice([(30, 62, 56, 255), (24, 52, 50, 255), (36, 74, 60, 255)]))
    SEA_Y = lambda x: 1180 + 26 * math.sin(x / 210) + 12 * math.sin(x / 67)
    # 海
    for x in range(W):
        ys = int(SEA_Y(x)); d.line([(x, ys), (x, H)], fill=SEA)
        d.line([(x, ys - 3), (x, ys)], fill=(96, 86, 76)); d.line([(x, ys), (x, ys + 3)], fill=SEA_L)
    for _ in range(9000):
        x = random.randrange(W); y = random.randrange(int(SEA_Y(x)) + 6, H)
        im.putpixel((x, y), random.choice([SEA_D, SEA_L, (30, 80, 100, 255)]))
    for _ in range(260):
        x = random.randrange(W); y = random.randrange(int(SEA_Y(x)) + 20, H - 10)
        d.line([(x, y), (x + 8, y)], fill=(100, 160, 176)); d.line([(x + 2, y + 2), (x + 6, y + 2)], fill=(100, 160, 176))
    # 道路
    CX = 1100; RY = 800
    J.road(d, [(CX, 340), (CX, 1100)], 84, col=(118, 104, 90))
    J.road(d, [(140, RY), (2060, RY)], 70, col=(118, 104, 90))
    J.road(d, [(140, 1090), (2060, 1096)], 50, col=(112, 100, 90))               # 滨海大道
    for _ in range(3500): im.putpixel((random.randint(CX - 40, CX + 40), random.randint(340, 1100)), random.choice([(104, 92, 80, 255), (132, 118, 104, 255)]))
    # 十字口广场
    d.ellipse([CX - 130, RY - 80, CX + 130, RY + 80], fill=(98, 88, 78)); d.ellipse([CX - 126, RY - 76, CX + 126, RY + 76], fill=(122, 108, 94))
    d.ellipse([CX - 8, RY - 5, CX + 8, RY + 5], fill=K)
    # 天后宫前广场（石板）
    d.rectangle([CX - 200, 300, CX + 200, 430], fill=(104, 96, 90))
    for x in range(CX - 200, CX + 200, 20):
        for y in range(300, 430, 20): d.rectangle([x, y, x + 19, y + 19], outline=(92, 84, 80))
    # 栈桥（三条）
    piers = [(420, 60), (1090, 70), (1760, 60)]
    for px, pw in piers:
        y0 = int(SEA_Y(px)) - 10
        d.rectangle([px - pw // 2 - 2, y0, px + pw // 2 + 2, y0 + 250], fill=K); d.rectangle([px - pw // 2, y0 + 2, px + pw // 2, y0 + 248], fill=(122, 90, 66))
        for yy in range(y0 + 4, y0 + 248, 6): d.line([(px - pw // 2, yy), (px + pw // 2, yy)], fill=(96, 68, 52))
        for yy in range(y0 + 10, y0 + 250, 40):
            for sx in (px - pw // 2 - 3, px + pw // 2 + 2): d.rectangle([sx - 1, yy, sx + 1, yy + 8], fill=K); d.point((sx, yy + 1), fill=(150, 112, 80))
    # 马来甘榜（西）：泥路
    J.road(d, [(CX - 40, 700), (700, 690), (480, 700), (300, 640)], 34, col=(110, 96, 84))
    J.road(d, [(480, 700), (460, 980)], 30, col=(110, 96, 84))
    # 华人义山（东）：台阶式山丘
    for k in range(4):
        y0 = 300 + k * 130
        d.rectangle([1700, y0, 2110, y0 + 118], fill=(40, 60, 56 + k * 4)); d.rectangle([1700, y0 + 118, 2110, y0 + 126], fill=K); d.rectangle([1700, y0 + 120, 2110, y0 + 124], fill=(96, 92, 100))
        for _ in range(3000): im.putpixel((random.randrange(1700, 2110), random.randrange(y0, y0 + 118)), random.choice([(46, 70, 62, 255), (34, 54, 52, 255), (52, 80, 66, 255)]))
        blocks.append((1700, y0 + 118, 1960, y0 + 126)); blocks.append((2010, y0 + 118, 2110, y0 + 126))     # 台阶口在 1960..2010
        d.rectangle([1960, y0 + 118, 2010, y0 + 136], fill=(124, 112, 100))
    J.road(d, [(1500, RY), (1700, RY), (1985, RY - 40), (1985, 320)], 30, col=(110, 98, 90))
    blocks.append((1690, 290, 1700, 830))
    # 降头师小屋前：白灰圆阵 + 符咒
    SH = (300, 380)
    d.ellipse([SH[0] - 66, SH[1] + 24, SH[0] + 66, SH[1] + 84], outline=(200, 196, 180), width=2)
    for i in range(8):
        a = math.radians(i * 45); d.line([(SH[0] + 56 * math.cos(a), SH[1] + 54 + 24 * math.sin(a)), (SH[0] + 66 * math.cos(a), SH[1] + 54 + 30 * math.sin(a))], fill=(200, 196, 180))
    d.line([(SH[0] - 40, SH[1] + 54), (SH[0] + 40, SH[1] + 54)], fill=(70, 220, 130)); d.line([(SH[0], SH[1] + 36), (SH[0], SH[1] + 72)], fill=(70, 220, 130))
    J.road(d, [(300, 640), (310, 470)], 28, col=(100, 88, 78))
    # 边界
    for x in range(0, W, 20): d.ellipse([x - 12, -10 + random.randint(-4, 4), x + 12, 22], fill=(22, 44, 48))
    for y in range(0, 1100, 20):
        d.ellipse([-6 + random.randint(-4, 4), y - 12, 22, y + 12], fill=(22, 44, 48)); d.ellipse([W - 22 + random.randint(-4, 4), y - 12, W + 6, y + 12], fill=(22, 44, 48))
    blocks += [(0, 0, W, 24), (0, 0, 22, 1100), (W - 22, 0, W, 1100)]

    SP = {k: f() for k, f in SPRITES.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    # 天后宫
    put('ny_temple', CX, 430, (-100, -84, 100, 0))
    for x in (CX - 150, CX + 150): put('ny_redlantern', x, 380, None)
    for x in (CX - 170, CX - 120, CX + 120, CX + 170): put('ny_lamp', x, 420, (-3, -4, 3, 0))
    # 唐人街骑楼：连排（五脚基相连），沿主街和二条横街两侧
    def row(x_start, y, specs, floors):
        x = x_start
        for (w_, hue) in specs:
            key = 'ny_h%d_%d_%d' % (w_, hue, floors)
            if key not in SP: SP[key] = shophouse(w_, hue, floors, hue + w_)
            put(key, x + w_ // 2, y, (-w_ // 2, -(40 * floors + 10), w_ // 2, 0)); x += w_
        return x
    row(520, 590, [(84, 0), (72, 1), (96, 2), (80, 3), (88, 4), (76, 5)], 2)
    row(1160, 590, [(88, 4), (76, 2), (84, 0), (96, 1), (72, 3), (88, 5)], 2)
    row(520, 760, [(76, 3), (88, 1), (84, 5), (72, 0), (96, 2), (80, 4)], 2)
    row(1160, 760, [(80, 2), (96, 4), (72, 1), (88, 5), (84, 0), (76, 3)], 2)
    row(520, 990, [(88, 5), (96, 0), (84, 2), (92, 4), (80, 1)], 3)
    row(1160, 990, [(92, 1), (80, 3), (96, 5), (88, 0), (84, 2)], 3)
    for x, y in ((CX - 130, 700), (CX + 130, 700), (CX - 130, 900), (CX + 130, 900)): put('ny_lamp', x, y, (-3, -4, 3, 0))
    for y in (480, 620, 1000):
        put('ny_lamp', CX - 60, y, (-3, -4, 3, 0)); put('ny_lamp', CX + 60, y, (-3, -4, 3, 0))
    put('ny_rickshaw', CX + 180, RY + 100, (-14, -8, 14, 0)); put('ny_rickshaw', 800, RY + 70, (-14, -8, 14, 0))
    for x, y in ((CX - 190, 470), (CX + 190, 470), (480, 580), (1700, 580), (480, 760), (1700, 760)): put('ny_palm%d' % (x % 3), x, y, (-4, -6, 4, 0))
    # 码头
    for x in (620, 1500): put('ny_godown', x, 1060, (-52, -46, 52, 0))
    for x, y in ((380, 1120), (470, 1130), (1050, 1130), (1140, 1120), (1720, 1130), (1800, 1120)): put('ny_crates', x, y, (-18, -22, 18, 0))
    for x, y in ((360, 1105), (500, 1110), (1020, 1110), (1180, 1105), (1690, 1110), (1830, 1110), (900, 1075), (1320, 1075)): put('ny_barrel', x, y, (-8, -10, 8, 0))
    for x in (260, 820, 1380, 1960): put('ny_lamp', x, 1075, (-3, -4, 3, 0))
    for x in (280, 760, 1280, 1900): put('hn_stall%d' % ((x // 10) % 2), x, 1060, (-32, -22, 32, 0))
    # 海上：帆船、汽船（碰撞为水体已封死，不需要 solid）
    put('ny_junk', 700, 1420, None); put('ny_junk', 1330, 1500, None); put('ny_steamer', 1980, 1420, None); put('ny_junk', 150, 1480, None)
    # 西：甘榜
    for x, y in ((220, 560), (360, 520), (180, 740), (350, 780), (230, 930), (390, 950)): put('ny_stilt0', x, y, (-34, -34, 34, 0))
    for x, y in ((120, 640), (460, 600), (130, 860), (500, 860), (290, 620), (300, 880), (500, 780), (560, 1010)): put('ny_palm%d' % (x % 3), x, y, (-4, -6, 4, 0))
    for x, y in ((420, 640), (160, 960)): put('ny_banana', x, y, (-5, -6, 5, 0))
    put('ny_banyan', 700, 960, (-14, -10, 14, 0))
    # 北：丛林 + 降头师
    put('ny_shaman', SH[0], SH[1], (-44, -50, 44, 0))
    for x in range(80, 2100, 70):
        y = random.randint(190, 300)
        if abs(x - SH[0]) < 80 and y > 250: continue
        if abs(x - CX) < 240 and y > 240: continue
        put('ny_palm%d' % random.randint(0, 2), x + random.randint(-14, 14), y, (-4, -6, 4, 0))
    for x in range(160, 2000, 190): put('ny_banana', x + random.randint(-30, 30), random.randint(310, 350), (-5, -6, 5, 0)) if abs(x - CX) > 260 else None
    for x, y in ((240, 330), (360, 340), (260, 440), (350, 450)): put('ny_banana', x, y, (-5, -6, 5, 0))
    put('ny_banyan', 560, 330, (-14, -10, 14, 0)); put('ny_banyan', 1560, 300, (-14, -10, 14, 0))
    # 东：华人义山
    graves = []
    for k_ in range(4):
        y0 = 300 + k_ * 130
        for x in range(1740, 1940, 76):
            put('ny_tomb', x + random.randint(-6, 6), y0 + 94, (-28, -24, 28, 0)); graves.append([x, y0 + 94])
        for x in range(2040, 2100, 60):
            put('ny_tomb', x, y0 + 94, (-28, -24, 28, 0)); graves.append([x, y0 + 94])
    put('jp_gorinto', 1990, 330, None) if False else None
    for x, y in ((1980, 360), (1980, 560)): put('ny_redlantern', x, y, None)
    # 散落石头
    for _ in range(14):
        x, y = random.randint(80, 2100), random.randint(330, 1060)
        if any(abs(x - o['x']) < 70 and abs(y - o['y']) < 40 for o in objs): continue
        if any(b[0] - 24 < x < b[2] + 24 and b[1] - 24 < y < b[3] + 24 for b in blocks): continue
        if abs(x - CX) < 150 or abs(y - RY) < 70: continue
        put('jp_rock%d' % random.randint(0, 1), x, y, (-12, -8, 12, 0))

    cols, rows = W // CELL, H // CELL
    grid = [[0] * cols for _ in range(rows)]
    for (x0, y0, x1, y1) in blocks:
        for r_ in range(max(0, y0 // CELL), min(rows, y1 // CELL + 1)):
            for c_ in range(max(0, x0 // CELL), min(cols, x1 // CELL + 1)): grid[r_][c_] = 1
    for c_ in range(cols):                                                       # 海：不可走，栈桥可走
        x = c_ * CELL + 4; ys = SEA_Y(x)
        for r_ in range(int(ys // CELL) + 1, rows):
            y = r_ * CELL + 4
            on_pier = any(abs(x - px) < pw // 2 + 2 and y < int(SEA_Y(px)) - 10 + 250 for px, pw in piers)
            if not on_pier: grid[r_][c_] = 1
    for r_ in range(int((RY - 80) // CELL), int((RY + 80) // CELL)):
        for c_ in range(int((CX - 130) // CELL), int((CX + 130) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(300 // CELL), int(1100 // CELL)):
        for c_ in range(int((CX - 40) // CELL), int((CX + 40) // CELL)): grid[r_][c_] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for row in grid for v in row), objs=objs, w=W, h=H,
                start=[CX, RY], boss=[1900, 520], shaman=list(SH), graves=graves)
    return im, sprites, data, SP


def preview(path, scale=1.0, crop=None):
    im, sprites, data, SP = build()
    full = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        spr, ax, ay = SP[o['img']]
        full.alpha_composite(spr, (int(o['x'] - ax), int(o['y'] - ay)))
    glow = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for o in data['objs']:
        if o['img'] == 'ny_lamp':
            for k, rr in enumerate((34, 22, 12)): g.ellipse([o['x'] - rr, o['y'] - 46 - rr * 0.8, o['x'] + rr, o['y'] - 46 + rr * 0.8], fill=(255, 210, 110, 16 + k * 8))
        if o['img'].startswith('ny_house'): g.ellipse([o['x'] - 50, o['y'] - 50, o['x'] + 50, o['y'] + 6], fill=(255, 190, 100, 16))
        if o['img'] == 'ny_shaman': g.ellipse([o['x'] - 60, o['y'] - 50, o['x'] + 60, o['y'] + 40], fill=(70, 230, 140, 18))
        if o['img'] == 'ny_temple': g.ellipse([o['x'] - 120, o['y'] - 90, o['x'] + 120, o['y'] + 10], fill=(255, 150, 90, 22))
    full.alpha_composite(glow)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'ny_preview.png', 0.45)
