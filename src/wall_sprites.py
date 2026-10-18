"""可被怪群推倒的围墙：分段精灵（石墙 / 铁艺围墙）与倒塌后的残骸。
每一段围墙是一张小图，游戏里按深度排序绘制；碰撞矩形另存在地图数据里，倒塌时从通行网格中拿掉。"""
import random
from PIL import Image, ImageDraw

K = (24, 14, 30)
ST_LIP, ST_FACE, ST_LINE, ST_SHADE = (150, 144, 154), (120, 112, 122), (96, 90, 102), (84, 78, 92)
BR_FACE, BR_LIGHT, BR_SHADE, BR_LINE = (112, 104, 110), (146, 138, 146), (82, 76, 86), (90, 84, 92)
IR_D, IR_H, IR_R = (34, 30, 42), (84, 78, 98), (52, 48, 64)


def _new(w, h):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


# ---------------- 石墙（房屋院墙） ----------------
# 每个构造函数返回 (图, dx, dy)：图的左上角 = (矩形左, 矩形上) - (dx, dy)
def stone_h(L, first=False, last=False):
    """水平石墙一段（矩形高 8）：上 3 行压顶，下 6 行墙面；只有首段画左轮廓、末段画右轮廓，段与段之间留一道接缝"""
    lf, rt = (1 if first else 0), (1 if last else 0)
    body = L + (1 if last else 0)
    W, H = lf + body + rt, 11
    im, d = _new(W, H)
    d.rectangle([0, 0, W - 1, 0], fill=K); d.rectangle([0, H - 1, W - 1, H - 1], fill=K)
    if lf: d.line([(0, 0), (0, H - 1)], fill=K)
    if rt: d.line([(W - 1, 0), (W - 1, H - 1)], fill=K)
    x0, x1 = lf, lf + body - 1
    d.rectangle([x0, 1, x1, 3], fill=ST_LIP); d.rectangle([x0, 4, x1, H - 2], fill=ST_FACE)
    d.line([(x0, 3), (x1, 3)], fill=ST_LINE); d.line([(x0, 7), (x1, 7)], fill=ST_LINE); d.line([(x0, H - 2), (x1, H - 2)], fill=ST_SHADE)
    for x in range(x0 + 5, x1, 9): d.line([(x, 4), (x, 6)], fill=ST_LINE)
    for x in range(x0 + 9, x1, 9): d.line([(x, 8), (x, 9)], fill=ST_LINE)
    if not first: d.line([(x0, 1), (x0, H - 2)], fill=ST_LINE)          # 接缝
    return im, lf, 1


def stone_v(L, first=False, last=False):
    """竖直石墙一段（矩形宽 6）：顶端一段带压顶，段间一道横缝"""
    te, be = (4 if first else 0), (1 if last else 0)
    W, H = 9, te + L + 1 + be
    im, d = _new(W, H)
    d.line([(0, 0), (0, H - 1)], fill=K); d.line([(W - 1, 0), (W - 1, H - 1)], fill=K)
    if first: d.line([(0, 0), (W - 1, 0)], fill=K)
    if last: d.line([(0, H - 1), (W - 1, H - 1)], fill=K)
    y0, y1 = te, te + L
    d.rectangle([1, y0, W - 2, y1], fill=ST_FACE)
    if first: d.rectangle([1, 1, W - 2, 3], fill=ST_LIP); d.line([(1, 3), (W - 2, 3)], fill=ST_LINE)
    d.line([(1, y0), (1, y1)], fill=ST_LIP); d.line([(W - 2, y0), (W - 2, y1)], fill=ST_SHADE)
    if not first: d.line([(1, y0), (W - 2, y0)], fill=ST_LINE)
    for y in range(y0 + 6, y1, 6): d.line([(2, y), (W - 3, y)], fill=ST_LINE)
    return im, 1, te


# ---------------- 铁艺围墙：砖柱 + 低砖基 + 铁栏杆（参考墓园围墙） ----------------
def _pillar(d, cx, top, bot):
    """砖柱：宽 6，柱帽宽 8"""
    d.rectangle([cx - 4, top, cx + 3, top + 3], fill=K); d.rectangle([cx - 3, top + 1, cx + 2, top + 2], fill=BR_LIGHT)
    d.rectangle([cx - 3, top + 3, cx + 2, bot], fill=K); d.rectangle([cx - 2, top + 4, cx + 1, bot - 1], fill=BR_FACE)
    d.line([(cx - 2, top + 4), (cx - 2, bot - 1)], fill=BR_LIGHT); d.line([(cx + 1, top + 4), (cx + 1, bot - 1)], fill=BR_SHADE)
    for y in range(top + 8, bot - 1, 5): d.line([(cx - 2, y), (cx + 1, y)], fill=BR_LINE)


def iron_h(L, last=False):
    """水平铁艺围墙一段。矩形 x0..x0+L，底边在 y1+1；画布 x=4 对应 x0；左边总有砖柱，最后一段右边也有。"""
    W = L + 9 if last else L + 5
    H = 34
    im, d = _new(W, H)
    ox = 4
    x_end = ox + L                                    # 本段右端 x
    # 低砖基
    d.rectangle([ox, 26, x_end, 33], fill=K); d.rectangle([ox, 27, x_end, 32], fill=BR_FACE)
    d.line([(ox, 27), (x_end, 27)], fill=BR_LIGHT); d.line([(ox, 28), (x_end, 28)], fill=BR_LIGHT); d.line([(ox, 32), (x_end, 32)], fill=BR_SHADE)
    d.line([(ox, 30), (x_end, 30)], fill=BR_LINE)
    for x in range(ox + 5, x_end, 9): d.line([(x, 28), (x, 29)], fill=BR_LINE)
    for x in range(ox + 9, x_end, 9): d.line([(x, 31), (x, 31)], fill=BR_LINE)
    # 栏杆
    x_lo, x_hi = ox + 4, x_end - 4 if not last else x_end - 4
    xs = list(range(x_lo + 1, x_hi, 4))
    d.line([(x_lo, 12), (x_hi, 12)], fill=IR_D); d.line([(x_lo, 13), (x_hi, 13)], fill=IR_R)
    d.line([(x_lo, 23), (x_hi, 23)], fill=IR_D); d.line([(x_lo, 24), (x_hi, 24)], fill=IR_R)
    for i, x in enumerate(xs):
        top = 4 if i % 2 == 0 else 6
        d.rectangle([x, top, x + 1, 25], fill=IR_D); d.line([(x, top), (x, 25)], fill=IR_H)
        d.point((x, top - 1), fill=IR_D)                                  # 矛尖
    for x in range(x_lo + 8, x_hi - 3, 8):                                # 圆环饰
        d.ellipse([x - 3, 15, x + 3, 21], outline=IR_D); d.point((x - 2, 16), fill=IR_H)
    # 砖柱
    _pillar(d, ox, 1, 33)
    if last: _pillar(d, ox + L, 1, 33)
    return im, 4, 26


def iron_v(L, last=False):
    """竖直铁艺围墙一段（东西向看过去，是一排立着的铁杆）。矩形 x0..x0+6，y 方向 L；画布 x=3 对应 x0；y=24 对应 ya。"""
    W, H = 12, L + 29
    im, d = _new(W, H)
    top0 = 24                                          # 矩形顶端所在行
    # 低砖基（一条竖着的砖带）
    d.rectangle([3, top0, 9, top0 + L + 1], fill=K); d.rectangle([4, top0 + 1, 8, top0 + L], fill=BR_FACE)
    d.line([(4, top0 + 1), (4, top0 + L)], fill=BR_LIGHT); d.line([(8, top0 + 1), (8, top0 + L)], fill=BR_SHADE)
    for y in range(top0 + 4, top0 + L, 6): d.line([(5, y), (7, y)], fill=BR_LINE)
    # 立杆：一根根杆子的底部落在砖带上，杆顶往上 14 格
    for t in range(2, L, 5):
        y = top0 + t
        d.rectangle([5, y - 14, 6, y], fill=IR_D); d.line([(5, y - 14), (5, y)], fill=IR_H); d.point((5, y - 15), fill=IR_D)
    # 上下横梁（斜着看是两条竖线）
    d.line([(6, top0 - 12), (6, top0 + L - 12)], fill=IR_R); d.line([(6, top0 - 4), (6, top0 + L - 4)], fill=IR_R)
    _pillar(d, 6, top0 - 24, top0 + 4)
    if last: _pillar(d, 6, top0 + L - 24, top0 + L + 4)
    return im, 3, 24


# ---------------- 倒塌后的残骸 ----------------
def rubble(kind, orient, L, seed=1):
    """kind 's' 石墙 / 'i' 铁艺；返回以段中心为中心的残骸图"""
    r = random.Random(seed * 97 + L)
    A, B = (L + 10, 14) if orient == 'h' else (14, L + 10)
    im, d = _new(A, B)
    pal = [ST_FACE, ST_LIP, ST_LINE, BR_FACE, BR_LIGHT]
    n = L // 3 + 3
    for _ in range(n):
        w, h = r.randint(2, 5), r.randint(2, 4)
        x, y = (r.randint(0, A - w), r.randint(2, B - h)) if orient == 'h' else (r.randint(2, A - w), r.randint(0, B - h))
        d.rectangle([x - 1, y - 1, x + w, y + h], fill=K); d.rectangle([x, y, x + w - 1, y + h - 1], fill=r.choice(pal))
        d.line([(x, y + h - 1), (x + w - 1, y + h - 1)], fill=ST_SHADE)
    if kind == 'i':
        for _ in range(max(3, L // 8)):                 # 倒在地上的铁杆
            ln = r.randint(8, 13)
            if orient == 'h': x0 = r.randint(0, A - ln); y0 = r.randint(3, B - 4); x1, y1 = x0 + ln, y0 + r.randint(-3, 3)
            else: y0 = r.randint(0, B - ln); x0 = r.randint(3, A - 4); y1, x1 = y0 + ln, x0 + r.randint(-3, 3)
            d.line([(x0, y0), (x1, y1)], fill=IR_D, width=2); d.point((x0, y0), fill=IR_H)
    return im
