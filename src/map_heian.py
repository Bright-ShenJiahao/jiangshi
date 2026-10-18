"""第二章·决战平安京：夜里的平安京（京都）。朱雀大路贯穿南北，北面是大内里（紫宸殿），南面是罗城门，
东北是安倍晴明的阴阳寮（五芒星封印），西边是花街（艺妓茶屋），东南是集市（能面摊、牛车），东缘是鸭川，西南是鸟辺野墓地。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw
import map_jp as J
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW, STRAW, STRAW_D, WALL, WALL_D, PATH, PATH_D, PINK

W, H = 2200, 1600
CELL = 8
TILE, TILE_D, TILE_L = (44, 62, 70), (30, 44, 54), (70, 94, 100)      # 青灰瓦
GREEN, GREEN_D, GREEN_L = (50, 96, 84), (34, 70, 64), (84, 140, 116)  # 宫殿青绿瓦
INDIGO, INDIGO_L = (40, 56, 110), (84, 108, 170)
WHITE = (226, 224, 214)


def roof(d, x0, x1, y_eave, y_top, col, col_d, col_l, w_ext=8, curve=6):
    """歇山/庑殿式大屋顶：梯形 + 瓦垄 + 上翘檐角"""
    d.polygon([(x0 - w_ext, y_eave + 2), (x1 + w_ext, y_eave + 2), (x1 - 6, y_top), (x0 + 6, y_top)], fill=K)
    d.polygon([(x0 - w_ext + 2, y_eave), (x1 + w_ext - 2, y_eave), (x1 - 8, y_top + 2), (x0 + 8, y_top + 2)], fill=col)
    n = max(6, (x1 - x0) // 7)
    for i in range(n + 1):
        t = i / n; xb = x0 - w_ext + 2 + t * (x1 - x0 + 2 * w_ext - 4); xt = x0 + 8 + t * (x1 - x0 - 16)
        d.line([(xb, y_eave - 1), (xt, y_top + 3)], fill=col_d)
    d.line([(x0 + 8, y_top + 2), (x1 - 8, y_top + 2)], fill=col_l, width=2)
    for sx in (-1, 1):                                                       # 檐角上翘
        xe = x0 - w_ext if sx < 0 else x1 + w_ext
        d.polygon([(xe, y_eave + 2), (xe + sx * 7, y_eave - curve), (xe + sx * -2, y_eave - 2)], fill=K)
    d.rectangle([x0 - w_ext + 2, y_eave, x1 + w_ext - 2, y_eave + 2], fill=col_d)


def pillars(d, x0, x1, y0, y1, n, col=RED, gap_open=None):
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i // n
        if gap_open and gap_open[0] < x < gap_open[1] and i not in (0, n): pass
        box(d, x - 3, y0, x + 3, y1, col); d.line([(x - 2, y0 + 1), (x - 2, y1 - 1)], fill=RED_L); d.line([(x + 2, y0 + 1), (x + 2, y1 - 1)], fill=RED_D)
        box(d, x - 5, y1 - 4, x + 5, y1, STONE_D)


def gate(w=200, tiers=2, ruin=False, green=False):
    """门：罗城门(两层，破败) / 朱雀门(一层，青绿瓦)"""
    col, cd, cl = (GREEN, GREEN_D, GREEN_L) if green else (TILE, TILE_D, TILE_L)
    h = 168 if tiers == 2 else 112
    im, d = canvas(w + 40, h); cx = (w + 40) // 2; x0, x1 = 20, w + 20; by = h - 4
    shadow(d, cx, by, w // 2 + 12, 7)
    box(d, x0 - 6, by - 14, x1 + 6, by, STONE_D); d.line([(x0 - 5, by - 13), (x1 + 5, by - 13)], fill=STONE_L)     # 基坛
    for x in range(x0, x1, 18): d.line([(x, by - 12), (x, by - 2)], fill=(70, 68, 86))
    ly0 = by - 62 if tiers == 2 else by - 58
    box(d, x0, ly0, x1, by - 14, WALL_D)                                                                         # 下层墙
    d.rectangle([x0 + 1, ly0 + 1, x1 - 1, ly0 + 5], fill=(60, 44, 46))
    n = 8 if w >= 180 else 6
    # 中央门洞
    gw = w // 3
    box(d, cx - gw // 2, ly0 + 6, cx + gw // 2, by - 14, (14, 10, 20))
    if ruin: d.rectangle([cx - gw // 2 + 4, ly0 + 10, cx + gw // 2 - 4, by - 16], fill=(22, 18, 34))
    pillars(d, x0 + 4, x1 - 4, ly0 + 2, by - 14, n)
    box(d, x0 - 2, ly0 - 4, x1 + 2, ly0 + 5, RED if not ruin else (120, 40, 40))                                  # 阑额
    ye = ly0 - 2
    if tiers == 2:
        roof(d, x0 - 4, x1 + 4, ye, ye - 18, col, cd, cl, 14, 7)
        ux0, ux1 = x0 + 26, x1 - 26; uy1 = ye - 18; uy0 = uy1 - 38
        box(d, ux0, uy0, ux1, uy1, WALL_D)
        pillars(d, ux0 + 3, ux1 - 3, uy0 + 2, uy1, 6)
        for i in range(6):
            wx = ux0 + 12 + i * (ux1 - ux0 - 24) // 5
            box(d, wx - 6, uy0 + 8, wx + 6, uy1 - 10, (56, 38, 70) if ruin else (240, 200, 110))                  # 窗：废墟里是诡异的紫光
            d.line([(wx, uy0 + 9), (wx, uy1 - 11)], fill=WOOD_D)
        d.line([(ux0, uy1 - 4), (ux1, uy1 - 4)], fill=RED_D, width=2)                                              # 栏杆
        roof(d, ux0 - 4, ux1 + 4, uy0 - 2, uy0 - 26, col, cd, cl, 14, 8)
        for sx in (ux0 - 16, ux1 + 16): d.polygon([(sx - 3, uy0 - 26), (sx + 3, uy0 - 26), (sx, uy0 - 36)], fill=(196, 170, 90))   # 鸱尾
    else:
        roof(d, x0 - 4, x1 + 4, ye, ye - 30, col, cd, cl, 14, 8)
        for sx in (x0 - 4, x1 + 4): d.polygon([(sx - 3, ye - 30), (sx + 3, ye - 30), (sx, ye - 40)], fill=(196, 170, 90))
    if ruin:                                                                                                       # 破损：缺角瓦、挂着的破灯笼
        for _ in range(26):
            px, py = random.randint(x0, x1), random.randint(ye - 40, ye)
            d.rectangle([px, py, px + 3, py + 2], fill=(20, 16, 28))
    return im, cx, by


def hall(w=260, h=170, green=True):
    """紫宸殿：宽大的庑殿式屋顶、红柱白墙、前有石阶和两棵树的位置"""
    col, cd, cl = (GREEN, GREEN_D, GREEN_L) if green else (TILE, TILE_D, TILE_L)
    im, d = canvas(w + 40, h); cx = (w + 40) // 2; x0, x1 = 20, w + 20; by = h - 4
    shadow(d, cx, by, w // 2 + 10, 8)
    for i in range(4):
        box(d, cx - 40 - i * 5, by - 4 - i * 6, cx + 40 + i * 5, by - i * 6, STONE if i % 2 else STONE_L)            # 石阶
    box(d, x0 - 8, by - 34, x1 + 8, by - 22, STONE_D)
    box(d, x0, by - 82, x1, by - 34, WHITE)
    for x in range(x0 + 6, x1, 12): d.line([(x, by - 80), (x, by - 36)], fill=(190, 188, 180))                         # 蔀戸格
    for y in (by - 66, by - 52): d.line([(x0 + 1, y), (x1 - 1, y)], fill=(190, 188, 180))
    box(d, cx - 28, by - 78, cx + 28, by - 36, (36, 24, 30))                                                       # 正中门
    d.rectangle([cx - 26, by - 76, cx + 26, by - 40], fill=(244, 196, 100))
    for x in range(cx - 20, cx + 26, 10): d.line([(x, by - 76), (x, by - 40)], fill=WOOD_D)
    pillars(d, x0 + 4, x1 - 4, by - 84, by - 34, 12)
    box(d, x0 - 2, by - 90, x1 + 2, by - 82, RED)
    roof(d, x0 - 6, x1 + 6, by - 88, by - 120, col, cd, cl, 18, 10)
    roof(d, x0 + 26, x1 - 26, by - 120, by - 150, col, cd, cl, 14, 9)
    d.line([(x0 + 34, by - 150), (x1 - 34, by - 150)], fill=(196, 170, 90), width=2)
    for sx in (x0 + 30, x1 - 30): d.polygon([(sx - 3, by - 150), (sx + 3, by - 150), (sx, by - 162)], fill=(196, 170, 90))
    return im, cx, by


def onmyoryo():
    """阴阳寮：中式楼阁，二层带观天台，门前挂着五芒星（桔梗印）的灯"""
    w, h = 180, 150
    im, d = canvas(w + 20, h); cx = (w + 20) // 2; x0, x1 = 10, w + 10; by = h - 4
    shadow(d, cx, by, w // 2, 7)
    box(d, x0 - 4, by - 12, x1 + 4, by, STONE_D)
    box(d, x0, by - 54, x1, by - 12, (58, 52, 76)); pillars(d, x0 + 4, x1 - 4, by - 56, by - 12, 6, col=(70, 62, 110))
    box(d, cx - 16, by - 46, cx + 16, by - 12, (20, 16, 34))
    d.ellipse([cx - 8, by - 42, cx + 8, by - 26], outline=(120, 190, 255)); d.line([(cx - 5, by - 28), (cx, by - 41), (cx + 5, by - 28), (cx - 7, by - 37), (cx + 7, by - 37), (cx - 5, by - 28)], fill=(150, 214, 255))
    for wx in (x0 + 22, x1 - 22): box(d, wx - 9, by - 46, wx + 9, by - 26, (120, 190, 255)); d.line([(wx, by - 46), (wx, by - 26)], fill=(40, 52, 90))
    roof(d, x0 - 2, x1 + 2, by - 58, by - 80, TILE, TILE_D, TILE_L, 14, 7)
    ux0, ux1 = x0 + 34, x1 - 34
    box(d, ux0, by - 112, ux1, by - 80, (58, 52, 76)); pillars(d, ux0 + 3, ux1 - 3, by - 114, by - 80, 3, col=(70, 62, 110))
    box(d, cx - 12, by - 106, cx + 12, by - 86, (30, 40, 90))
    for (sx, sy) in ((cx - 5, by - 98), (cx + 4, by - 102), (cx + 1, by - 92), (cx - 6, by - 90)): d.point((sx, sy), fill=(255, 240, 160))   # 星
    roof(d, ux0 - 2, ux1 + 2, by - 114, by - 138, TILE, TILE_D, TILE_L, 12, 6)
    return im, cx, by


def hunyi():
    """浑天仪（观星仪）"""
    im, d = canvas(44, 56); cx, by = 22, 54
    shadow(d, cx, by, 14)
    box(d, cx - 12, by - 8, cx + 12, by, STONE_D); box(d, cx - 5, by - 18, cx + 5, by - 8, STONE)
    d.ellipse([cx - 17, by - 52, cx + 17, by - 16], outline=K, width=3); d.ellipse([cx - 16, by - 51, cx + 16, by - 17], outline=(190, 160, 80), width=1)
    d.ellipse([cx - 7, by - 52, cx + 7, by - 16], outline=K, width=3); d.ellipse([cx - 6, by - 51, cx + 6, by - 17], outline=(150, 190, 220), width=1)
    d.line([(cx - 17, by - 34), (cx + 17, by - 34)], fill=K, width=3); d.line([(cx - 16, by - 34), (cx + 16, by - 34)], fill=(190, 160, 80))
    d.ellipse([cx - 3, by - 37, cx + 3, by - 31], fill=(120, 190, 255))
    return im, cx, by


def machiya(w=84, var=0, red=False):
    """町屋：深色格子的二层木屋，青灰瓦，挂着蓝染暖帘；red=True 是花街的红格子茶屋，挂满红灯笼"""
    r = random.Random(var * 13 + 5)
    im, d = canvas(w + 16, 112); x0 = 8; cx = (w + 16) // 2; by = 108
    shadow(d, cx, by, w // 2 + 4, 6)
    d.rectangle([x0, by - 90, x0 + w, by - 52], fill=K); d.rectangle([x0 + 1, by - 89, x0 + w - 1, by - 53], fill=(168, 150, 124) if not red else (150, 120, 112))
    for x in range(x0 + 5, x0 + w - 3, 6): d.line([(x, by - 84), (x, by - 60)], fill=(80, 58, 48))                          # 二楼虫笼窗
    d.rectangle([x0 + 8, by - 84, x0 + w - 8, by - 60], outline=(80, 58, 48))
    d.rectangle([x0 + 10, by - 82, x0 + w - 10, by - 62], fill=None)
    for x in range(x0 + 12, x0 + w - 10, 12): d.rectangle([x, by - 82, x + 5, by - 62], fill=(240, 196, 100) if r.random() < (0.7 if red else 0.4) else (70, 50, 44))
    d.polygon([(x0 - 6, by - 52), (x0 + w + 6, by - 52), (x0 + w - 4, by - 66), (x0 + 4, by - 66)], fill=K)               # 中间小檐
    d.polygon([(x0 - 4, by - 53), (x0 + w + 4, by - 53), (x0 + w - 5, by - 65), (x0 + 5, by - 65)], fill=TILE)
    d.rectangle([x0, by - 52, x0 + w, by - 4], fill=K)
    d.rectangle([x0 + 1, by - 51, x0 + w - 1, by - 5], fill=(98, 66, 52) if not red else RED_D)                              # 一楼格子
    for x in range(x0 + 3, x0 + w - 2, 4): d.line([(x, by - 48), (x, by - 8)], fill=(60, 40, 38) if not red else (90, 26, 28))
    for y in (by - 30, by - 14): d.line([(x0 + 2, y), (x0 + w - 2, y)], fill=(60, 40, 38) if not red else (90, 26, 28))
    dx = x0 + w // 2 + (6 if var % 2 else -6)
    d.rectangle([dx - 10, by - 44, dx + 10, by - 5], fill=(30, 22, 30)); d.rectangle([dx - 8, by - 42, dx + 8, by - 6], fill=(244, 196, 100))   # 门里的灯光
    d.rectangle([dx - 11, by - 46, dx + 11, by - 30], fill=INDIGO)                                                                            # 暖帘
    d.line([(dx, by - 46), (dx, by - 30)], fill=K)
    for k in range(3): d.line([(dx - 11, by - 46 + k * 5), (dx + 11, by - 46 + k * 5)], fill=INDIGO_L)
    d.ellipse([dx - 3, by - 41, dx + 3, by - 35], outline=WHITE)
    d.polygon([(x0 - 8, by - 88), (x0 + w + 8, by - 88), (x0 + w - 2, by - 108), (x0 + 2, by - 108)], fill=K)
    d.polygon([(x0 - 6, by - 89), (x0 + w + 6, by - 89), (x0 + w - 3, by - 106), (x0 + 3, by - 106)], fill=TILE)
    for x in range(x0 - 4, x0 + w + 4, 5): d.line([(x, by - 89), (x + (cx - x) // 10, by - 106)], fill=TILE_D)
    d.line([(x0 + 3, by - 106), (x0 + w - 3, by - 106)], fill=TILE_L, width=2)
    if red:
        for i, lx in enumerate(range(x0 + 6, x0 + w, 14)):
            d.line([(lx, by - 53), (lx, by - 50)], fill=K); d.ellipse([lx - 5, by - 50, lx + 5, by - 36], fill=K); d.ellipse([lx - 4, by - 49, lx + 4, by - 37], fill=(236, 86, 70))
    return im, cx, by


def market_stall(kind=0):
    """集市摊：条纹遮阳 + 货物。kind 0 = 能面摊（一排白面具）、1 = 布料/酒摊"""
    im, d = canvas(78, 70); cx, by = 39, 66
    shadow(d, cx, by, 30, 5)
    for x in (cx - 30, cx + 30): box(d, x - 2, 18, x + 2, by - 2, WOOD)
    box(d, cx - 30, by - 22, cx + 30, by - 4, WOOD_D); d.line([(cx - 29, by - 21), (cx + 29, by - 21)], fill=WOOD)
    d.polygon([(cx - 36, 26), (cx + 36, 26), (cx + 30, 8), (cx - 30, 8)], fill=K)
    for i in range(8):
        x = cx - 35 + i * 9; d.polygon([(x, 25), (x + 9, 25), (x + 7, 9), (x + 2, 9)], fill=RED if i % 2 else WHITE)
    for i in range(7): d.polygon([(cx - 35 + i * 10, 26), (cx - 26 + i * 10, 26), (cx - 30 + i * 10, 31)], fill=RED if i % 2 else WHITE)
    if kind == 0:
        for i in range(5):                                                  # 能面
            mx = cx - 24 + i * 12; my = 36
            d.ellipse([mx - 5, my - 2, mx + 5, my + 14], fill=K); d.ellipse([mx - 4, my - 1, mx + 4, my + 13], fill=(236, 232, 218))
            d.line([(mx - 3, my + 4), (mx - 1, my + 5)], fill=K); d.line([(mx + 1, my + 5), (mx + 3, my + 4)], fill=K); d.point((mx, my + 9), fill=(190, 60, 50))
            if i == 2: d.polygon([(mx - 4, my), (mx - 6, my - 5), (mx - 2, my - 1)], fill=(220, 180, 70)); d.polygon([(mx + 4, my), (mx + 6, my - 5), (mx + 2, my - 1)], fill=(220, 180, 70))   # 般若角
    else:
        for i in range(4): d.rectangle([cx - 24 + i * 14, by - 34, cx - 14 + i * 14, by - 22], fill=[INDIGO, (190, 70, 70), (214, 176, 84), (90, 150, 110)][i])
    return im, cx, by


def oxcart():
    """牛车：贵族乘坐的带竹帘车厢"""
    im, d = canvas(78, 54); cx, by = 39, 50
    shadow(d, cx, by, 30, 5)
    box(d, cx - 4, by - 36, cx + 28, by - 12, (46, 40, 60))
    d.polygon([(cx - 8, by - 36), (cx + 32, by - 36), (cx + 26, by - 46), (cx - 2, by - 46)], fill=K); d.polygon([(cx - 6, by - 37), (cx + 30, by - 37), (cx + 25, by - 45), (cx - 1, by - 45)], fill=(80, 106, 94))
    for x in range(cx - 1, cx + 27, 3): d.line([(x, by - 34), (x, by - 14)], fill=(140, 120, 76))
    box(d, cx + 4, by - 30, cx + 20, by - 18, (30, 22, 34)); d.line([(cx + 4, by - 24), (cx + 20, by - 24)], fill=(180, 60, 56))
    d.ellipse([cx + 4, by - 20, cx + 28, by + 2], fill=K); d.ellipse([cx + 6, by - 18, cx + 26, by], fill=WOOD); d.ellipse([cx + 14, by - 10, cx + 18, by - 6], fill=K)
    for a in range(0, 360, 45): d.line([(cx + 16, by - 8), (cx + 16 + 10 * math.cos(math.radians(a)), by - 8 + 10 * math.sin(math.radians(a)))], fill=WOOD_D)
    d.rectangle([cx - 30, by - 22, cx - 6, by - 14], fill=K); d.rectangle([cx - 29, by - 21, cx - 7, by - 15], fill=(52, 40, 40))   # 牛
    d.ellipse([cx - 36, by - 28, cx - 22, by - 16], fill=K); d.ellipse([cx - 35, by - 27, cx - 23, by - 17], fill=(52, 40, 40))
    d.line([(cx - 34, by - 28), (cx - 38, by - 32)], fill=(220, 210, 180), width=2); d.line([(cx - 24, by - 28), (cx - 21, by - 32)], fill=(220, 210, 180), width=2)
    for x in (cx - 26, cx - 10): d.rectangle([x, by - 14, x + 2, by - 2], fill=K)
    return im, cx, by


def brazier():
    """篝火台"""
    im, d = canvas(24, 40); cx, by = 12, 38
    shadow(d, cx, by, 8)
    d.line([(cx - 6, by), (cx - 3, by - 14)], fill=K, width=2); d.line([(cx + 6, by), (cx + 3, by - 14)], fill=K, width=2)
    d.polygon([(cx - 9, by - 24), (cx + 9, by - 24), (cx + 5, by - 14), (cx - 5, by - 14)], fill=K); d.polygon([(cx - 8, by - 24), (cx + 8, by - 24), (cx + 4, by - 15), (cx - 4, by - 15)], fill=(70, 62, 78))
    d.polygon([(cx - 6, by - 24), (cx - 2, by - 36), (cx, by - 28), (cx + 3, by - 38), (cx + 6, by - 24)], fill=(230, 100, 50)); d.polygon([(cx - 3, by - 24), (cx, by - 32), (cx + 3, by - 24)], fill=(255, 210, 110))
    return im, cx, by


def mikoshi_tree():
    """橘树（右近之橘）"""
    im, d = canvas(50, 60); cx, by = 25, 56
    shadow(d, cx, by - 1, 14)
    d.rectangle([cx - 3, by - 20, cx + 3, by], fill=K); d.rectangle([cx - 2, by - 20, cx + 2, by], fill=(70, 50, 44))
    for ox, oy, r in [(0, -32, 17), (-11, -26, 11), (11, -26, 11), (0, -42, 10)]: d.ellipse([cx + ox - r - 1, by + oy - r - 1, cx + ox + r + 1, by + oy + r + 1], fill=K)
    for i, (ox, oy, r) in enumerate([(0, -32, 17), (-11, -26, 11), (11, -26, 11), (0, -42, 10)]): d.ellipse([cx + ox - r, by + oy - r, cx + ox + r, by + oy + r], fill=(40, 92, 74) if i % 2 else (50, 110, 86))
    rr = random.Random(3)
    for _ in range(9):
        ox, oy = rr.randint(-14, 12), rr.randint(22, 50); d.ellipse([cx + ox, by - oy, cx + ox + 3, by - oy + 3], fill=(240, 160, 50))
    return im, cx, by


def kakigaki():
    """竹垣短段"""
    im, d = canvas(40, 26)
    shadow(d, 20, 24, 18, 3)
    for x in range(2, 40, 5): d.rectangle([x, 4, x + 2, 24], fill=K); d.rectangle([x + 1, 5, x + 1, 23], fill=(98, 130, 90))
    d.line([(0, 10), (39, 10)], fill=WOOD_D, width=2); d.line([(0, 18), (39, 18)], fill=WOOD_D, width=2)
    return im, 20, 24


SPRITES = dict(J.SPRITE_FUNCS)
SPRITES.update({
    'hn_rasho': lambda: gate(330, 2, True), 'hn_suzaku': lambda: gate(220, 1, False, True), 'hn_shishin': lambda: hall(280, 180),
    'hn_onmyo': onmyoryo, 'hn_hunyi': hunyi, 'hn_machiya0': lambda: machiya(84, 0), 'hn_machiya1': lambda: machiya(100, 1), 'hn_machiya2': lambda: machiya(72, 2),
    'hn_ochaya0': lambda: machiya(92, 3, True), 'hn_ochaya1': lambda: machiya(108, 4, True), 'hn_stall0': lambda: market_stall(0), 'hn_stall1': lambda: market_stall(1),
    'hn_cart': oxcart, 'hn_brazier': brazier, 'hn_orange': mikoshi_tree, 'hn_fence': kakigaki,
})


def rect_road(d, x0, y0, x1, y1, col=PATH, edge=PATH_D):
    d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], fill=edge); d.rectangle([x0, y0, x1, y1], fill=col)


def build(seed=33):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), (36, 48, 64, 255)); d = ImageDraw.Draw(im)
    blocks = []
    for _ in range(110000): im.putpixel((random.randrange(W), random.randrange(H)), random.choice(J.GROUND) + (255,))
    for _ in range(1200):
        x, y = random.randrange(W), random.randrange(H)
        for dx, hh in ((0, 2), (1, 4), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 84, 82))
    # 北山
    d.rectangle([0, 0, W, 150], fill=(26, 38, 52))
    for k, col in enumerate([(30, 44, 60), (24, 36, 50), (20, 30, 44)]):
        pts = [(0, 150)]
        for x in range(0, W + 40, 40): pts.append((x, 90 - k * 16 + int(34 * math.sin(x / 210 + k * 2) + 16 * math.sin(x / 71 + k))))
        pts.append((W, 150)); d.polygon(pts, fill=col)
    d.rectangle([0, 148, W, 156], fill=K)

    CX = 1100                                                 # 朱雀大路中线
    PAL_Y0, PAL_Y1 = 170, 540                                 # 大内里
    PAL_X0, PAL_X1 = 740, 1460
    # ---- 大内里：白砂院落 + 回廊墙 ----
    d.rectangle([PAL_X0, PAL_Y0, PAL_X1, PAL_Y1], fill=(66, 74, 90))
    for _ in range(26000): im.putpixel((random.randrange(PAL_X0, PAL_X1), random.randrange(PAL_Y0, PAL_Y1)), random.choice([(76, 84, 100, 255), (58, 66, 82, 255), (70, 80, 90, 255)]))
    for sx0, sx1 in ((PAL_X0, CX - 150), (CX + 150, PAL_X1)):                       # 南墙（中间留朱雀门位）
        d.rectangle([sx0, PAL_Y1 - 6, sx1, PAL_Y1 + 22], fill=K); d.rectangle([sx0 + 1, PAL_Y1 - 4, sx1 - 1, PAL_Y1 + 20], fill=WALL_D)
        d.rectangle([sx0 + 1, PAL_Y1 - 4, sx1 - 1, PAL_Y1 + 3], fill=TILE); d.line([(sx0, PAL_Y1 + 4), (sx1, PAL_Y1 + 4)], fill=K)
        for x in range(sx0 + 10, sx1, 22): d.line([(x, PAL_Y1 + 6), (x, PAL_Y1 + 18)], fill=(110, 94, 86))
    for (a, b, c, e) in ((PAL_X0, PAL_Y0 - 6, PAL_X0 + 22, PAL_Y1 + 22), (PAL_X1 - 22, PAL_Y0 - 6, PAL_X1, PAL_Y1 + 22)):
        d.rectangle([a, b, c, e], fill=K); d.rectangle([a + 1, b + 1, c - 1, e - 1], fill=WALL_D); d.rectangle([a + 1, b + 1, c - 1, b + 6], fill=TILE)
    d.rectangle([PAL_X0, PAL_Y0 - 6, PAL_X1, PAL_Y0 + 10], fill=K); d.rectangle([PAL_X0 + 1, PAL_Y0 - 5, PAL_X1 - 1, PAL_Y0 + 9], fill=WALL_D)
    blocks += [(PAL_X0, PAL_Y0 - 6, PAL_X1, PAL_Y0 + 10), (PAL_X0, PAL_Y0, PAL_X0 + 22, PAL_Y1 + 22), (PAL_X1 - 22, PAL_Y0, PAL_X1, PAL_Y1 + 22),
               (PAL_X0, PAL_Y1 - 6, CX - 150, PAL_Y1 + 22), (CX + 150, PAL_Y1 - 6, PAL_X1, PAL_Y1 + 22)]
    # 铺路：宫内中轴石道
    rect_road(d, CX - 40, 340, CX + 40, PAL_Y1 + 24)

    # ---- 朱雀大路 ----
    rect_road(d, CX - 64, PAL_Y1 + 24, CX + 64, H - 30)
    for _ in range(3000):
        x, y = random.randint(CX - 62, CX + 62), random.randint(PAL_Y1 + 26, H - 32)
        im.putpixel((x, y), random.choice([(104, 96, 100, 255), (132, 122, 122, 255)]))
    # ---- 二条大路（东西） ----
    ROAD_Y = 880
    rect_road(d, 120, ROAD_Y - 38, W - 120, ROAD_Y + 38)
    # 中央广场（十字口，加宽）
    rect_road(d, CX - 150, ROAD_Y - 90, CX + 150, ROAD_Y + 90)
    for _ in range(900): im.putpixel((random.randint(CX - 146, CX + 146), random.randint(ROAD_Y - 86, ROAD_Y + 86)), random.choice([(104, 96, 100, 255), (132, 122, 122, 255)]))
    # ---- 鸭川（东缘） ----
    RX = 2090
    def river_x(y): return RX + 22 * math.sin(y / 130) + 10 * math.sin(y / 47)
    for y in range(156, H):
        cx = river_x(y)
        d.line([(cx - 46, y), (cx + 46, y)], fill=K); d.line([(cx - 44, y), (cx + 44, y)], fill=(24, 46, 84))
        d.point((cx - 44 + (y * 7) % 88, y), fill=(60, 110, 160))
    for _ in range(1500):
        y = random.randint(160, H - 1); x = int(river_x(y) + random.randint(-42, 42)); im.putpixel((x, y), random.choice([(34, 62, 104, 255), (18, 36, 70, 255), (50, 90, 140, 255)]))
    # 五条大桥（木桥，擬宝珠栏杆）
    BY = ROAD_Y
    d.rectangle([int(river_x(BY)) - 80, BY - 22, int(river_x(BY)) + 80, BY + 22], fill=K)
    d.rectangle([int(river_x(BY)) - 78, BY - 20, int(river_x(BY)) + 78, BY + 20], fill=(104, 76, 60))
    for x in range(int(river_x(BY)) - 76, int(river_x(BY)) + 78, 8): d.line([(x, BY - 19), (x, BY + 19)], fill=(80, 58, 48))
    for yy in (BY - 22, BY + 22):
        d.line([(int(river_x(BY)) - 80, yy), (int(river_x(BY)) + 80, yy)], fill=RED, width=3)
        for x in range(int(river_x(BY)) - 76, int(river_x(BY)) + 80, 20): d.ellipse([x - 3, yy - 8, x + 3, yy - 2], fill=(210, 176, 90))
    for x0_, x1_ in ((int(river_x(150)) - 46, int(river_x(BY)) + 46),):
        pass
    # 鸭川碰撞：整段水体封死，只留桥面
    water = []
    # ---- 西南：鸟辺野墓地 ----
    for _ in range(26000):
        x, y = random.randrange(140, 880), random.randrange(1260, 1560)
        if (x - 510) ** 2 / 360 ** 2 + (y - 1410) ** 2 / 160 ** 2 < 1 and im.getpixel((x, y))[:3] in J.GROUND: im.putpixel((x, y), random.choice([(44, 50, 70, 255), (38, 42, 62, 255), (50, 58, 76, 255)]))
    J.road(d, [(CX - 40, 1360), (860, 1380), (700, 1400), (560, 1400)], 36)
    # ---- 花街小巷（西）、市（东南）的路面 ----
    J.road(d, [(CX - 64, 700), (760, 700), (360, 700)], 30)
    J.road(d, [(CX - 64, 1130), (760, 1130), (330, 1130)], 30)
    J.road(d, [(CX + 64, 1130), (1500, 1130), (1900, 1130)], 30)
    J.road(d, [(CX + 64, 700), (1500, 700), (1900, 700)], 30)
    # ---- 阴阳寮院落（东北）----
    OX0, OY0, OX1, OY1 = 1520, 590, 1960, 840
    d.rectangle([OX0, OY0, OX1, OY1], fill=(50, 58, 80))
    for _ in range(9000): im.putpixel((random.randrange(OX0, OX1), random.randrange(OY0, OY1)), random.choice([(58, 66, 92, 255), (44, 52, 74, 255), (52, 62, 86, 255)]))
    for (a, b, c, e) in ((OX0, OY0, OX1, OY0 + 8), (OX0, OY1 - 8, 1660, OY1), (1720, OY1 - 8, OX1, OY1), (OX0, OY0, OX0 + 8, OY1), (OX1 - 8, OY0, OX1, OY1)):
        d.rectangle([a - 1, b - 1, c + 1, e + 1], fill=K); d.rectangle([a, b, c, e], fill=WALL_D); d.rectangle([a, b, c, b + 2], fill=TILE) if e - b < 12 else None
    blocks += [(OX0, OY0, OX1, OY0 + 8), (OX0, OY1 - 8, 1660, OY1), (1720, OY1 - 8, OX1, OY1), (OX0, OY0, OX0 + 8, OY1), (OX1 - 8, OY0, OX1, OY1)]
    # 五芒星封印（桔梗印）
    SEAL = (1740, 740)
    for rr, col in ((78, (30, 50, 100)), (74, (70, 120, 200)), (68, (30, 50, 100))): d.ellipse([SEAL[0] - rr, SEAL[1] - rr * 0.62, SEAL[0] + rr, SEAL[1] + rr * 0.62], outline=col, width=2)
    pts = [(SEAL[0] + 70 * math.cos(math.radians(-90 + i * 72)), SEAL[1] + 70 * 0.62 * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
    for i in range(5): d.line([pts[i], pts[(i + 2) % 5]], fill=(110, 180, 255), width=2)
    for i in range(5): d.ellipse([pts[i][0] - 3, pts[i][1] - 3, pts[i][0] + 3, pts[i][1] + 3], fill=(220, 240, 255))
    d.ellipse([SEAL[0] - 4, SEAL[1] - 3, SEAL[0] + 4, SEAL[1] + 3], fill=(220, 240, 255))
    J.road(d, [(1680, OY1), (1680, ROAD_Y + 38)], 36)

    # ---- 神泉苑（西北池苑，红桥）----
    NX, NY, NRX, NRY = 400, 390, 190, 110
    d.ellipse([NX - NRX - 4, NY - NRY - 4, NX + NRX + 4, NY + NRY + 4], fill=K); d.ellipse([NX - NRX, NY - NRY, NX + NRX, NY + NRY], fill=(24, 44, 78))
    for _ in range(3500):
        a_, r_ = random.random() * 6.283, random.random() ** 0.5
        im.putpixel((int(NX + NRX * r_ * math.cos(a_)), int(NY + NRY * r_ * math.sin(a_))), random.choice([(32, 58, 98, 255), (20, 38, 70, 255), (44, 78, 120, 255)]))
    for _ in range(22):
        a_, r_ = random.random() * 6.283, random.random() ** 0.5 * 0.85; x, y = int(NX + NRX * r_ * math.cos(a_)), int(NY + NRY * r_ * math.sin(a_))
        d.ellipse([x - 7, y - 3, x + 7, y + 3], fill=(40, 100, 80)); d.line([(x, y), (x + 7, y)], fill=(24, 44, 78))
    for i in range(-NRX - 6, NRX + 7):                                    # 红色平桥，中间拱起
        t = i / (NRX + 6); yy = NY - int(10 * (1 - t * t))
        d.line([(NX + i, yy - 5), (NX + i, yy + 6)], fill=RED if abs(i) % 10 > 1 else RED_D)
    for yy_off in (-7, 7):
        for i in range(-NRX - 6, NRX + 7, 14):
            t = i / (NRX + 6); yy = NY - int(10 * (1 - t * t)); d.rectangle([NX + i - 1, yy + yy_off - 8, NX + i + 1, yy + yy_off], fill=RED_D)
    NPOND = (NX, NY, NRX, NRY)
    # ---- 伏见稻荷（东南）：千本鸟居小径 ----
    d_road = [(1300, 1420), (1900, 1420)]
    J.road(d, d_road, 34)
    # ---- 边界 ----
    for x in range(0, W, 20):
        for y0 in (0, H - 20): d.ellipse([x - 12, y0 - 6 + random.randint(-4, 4), x + 12, y0 + 22], fill=(22, 40, 48))
    for y in range(0, H, 20): d.ellipse([-6 + random.randint(-4, 4), y - 12, 22, y + 12], fill=(22, 40, 48))
    blocks += [(0, 0, W, 24), (0, H - 20, W, H), (0, 0, 22, H), (W - 22, 0, W, H)]

    # ---------------- 物件 ----------------
    SP = {k: f() for k, f in SPRITES.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    # 大内里
    put('hn_shishin', CX, 430, (-130, -80, 130, 0))
    put('jp_sakura0', CX - 130, 470, (-6, -6, 6, 0)); put('hn_orange', CX + 130, 470, (-6, -6, 6, 0))   # 左近の桜 / 右近の橘
    put('hn_suzaku', CX, PAL_Y1 + 24, None); blocks += [(CX - 150, PAL_Y1 - 6, CX - 100, PAL_Y1 + 22), (CX + 100, PAL_Y1 - 6, CX + 150, PAL_Y1 + 22)]
    for x in (CX - 300, CX - 220, CX + 220, CX + 300): put('jp_lantern', x, 480, (-5, -5, 5, 0))
    for x in (CX - 330, CX + 330): put('jp_willow', x, 330, (-5, -6, 5, 0))
    # 朱雀大路：柳树与石灯笼相间
    for i, y in enumerate(range(PAL_Y1 + 90, H - 90, 100)):
        if abs(y - ROAD_Y) < 130: continue
        for sx in (-86, 86):
            put('jp_willow' if (i % 2 == 0) else 'jp_lantern', CX + sx, y, (-5, -6, 5, 0))
    # 十字口
    for dx, dy in ((-170, -100), (170, -100), (-170, 110), (170, 110)): put('hn_brazier', CX + dx, ROAD_Y + dy, (-6, -6, 6, 0))
    put('jp_torii', CX, ROAD_Y - 220, None); blocks += [(CX - 22, ROAD_Y - 232, CX - 14, ROAD_Y - 220), (CX + 14, ROAD_Y - 232, CX + 22, ROAD_Y - 220)]
    # 罗城门（南）
    put('hn_rasho', CX, H - 24, None)
    blocks += [(CX - 170, H - 90, CX - 64, H - 24), (CX + 64, H - 90, CX + 170, H - 24)]
    for dx in (-130, 130): put('hn_brazier', CX + dx, H - 120, (-6, -6, 6, 0))
    # 阴阳寮
    put('hn_onmyo', 1700, 662, (-86, -50, 86, 0)); put('hn_hunyi', 1580, 770, (-10, -8, 10, 0)); put('hn_hunyi', 1880, 770, (-10, -8, 10, 0))
    for dx, dy in ((-92, -6), (92, -6), (-60, 60), (60, 60)): put('hn_brazier', SEAL[0] + dx, SEAL[1] + dy, (-6, -6, 6, 0))
    put('jp_sakura1', 1580, 640, (-5, -6, 5, 0)); put('jp_sakura0', 1880, 640, (-5, -6, 5, 0))
    # 花街（西）：两排红格子茶屋 + 町屋
    xs = 200
    for k, x in enumerate((230, 350, 470, 590, 700)):
        put('hn_ochaya%d' % (k % 2), x, 668, (-44, -40, 44, 0)); put('hn_ochaya%d' % ((k + 1) % 2), x, 790, None)
    for x in (230, 350, 470, 590, 700): blocks.append((x - 44, 760, x + 44, 790))
    for k, x in enumerate((230, 360, 500, 640)):
        put('hn_machiya%d' % (k % 3), x, 1098, (-42, -40, 42, 0)); put('hn_machiya%d' % ((k + 1) % 3), x, 1230, (-42, -40, 42, 0))
    put('jp_willow', 790, 760, (-5, -6, 5, 0)); put('jp_willow', 790, 1060, (-5, -6, 5, 0))
    for x in (300, 420, 560, 680): put('jp_chochin', x, 740, None)
    # 市（东南）
    for k, (x, y) in enumerate(((1240, 1050), (1360, 1050), (1480, 1050), (1620, 1050), (1760, 1050), (1300, 1230), (1440, 1230), (1580, 1230), (1720, 1230))):
        put('hn_stall%d' % (1 if k % 3 else 0), x, y, (-32, -22, 32, 0))
    put('hn_cart', 1860, 1190, (-30, -16, 30, 0)); put('hn_cart', 1230, 1300, (-30, -16, 30, 0))
    put('hn_machiya0', 1860, 980, (-42, -40, 42, 0)); put('hn_machiya1', 1960, 1100, (-50, -40, 50, 0))
    # 东侧町屋（二条大路以北）
    for x in (1240, 1360):
        put('hn_machiya%d' % (x % 3), x, 668, (-44, -40, 44, 0))
    for x, y in ((190, 360), (610, 330), (210, 470), (600, 470), (400, 520)): put('jp_willow', x, y, (-5, -6, 5, 0))
    put('jp_rock0', 250, 280, (-12, -8, 12, 0)); put('jp_rock1', 560, 290, (-12, -8, 12, 0))
    # 贺茂森林 + 神社（东北，大内里与阴阳寮之间）
    put('jp_haiden', 1750, 470, (-62, -80, 62, 0)); put('jp_komaL', 1686, 492, (-8, -6, 8, 0)); put('jp_komaR', 1814, 492, (-8, -6, 8, 0))
    for x, y in ((1560, 250), (1640, 330), (1560, 430), (1860, 260), (1940, 350), (1900, 450), (1520, 340), (1980, 250), (1700, 230), (1800, 280)): put('jp_cedar', x, y, (-5, -6, 5, 0))
    for x in (1690, 1810): put('jp_lantern', x, 520, (-5, -5, 5, 0))
    put('jp_torii', 1750, 545, None); blocks += [(1750 - 24, 534, 1750 - 16, 545), (1750 + 16, 534, 1750 + 24, 545)]
    for i, x in enumerate(range(1340, 1900, 56)): put('jp_torii', x, 1440, None); blocks += [(x - 22, 1428, x - 14, 1440), (x + 14, 1428, x + 22, 1440)]
    for x in (1300, 1920): put('jp_fox', x, 1400, (-7, -5, 7, 0))
    for x, y in ((1400, 1330), (1600, 1520), (1800, 1340), (1900, 1510), (1250, 1500)): put('jp_cedar', x, y, (-5, -6, 5, 0))
    # 樱 / 柳 / 灯
    for x, y in ((1020, 1260), (1180, 1290), (900, 580), (1300, 580), (980, 1420), (1220, 1430), (460, 930), (1680, 940)): put('jp_sakura%d' % (x % 2), x, y, (-5, -6, 5, 0))
    # 鸟辺野墓地
    graves = []
    for r_ in range(5):
        for c_ in range(10):
            x, y = 220 + c_ * 62 + (r_ % 2) * 20, 1320 + r_ * 50
            if (x - 510) ** 2 / 360 ** 2 + (y - 1410) ** 2 / 160 ** 2 > 1: continue
            if abs(y - 1400) < 22 and x > 540: continue
            if random.random() < 0.15: continue
            x += random.randint(-6, 6); y += random.randint(-5, 5)
            put('jp_grave%d' % random.randint(0, 2), x, y, (-8, -6, 8, 0)); graves.append([x, y])
            if random.random() < 0.3: put('jp_sotoba', x + 14, y + 4, None)
    put('jp_gorinto', 180, 1330, (-9, -6, 9, 0)); put('jp_jizo', 330, 1290, (-6, -5, 6, 0)); put('jp_jizo', 352, 1294, (-6, -5, 6, 0))
    # 零散石头/竹垣
    for _ in range(26):
        x, y = random.randint(60, 2040), random.randint(220, 1540)
        if any(abs(x - o['x']) < 60 and abs(y - o['y']) < 40 for o in objs): continue
        if any(b[0] - 24 < x < b[2] + 24 and b[1] - 24 < y < b[3] + 24 for b in blocks): continue
        if abs(x - CX) < 140 or abs(y - ROAD_Y) < 100: continue
        put('jp_rock%d' % random.randint(0, 1), x, y, (-12, -8, 12, 0))

    # ---------------- 通行网格 ----------------
    cols, rows = W // CELL, H // CELL
    grid = [[0] * cols for _ in range(rows)]
    for (x0, y0, x1, y1) in blocks:
        for r_ in range(max(0, y0 // CELL), min(rows, y1 // CELL + 1)):
            for c_ in range(max(0, x0 // CELL), min(cols, x1 // CELL + 1)): grid[r_][c_] = 1
    for r_ in range(rows):                                   # 鸭川：水面不可走，桥面可走
        y = r_ * CELL + 4
        if y < 156: continue
        cx = river_x(y)
        for c_ in range(cols):
            x = c_ * CELL + 4
            if abs(x - cx) < 46 and abs(y - BY) > 24: grid[r_][c_] = 1
    for r_ in range(rows):                                   # 神泉苑池塘：水面不可走，桥面可走
        for c_ in range(cols):
            x, y = c_ * CELL + 4, r_ * CELL + 4
            if ((x - NPOND[0]) / NPOND[2]) ** 2 + ((y - NPOND[1]) / NPOND[3]) ** 2 < 1.0 and abs(y - NPOND[1]) > 12: grid[r_][c_] = 1
    for r_ in range(int((ROAD_Y - 90) // CELL), int((ROAD_Y + 90) // CELL)):           # 出生广场、大路保持畅通
        for c_ in range(int((CX - 150) // CELL), int((CX + 150) // CELL)): grid[r_][c_] = 0
    for r_ in range(int((PAL_Y1 + 20) // CELL), int((H - 30) // CELL)):
        for c_ in range(int((CX - 64) // CELL), int((CX + 64) // CELL)):
            if not (r_ * CELL > H - 130): grid[r_][c_] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for row in grid for v in row), objs=objs, w=W, h=H,
                start=[CX, ROAD_Y], boss=[CX, 400], seal=list(SEAL), graves=graves)
    return im, sprites, data, SP


def preview(path, scale=1.0, crop=None):
    im, sprites, data, SP = build()
    full = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        spr, ax, ay = SP[o['img']]
        full.alpha_composite(spr, (int(o['x'] - ax), int(o['y'] - ay)))
    glow = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for o in data['objs']:
        if o['img'] in ('jp_lantern', 'jp_chochin'):
            for k, rr in enumerate((30, 20, 11)): g.ellipse([o['x'] - rr, o['y'] - 24 - rr * 0.8, o['x'] + rr, o['y'] - 24 + rr * 0.8], fill=(255, 196, 100, 16 + k * 8))
        if o['img'] == 'hn_brazier':
            for k, rr in enumerate((44, 28, 14)): g.ellipse([o['x'] - rr, o['y'] - 30 - rr * 0.8, o['x'] + rr, o['y'] - 30 + rr * 0.8], fill=(255, 150, 70, 14 + k * 9))
        if o['img'] in ('hn_ochaya0', 'hn_ochaya1'): g.ellipse([o['x'] - 70, o['y'] - 60, o['x'] + 70, o['y'] + 10], fill=(255, 130, 90, 22))
    sx, sy = data['seal']
    for k, rr in enumerate((90, 60, 30)): g.ellipse([sx - rr, sy - rr * 0.62, sx + rr, sy + rr * 0.62], fill=(100, 170, 255, 14 + k * 8))
    full.alpha_composite(glow)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'heian_preview.png', 0.5)
