"""第五章·地底天宫（秦始皇陵）：巨大的地下空腔里，一座座石台悬浮在虚空中，彼此用悬浮的台阶、吊桥相连。
自南向北——墓道口 → 兵马俑大军台 → 悬浮台阶 → 浮空宫殿（大殿）→ 悬浮台阶 → 主墓室（水银海、星象穹顶）；东西两侧是悬空的石墙迷宫。脚下深处是发光的水银河。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw
import map_jp as J
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW

W, H = 2400, 2100
CELL = 8
FLOOR = [(34, 42, 46), (30, 38, 44), (38, 46, 50)]
WALL_T, WALL_F, WALL_D = (92, 96, 106), (58, 62, 74), (40, 44, 56)
GOLD, GOLD_D, GOLD_L = (214, 176, 80), (150, 116, 50), (246, 220, 140)
BRONZE, BRONZE_D, PATINA = (140, 108, 70), (96, 72, 50), (70, 140, 116)
MERC, MERC_D, MERC_L = (148, 168, 190), (96, 114, 138), (222, 236, 248)
LAC, LAC_R = (34, 26, 34), (150, 40, 44)
FLAME = (90, 230, 220)
CLAY, CLAY_D, CLAY_L = (150, 108, 88), (108, 74, 64), (186, 142, 112)


def warrior(var=0):
    """兵马俑：站姿陶俑，铠甲片、发髻、石座"""
    r = random.Random(var)
    im, d = canvas(24, 52); cx = 12; by = 50
    shadow(d, cx, by, 9, 3)
    box(d, cx - 8, by - 5, cx + 8, by, (96, 88, 90))
    d.rectangle([cx - 5, by - 18, cx - 1, by - 5], fill=K); d.rectangle([cx + 1, by - 18, cx + 5, by - 5], fill=K)
    d.rectangle([cx - 4, by - 17, cx - 2, by - 6], fill=CLAY_D); d.rectangle([cx + 2, by - 17, cx + 4, by - 6], fill=CLAY_D)
    d.rectangle([cx - 8, by - 36, cx + 8, by - 17], fill=K); d.rectangle([cx - 7, by - 35, cx + 7, by - 18], fill=CLAY)
    for y in range(by - 33, by - 19, 4):
        for x in range(cx - 6, cx + 6, 4): d.rectangle([x, y, x + 2, y + 2], fill=CLAY_L); d.point((x + 3, y + 3), fill=CLAY_D)
    d.rectangle([cx - 7, by - 24, cx + 7, by - 22], fill=(150, 60, 56))
    d.rectangle([cx - 11, by - 34, cx - 8, by - 22], fill=K); d.rectangle([cx + 8, by - 34, cx + 11, by - 22], fill=K)
    d.rectangle([cx - 10, by - 33, cx - 9, by - 23], fill=CLAY_D); d.rectangle([cx + 9, by - 33, cx + 10, by - 23], fill=CLAY_D)
    d.ellipse([cx - 6, by - 46, cx + 6, by - 33], fill=K); d.ellipse([cx - 5, by - 45, cx + 5, by - 34], fill=CLAY_L)
    d.rectangle([cx - 2, by - 51, cx + 2, by - 45], fill=K); d.rectangle([cx - 1, by - 50, cx + 1, by - 46], fill=CLAY_D)   # 发髻
    d.point((cx - 2, by - 40), fill=K); d.point((cx + 2, by - 40), fill=K); d.line([(cx - 2, by - 37), (cx + 2, by - 37)], fill=CLAY_D)
    if var % 2: d.line([(cx + 12, by - 50), (cx + 12, by - 6)], fill=K, width=2); d.line([(cx + 12, by - 50), (cx + 12, by - 6)], fill=BRONZE, width=1); d.polygon([(cx + 10, by - 50), (cx + 14, by - 50), (cx + 12, by - 58)], fill=PATINA)  # 持戈
    return im, cx, by


def chariot():
    """青铜车马（铜车马）"""
    im, d = canvas(84, 58); cx, by = 42, 56
    shadow(d, cx, by, 32, 4)
    for wx in (cx - 8, cx + 14):
        d.ellipse([wx - 12, by - 26, wx + 12, by - 2], fill=K); d.ellipse([wx - 10, by - 24, wx + 10, by - 4], fill=BRONZE); d.ellipse([wx - 3, by - 17, wx + 3, by - 11], fill=K)
        for a in range(0, 360, 45): d.line([(wx, by - 14), (wx + 9 * math.cos(math.radians(a)), by - 14 + 9 * math.sin(math.radians(a)))], fill=BRONZE_D)
    box(d, cx - 14, by - 40, cx + 22, by - 18, PATINA); d.polygon([(cx - 18, by - 40), (cx + 26, by - 40), (cx + 18, by - 52), (cx - 10, by - 52)], fill=K); d.polygon([(cx - 16, by - 41), (cx + 24, by - 41), (cx + 17, by - 51), (cx - 9, by - 51)], fill=BRONZE)
    d.rectangle([cx - 8, by - 36, cx + 14, by - 24], fill=(24, 30, 34)); d.line([(cx + 22, by - 20), (cx + 40, by - 18)], fill=K, width=2)
    d.rectangle([cx + 36, by - 28, cx + 52, by - 14], fill=K); d.rectangle([cx + 37, by - 27, cx + 51, by - 15], fill=BRONZE); d.ellipse([cx + 46, by - 36, cx + 58, by - 24], fill=K); d.ellipse([cx + 47, by - 35, cx + 57, by - 25], fill=BRONZE)
    return im, cx, by


def lamp():
    """人鱼膏长明灯：青铜灯台，青绿色火焰"""
    im, d = canvas(20, 52); cx, by = 10, 50
    shadow(d, cx, by, 7, 2)
    box(d, cx - 6, by - 6, cx + 6, by, BRONZE_D); d.rectangle([cx - 2, by - 28, cx + 2, by - 6], fill=K); d.rectangle([cx - 1, by - 27, cx + 1, by - 7], fill=BRONZE)
    d.polygon([(cx - 8, by - 28), (cx + 8, by - 28), (cx + 5, by - 34), (cx - 5, by - 34)], fill=K); d.polygon([(cx - 7, by - 29), (cx + 7, by - 29), (cx + 4, by - 33), (cx - 4, by - 33)], fill=BRONZE)
    d.polygon([(cx - 4, by - 33), (cx - 1, by - 44), (cx + 1, by - 38), (cx + 3, by - 46), (cx + 5, by - 33)], fill=FLAME); d.polygon([(cx - 2, by - 33), (cx, by - 41), (cx + 2, by - 33)], fill=(210, 255, 250))
    return im, cx, by


def pillar():
    """漆柱：黑漆红纹、铜箍、石础"""
    im, d = canvas(30, 86); cx, by = 15, 84
    shadow(d, cx, by, 12, 3)
    box(d, cx - 12, by - 8, cx + 12, by, STONE_D); box(d, cx - 8, by - 12, cx + 8, by - 7, STONE)
    d.rectangle([cx - 8, 10, cx + 8, by - 12], fill=K); d.rectangle([cx - 7, 11, cx + 7, by - 13], fill=LAC); d.line([(cx - 5, 11), (cx - 5, by - 13)], fill=(70, 56, 70))
    for y in range(20, by - 14, 12): d.line([(cx - 7, y), (cx + 7, y)], fill=LAC_R); d.line([(cx - 7, y + 1), (cx + 7, y + 1)], fill=GOLD_D)
    d.rectangle([cx - 8, by - 20, cx + 8, by - 16], fill=BRONZE); d.rectangle([cx - 8, 10, cx + 8, 14], fill=BRONZE)
    box(d, cx - 12, 2, cx + 12, 10, (60, 46, 56)); d.rectangle([cx - 10, 4, cx + 10, 6], fill=GOLD_D)
    return im, cx, by


def gate(w=200, h=130):
    """青铜大门：夯土门墩 + 兽面铺首 + 门楼"""
    im, d = canvas(w + 40, h + 40); cx = (w + 40) // 2; by = h + 36
    shadow(d, cx, by, w // 2 + 10, 6)
    for sx in (-1, 1):
        px = cx + sx * (w // 2 - 28)
        box(d, px - 28, by - h, px + 28, by, (86, 78, 80)); d.rectangle([px - 27, by - h, px + 27, by - h + 6], fill=(112, 104, 104))
        for y in range(by - h + 14, by - 4, 12): d.line([(px - 27, y), (px + 27, y)], fill=(70, 62, 66))
    gw = w - 112
    box(d, cx - gw // 2, by - h + 28, cx + gw // 2, by, (20, 24, 30))
    d.rectangle([cx - gw // 2 + 4, by - h + 32, cx - 2, by - 2], fill=BRONZE_D); d.rectangle([cx + 2, by - h + 32, cx + gw // 2 - 4, by - 2], fill=BRONZE_D)   # 门扇
    for x in range(cx - gw // 2 + 8, cx + gw // 2 - 6, 10):
        if abs(x - cx) > 4: d.line([(x, by - h + 34), (x, by - 4)], fill=PATINA)
    for sx in (-1, 1):
        mx = cx + sx * 16; d.ellipse([mx - 8, by - 50, mx + 8, by - 34], fill=K); d.ellipse([mx - 7, by - 49, mx + 7, by - 35], fill=GOLD); d.ellipse([mx - 3, by - 45, mx + 3, by - 39], fill=K)   # 铺首
    d.rectangle([cx - gw // 2 - 6, by - h + 14, cx + gw // 2 + 6, by - h + 30], fill=K); d.rectangle([cx - gw // 2 - 4, by - h + 16, cx + gw // 2 + 4, by - h + 28], fill=LAC_R)
    for x in range(cx - gw // 2, cx + gw // 2, 14): d.rectangle([x, by - h + 19, x + 6, by - h + 25], fill=GOLD_D)
    return im, cx, by


def coffin():
    """主墓室：高台上的青铜椁与棺，环绕金玉"""
    im, d = canvas(220, 150); cx = 110; by = 146
    shadow(d, cx, by, 100, 8)
    for i in range(4): box(d, cx - 100 + i * 8, by - 12 - i * 8, cx + 100 - i * 8, by - i * 8, STONE_L if i % 2 else STONE)
    box(d, cx - 60, by - 62, cx + 60, by - 30, BRONZE_D); d.rectangle([cx - 59, by - 62, cx + 59, by - 56], fill=BRONZE)
    for x in range(cx - 56, cx + 56, 10): d.rectangle([x, by - 52, x + 6, by - 36], fill=PATINA)
    box(d, cx - 44, by - 84, cx + 44, by - 60, (86, 62, 44)); d.rectangle([cx - 43, by - 84, cx + 43, by - 80], fill=GOLD)
    for x in range(cx - 38, cx + 40, 12): d.ellipse([x, by - 78, x + 6, by - 72], fill=GOLD_L); d.line([(x + 3, by - 72), (x + 3, by - 64)], fill=GOLD_D)
    d.ellipse([cx - 14, by - 106, cx + 14, by - 82], fill=K); d.ellipse([cx - 12, by - 104, cx + 12, by - 84], fill=(70, 200, 170)); d.ellipse([cx - 5, by - 98, cx + 5, by - 90], fill=K)    # 玉璧
    for sx in (-1, 1):
        for k in range(3): d.ellipse([cx + sx * (66 + k * 8) - 5, by - 22 - k * 4, cx + sx * (66 + k * 8) + 5, by - 14 - k * 4], fill=GOLD if k % 2 == 0 else (70, 200, 170))
    return im, cx, by


def chest(gold=True):
    im, d = canvas(34, 30); cx, by = 17, 28
    shadow(d, cx, by, 13, 3)
    box(d, cx - 13, by - 16, cx + 13, by, (110, 70, 50)); d.polygon([(cx - 14, by - 16), (cx + 14, by - 16), (cx + 10, by - 26), (cx - 10, by - 26)], fill=K); d.polygon([(cx - 13, by - 17), (cx + 13, by - 17), (cx + 9, by - 25), (cx - 9, by - 25)], fill=(130, 84, 58))
    d.rectangle([cx - 14, by - 12, cx + 14, by - 9], fill=GOLD_D); d.rectangle([cx - 3, by - 14, cx + 3, by - 6], fill=GOLD); d.point((cx, by - 10), fill=K)
    if gold: d.line([(cx - 8, by - 28), (cx - 5, by - 31)], fill=GOLD_L); d.point((cx + 6, by - 30), fill=GOLD_L)
    return im, cx, by


def bones():
    im, d = canvas(36, 22); cx, by = 18, 20
    shadow(d, cx, by, 12, 2)
    d.ellipse([cx - 14, by - 10, cx - 2, by + 0], fill=K); d.ellipse([cx - 13, by - 9, cx - 3, by - 1], fill=(222, 214, 194)); d.rectangle([cx - 11, by - 6, cx - 9, by - 4], fill=K); d.rectangle([cx - 7, by - 6, cx - 5, by - 4], fill=K)
    d.line([(cx, by - 4), (cx + 14, by - 8)], fill=(222, 214, 194), width=2); d.line([(cx + 2, by - 1), (cx + 16, by - 2)], fill=(222, 214, 194), width=2)
    return im, cx, by


def crane():
    """青铜仙鹤"""
    im, d = canvas(30, 56); cx, by = 15, 54
    shadow(d, cx, by, 10, 3)
    box(d, cx - 8, by - 5, cx + 8, by, BRONZE_D)
    d.line([(cx - 3, by - 5), (cx - 3, by - 24)], fill=K, width=3); d.line([(cx + 3, by - 5), (cx + 3, by - 24)], fill=K, width=3)
    d.line([(cx - 3, by - 5), (cx - 3, by - 24)], fill=BRONZE, width=1); d.line([(cx + 3, by - 5), (cx + 3, by - 24)], fill=BRONZE, width=1)
    d.ellipse([cx - 11, by - 38, cx + 11, by - 22], fill=K); d.ellipse([cx - 10, by - 37, cx + 10, by - 23], fill=PATINA)
    d.line([(cx + 6, by - 34), (cx + 9, by - 50)], fill=K, width=3); d.line([(cx + 6, by - 34), (cx + 9, by - 50)], fill=PATINA, width=1)
    d.ellipse([cx + 5, by - 55, cx + 13, by - 47], fill=K); d.ellipse([cx + 6, by - 54, cx + 12, by - 48], fill=PATINA); d.line([(cx + 12, by - 51), (cx + 18, by - 49)], fill=GOLD, width=1)
    d.polygon([(cx - 10, by - 34), (cx - 20, by - 44), (cx - 8, by - 28)], fill=K); d.polygon([(cx - 9, by - 33), (cx - 17, by - 41), (cx - 8, by - 29)], fill=PATINA)
    return im, cx, by


def beast():
    """镇墓兽：石雕辟邪"""
    im, d = canvas(40, 40); cx, by = 20, 38
    shadow(d, cx, by, 14, 3)
    box(d, cx - 14, by - 6, cx + 14, by, STONE_D)
    d.rectangle([cx - 10, by - 22, cx + 10, by - 6], fill=K); d.rectangle([cx - 9, by - 21, cx + 9, by - 7], fill=(112, 120, 108))
    d.ellipse([cx - 10, by - 34, cx + 4, by - 20], fill=K); d.ellipse([cx - 9, by - 33, cx + 3, by - 21], fill=(130, 138, 124))
    d.polygon([(cx - 8, by - 34), (cx - 4, by - 42), (cx, by - 34)], fill=K); d.polygon([(cx - 6, by - 34), (cx - 4, by - 40), (cx - 2, by - 34)], fill=(130, 138, 124))
    d.point((cx - 6, by - 28), fill=(240, 70, 60)); d.point((cx - 2, by - 28), fill=(240, 70, 60))
    d.polygon([(cx + 8, by - 20), (cx + 18, by - 30), (cx + 18, by - 14)], fill=(112, 120, 108))
    return im, cx, by


def crossbow():
    """弩机石柱：机关"""
    im, d = canvas(24, 46); cx, by = 12, 44
    shadow(d, cx, by, 8, 2)
    box(d, cx - 7, by - 30, cx + 7, by, (80, 82, 94)); d.rectangle([cx - 6, by - 30, cx + 6, by - 26], fill=(110, 112, 126))
    d.rectangle([cx - 4, by - 22, cx + 4, by - 16], fill=K); d.rectangle([cx - 3, by - 21, cx + 3, by - 17], fill=(20, 16, 20))
    d.line([(cx - 10, by - 34), (cx + 10, by - 34)], fill=K, width=3); d.line([(cx - 10, by - 34), (cx + 10, by - 34)], fill=BRONZE, width=1)
    d.line([(cx, by - 38), (cx, by - 30)], fill=PATINA)
    return im, cx, by


SPRITES = {'qn_warrior0': lambda: warrior(0), 'qn_warrior1': lambda: warrior(1), 'qn_warrior2': lambda: warrior(2), 'qn_chariot': chariot, 'qn_lamp': lamp, 'qn_pillar': pillar,
           'qn_gate': lambda: gate(220, 130), 'qn_gateS': lambda: gate(150, 100), 'qn_coffin': coffin, 'qn_chest': chest, 'qn_bones': bones, 'qn_crane': crane, 'qn_beast': beast, 'qn_bow': crossbow}


from PIL import ImageFilter, ImageChops
import numpy as np


def hall():
    """秦式大殿：黑瓦重檐、黑红漆柱、金色脊饰、云纹台基"""
    w, h = 320, 210
    im, d = canvas(w, h); cx = w // 2; by = h - 4
    BLK, BLK_D, BLK_L = (40, 36, 52), (28, 24, 38), (74, 70, 96)
    shadow(d, cx, by, 150, 8)
    for i in range(4): box(d, cx - 70 - i * 10, by - 6 - i * 7, cx + 70 + i * 10, by - i * 7, STONE_L if i % 2 else STONE)
    box(d, 20, by - 96, w - 20, by - 28, (70, 36, 44)); d.rectangle([21, by - 96, w - 21, by - 90], fill=(110, 50, 54))
    for x in range(26, w - 22, 22):
        d.rectangle([x - 3, by - 94, x + 3, by - 30], fill=K); d.rectangle([x - 2, by - 93, x + 2, by - 31], fill=LAC); d.line([(x - 1, by - 93), (x - 1, by - 31)], fill=(90, 70, 90))
        d.line([(x - 2, by - 60), (x + 2, by - 60)], fill=GOLD_D)
    box(d, cx - 30, by - 84, cx + 30, by - 30, (20, 14, 22)); d.rectangle([cx - 28, by - 82, cx + 28, by - 32], fill=(246, 204, 112)); d.line([(cx, by - 82), (cx, by - 32)], fill=BRONZE_D)
    for gx in range(cx - 22, cx + 24, 11): d.line([(gx, by - 82), (gx, by - 32)], fill=BRONZE_D)
    for x in range(30, w - 28, 12): d.rectangle([x, by - 92, x + 6, by - 86], fill=GOLD_D)
    def roof(x0, x1, ye, yt, ext):
        d.polygon([(x0 - ext, ye + 2), (x1 + ext, ye + 2), (x1 - 8, yt), (x0 + 8, yt)], fill=K)
        d.polygon([(x0 - ext + 2, ye), (x1 + ext - 2, ye), (x1 - 10, yt + 2), (x0 + 10, yt + 2)], fill=BLK)
        n = (x1 - x0) // 7
        for i in range(n + 1):
            t = i / n; d.line([(x0 - ext + 2 + t * (x1 - x0 + 2 * ext - 4), ye - 1), (x0 + 10 + t * (x1 - x0 - 20), yt + 3)], fill=BLK_D)
        d.line([(x0 + 10, yt + 2), (x1 - 10, yt + 2)], fill=GOLD, width=2)
        for sx in (-1, 1): d.polygon([((x0 - ext) if sx < 0 else (x1 + ext), ye + 2), (((x0 - ext) if sx < 0 else (x1 + ext)) + sx * 8, ye - 7), (((x0 - ext) if sx < 0 else (x1 + ext)) - sx * 2, ye - 2)], fill=GOLD_D)
    roof(14, w - 14, by - 94, by - 128, 16); roof(52, w - 52, by - 128, by - 164, 12)
    for sx in (50, w - 50): d.polygon([(sx - 4, by - 164), (sx + 4, by - 164), (sx, by - 180)], fill=GOLD)
    d.ellipse([cx - 8, by - 178, cx + 8, by - 164], fill=GOLD); d.ellipse([cx - 4, by - 175, cx + 4, by - 167], fill=(250, 240, 180))
    return im, cx, by


SPRITES['qn_hall'] = hall


def maze(x0, y0, cols, rows, cell, seed):
    r = random.Random(seed)
    vis = [[False] * cols for _ in range(rows)]
    hw = [[True] * cols for _ in range(rows + 1)]; vw = [[True] * (cols + 1) for _ in range(rows)]
    stack = [(rows - 1, cols // 2)]; vis[rows - 1][cols // 2] = True
    while stack:
        rr, cc = stack[-1]; nbs = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = rr + dr, cc + dc
            if 0 <= nr < rows and 0 <= nc < cols and not vis[nr][nc]: nbs.append((nr, nc, dr, dc))
        if not nbs: stack.pop(); continue
        nr, nc, dr, dc = r.choice(nbs); vis[nr][nc] = True
        if dr == -1: hw[rr][cc] = False
        elif dr == 1: hw[rr + 1][cc] = False
        elif dc == -1: vw[rr][cc] = False
        else: vw[rr][cc + 1] = False
        stack.append((nr, nc))
    for _ in range(cols * rows // 5):
        rr, cc = r.randrange(rows), r.randrange(1, cols); vw[rr][cc] = False
    return hw, vw


def bigpillar():
    """正殿大柱：粗大的黑漆红纹金箍柱，带石础与斗拱"""
    im, d = canvas(44, 130); cx, by = 22, 128
    shadow(d, cx, by, 18, 4)
    box(d, cx - 18, by - 10, cx + 18, by, STONE_D); box(d, cx - 13, by - 16, cx + 13, by - 9, STONE)
    d.rectangle([cx - 13, 16, cx + 13, by - 16], fill=K); d.rectangle([cx - 12, 17, cx + 12, by - 17], fill=LAC)
    d.rectangle([cx - 12, 17, cx - 8, by - 17], fill=(60, 44, 58)); d.rectangle([cx + 8, 17, cx + 12, by - 17], fill=(20, 14, 22))
    for y in range(28, by - 20, 16):
        d.line([(cx - 12, y), (cx + 12, y)], fill=LAC_R); d.line([(cx - 12, y + 1), (cx + 12, y + 1)], fill=GOLD_D)
        d.polygon([(cx - 4, y + 4), (cx + 4, y + 4), (cx, y + 10)], fill=GOLD_D)
    for yy in (by - 30, 18): d.rectangle([cx - 13, yy, cx + 13, yy + 5], fill=BRONZE); d.line([(cx - 13, yy), (cx + 13, yy)], fill=GOLD_L)
    box(d, cx - 20, 2, cx + 20, 16, (70, 52, 62)); d.rectangle([cx - 17, 5, cx + 17, 8], fill=GOLD_D)
    d.polygon([(cx - 20, 2), (cx - 26, 8), (cx - 20, 12)], fill=(90, 66, 70)); d.polygon([(cx + 20, 2), (cx + 26, 8), (cx + 20, 12)], fill=(90, 66, 70))
    return im, cx, by


SPRITES['qn_bigpillar'] = bigpillar


def build(seed=88):
    random.seed(seed)
    CX = 1200
    # ---------- 虚空：深蓝黑 + 星 + 脚下很深处发光的水银河 ----------
    base = Image.new('RGBA', (W, H), (8, 10, 22, 255)); bd = ImageDraw.Draw(base)
    for _ in range(3200):
        x, y = random.randrange(W), random.randrange(H)
        bd.point((x, y), fill=random.choice([(60, 70, 110, 255), (90, 100, 150, 255), (140, 150, 200, 255), (200, 190, 130, 255)]))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    pts = [(-40, 1500)]
    for x in range(0, W + 120, 120): pts.append((x, 1500 + int(260 * math.sin(x / 330) + 90 * math.sin(x / 97))))
    gd.line(pts, fill=(70, 200, 210, 150), width=90); gd.line(pts, fill=(200, 240, 250, 170), width=26)
    pts2 = [(x, y - 900) for (x, y) in pts]
    gd.line(pts2, fill=(70, 160, 200, 90), width=70); gd.line(pts2, fill=(190, 230, 250, 100), width=18)
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    base.alpha_composite(glow)
    for _ in range(36):
        x = random.randrange(W); y0 = random.randrange(0, H // 2); L = random.randrange(120, 420)
        for k in range(0, L, 6): bd.rectangle([x, y0 + k, x + 2, y0 + k + 3], fill=(26, 28, 44, 255))
    im = base; d = ImageDraw.Draw(im)
    walk = Image.new('L', (W, H), 0); wd = ImageDraw.Draw(walk)
    blocks = []
    traps = []      # 机关/陷阱数据，供游戏逻辑使用：{t, x, y, w, h}

    def island(shape, floor_col=(62, 66, 78), grid_col=(52, 56, 68), under=28):
        m = Image.new('L', (W, H), 0); shape(ImageDraw.Draw(m), 255)
        sh = ImageChops.offset(m, 6, 54).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.55))
        im.paste((0, 0, 0, 255), (0, 0), sh)
        rock = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for k in range(1, under + 1):
            mm = ImageChops.offset(m, 0, k); tone = int(52 - k * 0.9)
            rock.paste((tone, tone - 4, tone + 8, 255), (0, 0), mm)
        im.alpha_composite(rock)
        nz = np.array(m); ys, xs = np.nonzero(nz > 0); edge = {}
        for y, x in zip(ys[::7], xs[::7]):
            if y + 1 < H and nz[y + 1, x] == 0: edge[x] = y
        for x, y in list(edge.items())[::5]:
            ln = random.randint(10, 34); wdt = random.randint(2, 5)
            d.polygon([(x - wdt, y + under - 6), (x + wdt, y + under - 6), (x, y + under + ln)], fill=(34, 32, 46, 255))
        top = Image.new('RGBA', (W, H), floor_col + (255,)); td = ImageDraw.Draw(top)
        for _ in range(60000): td.point((random.randrange(W), random.randrange(H)), fill=random.choice([floor_col, grid_col, tuple(min(255, c + 8) for c in floor_col)]))
        for x in range(0, W, 28): td.line([(x, 0), (x, H)], fill=grid_col)
        for y in range(0, H, 28): td.line([(0, y), (W, y)], fill=grid_col)
        im.paste(top, (0, 0), m)
        edge_m = ImageChops.subtract(m, m.filter(ImageFilter.MinFilter(5)))
        im.paste((24, 26, 40, 255), (0, 0), edge_m)
        inner = ImageChops.subtract(m.filter(ImageFilter.MinFilter(5)), m.filter(ImageFilter.MinFilter(9)))
        im.paste((112, 116, 132, 255), (0, 0), inner)
        wd.bitmap((0, 0), m, fill=255)

    def rough_ellipse(cx, cy, rx, ry, jit=14, seed_=0):
        r = random.Random(seed_); n = 48
        pts = [(cx + (rx + r.randint(-jit, jit)) * math.cos(2 * math.pi * i / n), cy + (ry + r.randint(-jit, jit) * 0.6) * math.sin(2 * math.pi * i / n)) for i in range(n)]
        return lambda dd, f: dd.polygon(pts, fill=f)

    def rect_shape(x0, y0, x1, y1, jit=10, seed_=0):
        r = random.Random(seed_); pts = []
        for x in range(x0, x1, 40): pts.append((x, y0 + r.randint(-jit, jit)))
        for y in range(y0, y1, 40): pts.append((x1 + r.randint(-jit, jit), y))
        for x in range(x1, x0, -40): pts.append((x, y1 + r.randint(-jit, jit)))
        for y in range(y1, y0, -40): pts.append((x0 + r.randint(-jit, jit), y))
        return lambda dd, f: dd.polygon(pts, fill=f)

    # ---------- 各座浮空石台 ----------
    ENT = (CX - 120, 1800, CX + 120, 1960)
    PIT = (820, 1290, 1580, 1640)                    # 兵马俑坑（缩小）
    HALL = (700, 620, 1700, 1200)                    # 正殿台
    WS = (140, 700, 640, 1140); ES = (1760, 700, 2260, 1140)       # 东西偏殿台
    WT = (140, 1300, 640, 1760); ET = (1760, 1300, 2260, 1760)     # 西：机关迷宫  东：陷阱房
    BUR_C, BUR_R = (CX, 240), (380, 170)
    island(rect_shape(*ENT, 6, 1))
    island(rect_shape(*PIT, 12, 2), (58, 52, 56), (50, 44, 50))
    island(rect_shape(*HALL, 10, 3), (56, 58, 72), (48, 50, 64))
    island(rect_shape(*WS, 8, 4)); island(rect_shape(*ES, 8, 5))
    island(rect_shape(*WT, 8, 6), (50, 54, 62), (42, 46, 56)); island(rect_shape(*ET, 8, 7), (58, 48, 52), (48, 40, 44))
    island(rough_ellipse(*BUR_C, *BUR_R, 10, 4), (50, 56, 76), (42, 48, 68))

    # ---------- 悬浮台阶 / 吊桥 ----------
    def floating_stairs(xc, y_from, y_to, wdt=96, step=16):
        ys = list(range(min(y_from, y_to), max(y_from, y_to), step))
        for k, y in enumerate(ys):
            sx = int(6 * math.sin(k * 1.7))
            d.rectangle([xc - wdt // 2 + sx + 6, y + 14, xc + wdt // 2 + sx + 6, y + 22], fill=(4, 6, 14, 255))
            d.rectangle([xc - wdt // 2 + sx - 1, y - 1, xc + wdt // 2 + sx + 1, y + 11], fill=K)
            d.rectangle([xc - wdt // 2 + sx, y, xc + wdt // 2 + sx, y + 9], fill=(112, 116, 134) if k % 2 else (134, 138, 156))
            d.rectangle([xc - wdt // 2 + sx, y + 6, xc + wdt // 2 + sx, y + 9], fill=(78, 82, 100))
            d.point((xc - wdt // 2 + sx + 3, y + 2), fill=(190, 194, 210))
        wd.rectangle([xc - wdt // 2 - 6, min(y_from, y_to) - 4, xc + wdt // 2 + 6, max(y_from, y_to) + 12], fill=255)
        for yy in range(min(y_from, y_to) + 10, max(y_from, y_to), 50):
            for sx in (-1, 1):
                lx = xc + sx * (wdt // 2 + 14)
                d.ellipse([lx - 5, yy - 10, lx + 5, yy], fill=K); d.ellipse([lx - 4, yy - 9, lx + 4, yy - 1], fill=(90, 230, 220, 255))

    def plank_bridge(x0, x1, yc, wdt=56):
        for x in range(x0, x1, 12):
            sy = int(3 * math.sin(x * 0.2))
            d.rectangle([x + 4, yc - wdt // 2 + sy + 12, x + 12, yc + wdt // 2 + sy + 12], fill=(4, 6, 14, 255))
            d.rectangle([x, yc - wdt // 2 + sy, x + 10, yc + wdt // 2 + sy], fill=K); d.rectangle([x + 1, yc - wdt // 2 + sy + 1, x + 9, yc + wdt // 2 + sy - 1], fill=(120, 90, 64) if (x // 12) % 2 else (140, 104, 72))
        for yy in (yc - wdt // 2 - 3, yc + wdt // 2 + 3): d.line([(x0, yy), (x1, yy)], fill=(180, 140, 80), width=2)
        for x in range(x0, x1, 40):
            for yy in (yc - wdt // 2 - 3, yc + wdt // 2 + 3): d.rectangle([x, yy - 10, x + 3, yy], fill=GOLD_D)
        wd.rectangle([x0 - 2, yc - wdt // 2 - 4, x1 + 2, yc + wdt // 2 + 4], fill=255)
    STAIRS = ((CX, 1640, 1800, 100), (CX, 1200, 1290, 100), (CX, 410, 620, 90))
    for (xc, ya, yb, ww) in STAIRS: floating_stairs(xc, ya, yb, ww, 14)
    plank_bridge(630, 710, 930); plank_bridge(1690, 1770, 930)          # 正殿 ↔ 偏殿
    plank_bridge(630, 830, 1530); plank_bridge(1570, 1770, 1530)        # 兵马俑坑 ↔ 机关迷宫 / 陷阱房

    def wall_rect(x0, y0, x1, y1, face=10, solid=True):
        d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + face + 1], fill=K)
        d.rectangle([x0, y0, x1, y1], fill=WALL_T); d.rectangle([x0, y1, x1, y1 + face], fill=WALL_F)
        d.line([(x0, y1 + face - 1), (x1, y1 + face - 1)], fill=WALL_D)
        for x in range(x0 + 6, x1 - 2, 12): d.rectangle([x, y1 + 3, x + 5, y1 + 6], fill=(78, 84, 100))
        if solid: blocks.append((x0, y0, x1, y1 + face))

    def room(x0, y0, x1, y1, doors=(), T=16):
        """四面墙的房间；doors=[('N'|'S'|'W'|'E', 开口起, 开口止)]"""
        def segs(a, b, gaps):
            out = []; cur = a
            for (g0, g1) in sorted(gaps):
                if g0 > cur: out.append((cur, g0))
                cur = g1
            if cur < b: out.append((cur, b))
            return out
        g = {s: [(a, b) for (ss, a, b) in doors if ss == s] for s in 'NSWE'}
        for (a, b) in segs(x0, x1, g['N']): wall_rect(a, y0, b, y0 + T, 12)
        for (a, b) in segs(x0, x1, g['S']): wall_rect(a, y1 - T, b, y1, 12)
        for (a, b) in segs(y0 + T, y1 - T, g['W']): wall_rect(x0, a, x0 + T, b, 12)
        for (a, b) in segs(y0 + T, y1 - T, g['E']): wall_rect(x1 - T, a, x1, b, 12)

    # ---------- 正殿：红毯 + 18 根大柱 + 机关 ----------
    HX0, HY0, HX1, HY1 = 760, 660, 1640, 1140
    d.rectangle([HX0, HY0, HX1, HY1], fill=(40, 40, 54))
    for x in range(HX0, HX1, 40):
        for y in range(HY0, HY1, 40):
            if ((x - HX0) // 40 + (y - HY0) // 40) % 2: d.rectangle([x, y, x + 39, y + 39], fill=(46, 46, 62))
    d.rectangle([CX - 60, HY0, CX + 60, HY1 + 60], fill=(120, 34, 40)); d.rectangle([CX - 56, HY0, CX - 52, HY1 + 60], fill=GOLD_D); d.rectangle([CX + 52, HY0, CX + 56, HY1 + 60], fill=GOLD_D)
    for y in range(HY0 + 10, HY1 + 40, 36): d.polygon([(CX, y), (CX + 10, y + 8), (CX, y + 16), (CX - 10, y + 8)], outline=GOLD_D)
    room(HX0, HY0, HX1, HY1, doors=[('N', CX - 60, CX + 60), ('S', CX - 70, CX + 70), ('W', 870, 950), ('E', 870, 950)])
    # 殿内挂帷
    for x in range(HX0 + 40, HX1 - 20, 80):
        if abs(x - CX) > 70: d.rectangle([x, HY0 + 4, x + 20, HY0 + 28], fill=(120, 34, 40)); d.line([(x, HY0 + 4), (x + 20, HY0 + 4)], fill=GOLD_D)
    # 机关：红毯两侧喷火口 + 压力板
    for (fx, fy) in ((CX - 100, 800), (CX + 100, 800), (CX - 100, 980), (CX + 100, 980)):
        d.rectangle([fx - 14, fy - 8, fx + 14, fy + 8], fill=K); d.rectangle([fx - 12, fy - 6, fx + 12, fy + 6], fill=(50, 40, 40))
        for gx in range(fx - 9, fx + 10, 6): d.line([(gx, fy - 5), (gx, fy + 5)], fill=(20, 16, 16))
        traps.append(dict(t='flame', x=fx - 14, y=fy - 8, w=28, h=16))
    for (px, py) in ((CX, 880), (CX, 1060)):
        d.rectangle([px - 22, py - 8, px + 22, py + 8], fill=K); d.rectangle([px - 20, py - 6, px + 20, py + 6], fill=GOLD_D); d.rectangle([px - 14, py - 3, px + 14, py + 3], fill=(176, 136, 70))
        traps.append(dict(t='plate', x=px - 22, y=py - 8, w=44, h=16))
    d.rectangle([CX - 80, 1146, CX + 80, 1196], fill=(70, 74, 90))     # 殿门前台阶（装饰）
    # ---------- 偏殿 ----------
    room(180, 740, 620, 1100, doors=[('E', 890, 970)])
    room(1780, 740, 2220, 1100, doors=[('W', 890, 970)])
    for (x0, x1) in ((180, 620), (1780, 2220)):
        d.rectangle([x0 + 16, 756, x1 - 16, 1084], fill=(46, 44, 56))
        for x in range(x0 + 16, x1 - 16, 40):
            for y in range(756, 1084, 40):
                if ((x - x0) // 40 + (y - 756) // 40) % 2: d.rectangle([x, y, x + 39, y + 39], fill=(52, 48, 62))
    d.rectangle([228, 880, 574, 980], fill=(110, 32, 40)) ; d.rectangle([1826, 880, 2172, 980], fill=(110, 32, 40))   # 红毯
    for (x0, x1) in ((228, 574), (1826, 2172)): d.line([(x0, 880), (x1, 880)], fill=GOLD_D); d.line([(x0, 980), (x1, 980)], fill=GOLD_D)
    # ---------- 西：机关迷宫 ----------
    def maze_gen(x0, y0, cols, rows, cell, seed):
        r = random.Random(seed)
        vis = [[False] * cols for _ in range(rows)]
        hw = [[True] * cols for _ in range(rows + 1)]; vw = [[True] * (cols + 1) for _ in range(rows)]
        stack = [(rows // 2, cols - 1)]; vis[rows // 2][cols - 1] = True
        while stack:
            rr, cc = stack[-1]; nbs = []
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not vis[nr][nc]: nbs.append((nr, nc, dr, dc))
            if not nbs: stack.pop(); continue
            nr, nc, dr, dc = r.choice(nbs); vis[nr][nc] = True
            if dr == -1: hw[rr][cc] = False
            elif dr == 1: hw[rr + 1][cc] = False
            elif dc == -1: vw[rr][cc] = False
            else: vw[rr][cc + 1] = False
            stack.append((nr, nc))
        for _ in range(cols * rows // 4):
            rr, cc = r.randrange(rows), r.randrange(1, cols); vw[rr][cc] = False
        return hw, vw
    MX0, MY0, MC, MR, MCELL = 170, 1320, 5, 5, 84
    hw, vw = maze_gen(MX0, MY0, MC, MR, MCELL, 11); T = 14
    for r_ in range(MR + 1):
        for c_ in range(MC):
            if hw[r_][c_]: wall_rect(MX0 + c_ * MCELL - T // 2, MY0 + r_ * MCELL - T // 2, MX0 + (c_ + 1) * MCELL + T // 2, MY0 + r_ * MCELL + T // 2, 8)
    for r_ in range(MR):
        for c_ in range(MC + 1):
            if vw[r_][c_]:
                if c_ == MC and r_ in (1, 2, 3): continue
                wall_rect(MX0 + c_ * MCELL - T // 2, MY0 + r_ * MCELL - T // 2, MX0 + c_ * MCELL + T // 2, MY0 + (r_ + 1) * MCELL + T // 2, 8)
    for r_ in range(MR):                                # 迷宫地面压力板（触发弩箭）
        for c_ in range(MC):
            if random.random() < 0.22 and c_ < MC - 1:
                px, py = MX0 + c_ * MCELL + MCELL // 2, MY0 + r_ * MCELL + MCELL // 2 + 6
                d.rectangle([px - 14, py - 8, px + 14, py + 8], fill=K); d.rectangle([px - 12, py - 6, px + 12, py + 6], fill=GOLD_D); d.rectangle([px - 8, py - 3, px + 8, py + 3], fill=(176, 136, 70))
                traps.append(dict(t='plate', x=px - 14, y=py - 8, w=28, h=16))
    # ---------- 东：陷阱房（地刺阵，只有一条安全路径）----------
    room(1820, 1340, 2240, 1720, doors=[('W', 1480, 1560)])
    TX0, TY0, TC, TR, TS = 1850, 1370, 5, 5, 60
    d.rectangle([1836, 1356, 2224, 1704], fill=(44, 38, 44))
    safe = set(); rmid = 2; r_ = rmid
    for c_ in range(TC):
        safe.add((r_, c_))
        while random.random() < 0.55:
            nr = r_ + random.choice((-1, 1))
            if 0 <= nr < TR: r_ = nr; safe.add((r_, c_))
            else: break
    while r_ != rmid: r_ += 1 if r_ < rmid else -1; safe.add((r_, TC - 1))
    for rr in range(TR):
        for cc in range(TC):
            x, y = TX0 + cc * TS, TY0 + rr * TS
            if (rr, cc) in safe:
                d.rectangle([x + 2, y + 2, x + TS - 3, y + TS - 3], fill=(74, 70, 82)); d.rectangle([x + 6, y + 6, x + TS - 7, y + TS - 7], outline=(96, 92, 106))
                if random.random() < 0.4: traps.append(dict(t='plate', x=x + 18, y=y + 22, w=24, h=16)); d.rectangle([x + 18, y + 22, x + 42, y + 38], fill=GOLD_D); d.rectangle([x + 22, y + 25, x + 38, y + 35], fill=(176, 136, 70))
            else:
                d.rectangle([x + 2, y + 2, x + TS - 3, y + TS - 3], fill=(30, 24, 30))
                for sx in range(x + 8, x + TS - 6, 14):
                    for sy in range(y + 10, y + TS - 6, 14):
                        d.polygon([(sx - 5, sy + 6), (sx + 5, sy + 6), (sx, sy - 7)], fill=(176, 180, 192)); d.polygon([(sx, sy - 7), (sx + 5, sy + 6), (sx + 1, sy + 6)], fill=(120, 124, 140)); d.point((sx, sy - 6), fill=(255, 255, 255))
                d.rectangle([x + 2, y + 2, x + TS - 3, y + TS - 3], outline=(110, 30, 34))
                traps.append(dict(t='spike', x=x + 2, y=y + 2, w=TS - 4, h=TS - 4))
    # ---------- 宫殿台、主墓室 ----------
    RC = BUR_C
    d.ellipse([RC[0] - 330, RC[1] - 110, RC[0] + 330, RC[1] + 110], fill=K); d.ellipse([RC[0] - 324, RC[1] - 104, RC[0] + 324, RC[1] + 104], fill=MERC_D)
    for _ in range(9000):
        a, rr = random.random() * 6.283, random.random() ** 0.5; im.putpixel((int(RC[0] + 320 * rr * math.cos(a)), int(RC[1] + 100 * rr * math.sin(a))), random.choice([MERC, MERC_L, MERC_D]))
    islands = ((CX - 230, 220, 36), (CX + 230, 230, 40), (CX - 150, 290, 24), (CX + 160, 170, 28))
    for (ex, ey, er) in islands:
        d.ellipse([ex - er, ey - er * 0.6, ex + er, ey + er * 0.6], fill=K); d.ellipse([ex - er + 2, ey - er * 0.6 + 2, ex + er - 2, ey + er * 0.6 - 2], fill=(60, 78, 66))
    d.ellipse([CX - 110, 190, CX + 110, 262], fill=K); d.ellipse([CX - 106, 194, CX + 106, 258], fill=(80, 84, 94))
    # 水银海上的石径：南岸直通中央石台（路面稍窄，两侧是水银）
    d.rectangle([CX - 38, 250, CX + 38, 362], fill=K); d.rectangle([CX - 34, 250, CX + 34, 362], fill=(84, 88, 100))
    for y in range(256, 360, 14): d.line([(CX - 34, y), (CX + 34, y)], fill=(70, 74, 88))
    wd.rectangle([CX - 36, 248, CX + 36, 364], fill=255)

    # ---------- 物件 ----------
    SP = {k: f() for k, f in SPRITES.items()}
    objs = []; warriors = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    put('qn_gateS', CX, 1930, None); blocks += [(CX - 120, 1910, CX - 60, 1950), (CX + 60, 1910, CX + 120, 1950)]
    for y in (1850, 1900): put('qn_lamp', CX - 80, y, (-5, -6, 5, 0)); put('qn_lamp', CX + 80, y, (-5, -6, 5, 0))
    # 兵马俑坑：只有 3 排，中间留宽通道；记录位置，之后可作为怪物出现
    for rr in range(3):
        for cc in range(5):
            for side in (-1, 1):
                x = CX + side * (90 + cc * 56); y = 1370 + rr * 50
                put('qn_warrior%d' % ((cc + rr) % 3), x, y, (-6, -8, 6, 0)); warriors.append(dict(x=x, y=y, k=(cc + rr) % 3))
    for x in (900, 1500): put('qn_chariot', x, 1600, (-30, -14, 30, 0))
    for sx in (-1, 1): put('qn_beast', CX + sx * 90, 1600, (-12, -8, 12, 0)); put('qn_lamp', CX + sx * 150, 1330, (-5, -6, 5, 0))
    # 正殿：18 根大柱（两侧各 3 列 × 3 排）
    for rr, y in enumerate((780, 920, 1060)):
        for cx_ in (-340, -240, -140, 140, 240, 340):
            put('qn_bigpillar', CX + cx_, y, (-16, -14, 16, 0))
    for sx in (-1, 1):
        put('qn_beast', CX + sx * 90, 720, (-12, -8, 12, 0)); put('qn_lamp', CX + sx * 130, 700, (-5, -6, 5, 0))
        put('qn_crane', CX + sx * 440, 1100, (-9, -8, 9, 0)); put('qn_lamp', CX + sx * 430, 700, (-5, -6, 5, 0))
    # 偏殿：4 根柱、宝箱、灯、弩机
    for (x0, x1) in ((180, 620), (1780, 2220)):
        mx = (x0 + x1) // 2
        for (ox, oy) in ((-130, 830), (-130, 1030), (130, 830), (130, 1030)): put('qn_pillar', mx + ox, oy, (-9, -12, 9, 0))
        for oy in (790, 1060): put('qn_lamp', mx, oy, (-5, -6, 5, 0))
    put('qn_chest', 230, 790, (-12, -8, 12, 0)); put('qn_chest', 230, 1070, (-12, -8, 12, 0)); put('qn_bow', 560, 790, (-8, -8, 8, 0)); put('qn_bow', 560, 1070, (-8, -8, 8, 0))
    put('qn_chest', 2170, 790, (-12, -8, 12, 0)); put('qn_chest', 2170, 1070, (-12, -8, 12, 0)); put('qn_beast', 2190, 930, (-12, -8, 12, 0))
    put('qn_bow', 1840, 790, (-8, -8, 8, 0)); put('qn_bow', 1840, 1070, (-8, -8, 8, 0))
    # 机关迷宫：宝箱 / 灯 / 弩机
    for r_ in range(MR):
        for c_ in range(MC):
            cx_, cy_ = MX0 + c_ * MCELL + MCELL // 2, MY0 + r_ * MCELL + MCELL // 2 + 14
            roll = random.random()
            if roll < 0.14: put('qn_chest', cx_, cy_, (-12, -8, 12, 0))
            elif roll < 0.28: put('qn_lamp', cx_ + 22, cy_ - 6, (-5, -6, 5, 0))
            elif roll < 0.38: put('qn_bones', cx_, cy_ + 4, None)
            elif roll < 0.5: put('qn_bow', cx_, cy_ + 10, (-8, -8, 8, 0))
    # 陷阱房：房内灯、骸骨、弩机、终点宝箱
    put('qn_chest', 2195, 1530, (-12, -8, 12, 0)); put('qn_lamp', 2195, 1450, (-5, -6, 5, 0)); put('qn_lamp', 2195, 1620, (-5, -6, 5, 0))
    put('qn_bow', 1900, 1368, (-8, -8, 8, 0)); put('qn_bow', 2100, 1368, (-8, -8, 8, 0)); put('qn_bones', 1990, 1700, None)
    # 主墓室
    put('qn_coffin', CX, 250, (-70, -70, 70, 0))
    for sx in (-1, 1): put('qn_lamp', CX + sx * 150, 300, (-5, -6, 5, 0)); put('qn_beast', CX + sx * 100, 346, (-12, -8, 12, 0))

    # ---------- 通行网格 ----------
    cols, rows = W // CELL, H // CELL
    wm = np.array(walk.resize((cols, rows), Image.BILINEAR)) > 200
    grid = (~wm).astype(np.uint8)
    for (x0, y0, x1, y1) in blocks:
        grid[max(0, y0 // CELL): min(rows, y1 // CELL + 1), max(0, x0 // CELL): min(cols, x1 // CELL + 1)] = 1
    for r_ in range(rows):
        for c_ in range(cols):
            x, y = c_ * CELL + 4, r_ * CELL + 4
            if ((x - RC[0]) / 324) ** 2 + ((y - RC[1]) / 104) ** 2 < 1.0:
                on_platform = ((x - CX) / 106) ** 2 + ((y - 226) / 32) ** 2 < 1.0
                on_island = any(((x - ex) / er) ** 2 + ((y - ey) / (er * 0.6)) ** 2 < 1.0 for ex, ey, er in islands)
                on_path = abs(x - CX) < 34 and 250 <= y <= 362
                if not on_platform and not on_island and not on_path: grid[r_, c_] = 1
    for (xc, ya, yb, ww) in STAIRS:
        grid[ya // CELL: yb // CELL + 1, (xc - ww // 2) // CELL: (xc + ww // 2) // CELL + 1] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for v in grid.flatten()), objs=objs, w=W, h=H,
                start=[CX, 1890], boss=[CX, 226], graves=[], traps=traps, warriors=warriors)
    return im, sprites, data, SP


def preview(path, scale=1.0, crop=None):
    im, sprites, data, SP = build()
    full = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        spr, ax, ay = SP[o['img']]
        full.alpha_composite(spr, (int(o['x'] - ax), int(o['y'] - ay)))
    glow = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for o in data['objs']:
        if o['img'] == 'qn_lamp':
            for k, rr in enumerate((56, 34, 16)): g.ellipse([o['x'] - rr, o['y'] - 38 - rr * 0.8, o['x'] + rr, o['y'] - 38 + rr * 0.8], fill=(90, 230, 220, 14 + k * 8))
        if o['img'] == 'qn_coffin':
            for k, rr in enumerate((160, 100, 50)): g.ellipse([o['x'] - rr, o['y'] - 70 - rr * 0.5, o['x'] + rr, o['y'] - 70 + rr * 0.5], fill=(246, 210, 120, 12 + k * 8))
        if o['img'] == 'qn_hall':
            for k, rr in enumerate((180, 110, 50)): g.ellipse([o['x'] - rr, o['y'] - 90 - rr * 0.4, o['x'] + rr, o['y'] - 90 + rr * 0.4], fill=(246, 190, 100, 10 + k * 8))
    full.alpha_composite(glow)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'qin_preview.png', 0.4)
