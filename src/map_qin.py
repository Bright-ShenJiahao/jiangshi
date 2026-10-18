"""第五章·地底天宫（秦始皇陵）：巨大的地下空腔里，一座座石台悬浮在虚空中，彼此用悬浮的台阶、吊桥相连。
自南向北——墓道口 → 兵马俑大军台 → 悬浮台阶 → 浮空宫殿（大殿）→ 悬浮台阶 → 主墓室（水银海、星象穹顶）；东西两侧是悬空的石墙迷宫。脚下深处是发光的水银河。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw
import map_jp as J
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW

W, H = 2200, 1800
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


def build(seed=88):
    random.seed(seed)
    CX = 1100
    # ---------- 虚空：深蓝黑 + 星 + 脚下很深处发光的水银河 ----------
    base = Image.new('RGBA', (W, H), (8, 10, 22, 255)); bd = ImageDraw.Draw(base)
    for _ in range(2600):
        x, y = random.randrange(W), random.randrange(H)
        bd.point((x, y), fill=random.choice([(60, 70, 110, 255), (90, 100, 150, 255), (140, 150, 200, 255), (200, 190, 130, 255)]))
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    pts = [(-40, 1320)]
    for x in range(0, W + 120, 120): pts.append((x, 1320 + int(260 * math.sin(x / 330) + 90 * math.sin(x / 97))))
    gd.line(pts, fill=(70, 200, 210, 150), width=90); gd.line(pts, fill=(200, 240, 250, 170), width=26)
    pts2 = [(x, y - 780) for (x, y) in pts]
    gd.line(pts2, fill=(70, 160, 200, 90), width=70); gd.line(pts2, fill=(190, 230, 250, 100), width=18)
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    base.alpha_composite(glow)
    # 远处的悬挂锁链（垂直暗线）
    for _ in range(30):
        x = random.randrange(W); y0 = random.randrange(0, H // 2); L = random.randrange(120, 420)
        for k in range(0, L, 6): bd.rectangle([x, y0 + k, x + 2, y0 + k + 3], fill=(26, 28, 44, 255))
    im = base; d = ImageDraw.Draw(im)
    walk = Image.new('L', (W, H), 0); wd = ImageDraw.Draw(walk)               # 可行走遮罩
    blocks = []

    def island(shape, floor_col=(62, 66, 78), grid_col=(52, 56, 68), under=28):
        """shape(draw, fill) 把形状画进遮罩；画出：投影 → 岩石底 → 地面"""
        m = Image.new('L', (W, H), 0); shape(ImageDraw.Draw(m), 255)
        sh = ImageChops.offset(m, 6, 54).filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.55))
        im.paste((0, 0, 0, 255), (0, 0), sh)
        rock = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(rock)
        for k in range(1, under + 1):                                      # 岩石底：逐层下移，越往下越窄、越暗
            mm = ImageChops.offset(m, 0, k)
            tone = int(52 - k * 0.9)
            rock.paste((tone, tone - 4, tone + 8, 255), (0, 0), mm)
        im.alpha_composite(rock)
        nz = np.array(m)
        # 岩石尖刺（钟乳石）
        ys, xs = np.nonzero(nz > 0)
        edge = {}
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

    def seq(*shapes):
        return lambda dd, f: [sh(dd, f) for sh in shapes]

    # ---------- 各座浮空石台 ----------
    ENT = (CX - 120, 1620, CX + 120, 1770)
    ARMY = (260, 1030, 1940, 1500)
    PAL_C, PAL_R = (CX, 690), (300, 190)
    BUR_C, BUR_R = (CX, 240), (380, 170)
    WM = (110, 560, 650, 1000); EM = (1550, 560, 2090, 1000)
    island(rect_shape(*ENT, 6, 1))
    island(rect_shape(*ARMY, 16, 2), (58, 52, 56), (50, 44, 50))                    # 兵马俑大军台：土褐色
    island(rough_ellipse(*PAL_C, *PAL_R, 10, 3))
    island(rough_ellipse(*BUR_C, *BUR_R, 10, 4), (50, 56, 76), (42, 48, 68))
    island(rect_shape(*WM, 10, 5)); island(rect_shape(*EM, 10, 6))
    # ---------- 悬浮台阶 / 吊桥（也记入可行走遮罩）----------
    def floating_stairs(xc, y_from, y_to, wdt=96, step=16, flights=1):
        """y_from→y_to 的一段悬浮台阶：每级是一块单独悬着的石板，下面有投影"""
        ys = list(range(min(y_from, y_to), max(y_from, y_to), step))
        for k, y in enumerate(ys):
            sx = int(6 * math.sin(k * 1.7))                                         # 略微错落，像悬着
            d.rectangle([xc - wdt // 2 + sx + 6, y + 14, xc + wdt // 2 + sx + 6, y + 22], fill=(4, 6, 14, 255))
            d.rectangle([xc - wdt // 2 + sx - 1, y - 1, xc + wdt // 2 + sx + 1, y + 11], fill=K)
            d.rectangle([xc - wdt // 2 + sx, y, xc + wdt // 2 + sx, y + 9], fill=(112, 116, 134) if k % 2 else (134, 138, 156))
            d.rectangle([xc - wdt // 2 + sx, y + 6, xc + wdt // 2 + sx, y + 9], fill=(78, 82, 100))
            d.point((xc - wdt // 2 + sx + 3, y + 2), fill=(190, 194, 210))
        wd.rectangle([xc - wdt // 2 - 6, min(y_from, y_to) - 4, xc + wdt // 2 + 6, max(y_from, y_to) + 12], fill=255)
        for yy in range(min(y_from, y_to) + 10, max(y_from, y_to), 50):              # 两侧悬浮的长明灯
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
    floating_stairs(CX, 1500, 1620, 100, 14)                                       # 入口 → 大军台
    floating_stairs(CX, 840, 1040, 110, 16)                                        # 大军台 → 宫殿台（悬浮台阶）
    floating_stairs(CX, 400, 520, 90, 14)                                          # 宫殿台 → 主墓室
    plank_bridge(640, 860, 780); plank_bridge(1340, 1560, 780)                      # 宫殿台 ↔ 东西迷宫台
    # 大军台两端的悬浮踏石，通向迷宫台的下沿（一块块单独悬着的方石）
    for (sx0, sy0, dx_, dy_) in ((300, 1030, 0, -1), (1900, 1030, 0, -1)):
        for k in range(1, 8):
            x, y = sx0 + k * 12 * (1 if sx0 < CX else -1) * 0, sy0 - k * 20
            d.rectangle([x - 18 + 5, y + 10, x + 18 + 5, y + 22], fill=(4, 6, 14, 255)); d.rectangle([x - 19, y - 1, x + 19, y + 13], fill=K); d.rectangle([x - 18, y, x + 18, y + 11], fill=(120, 124, 142) if k % 2 else (140, 144, 160))
            wd.rectangle([x - 24, y - 4, x + 24, y + 14], fill=255)
    # 脚下的水银瀑布：从宫殿台两侧边缘流下
    for sx in (-1, 1):
        x = CX + sx * 290
        for k in range(60):
            a = 180 - k * 3
            if a > 0: d.line([(x - 5 + (k % 3), 700 + k * 2 + 30), (x + 5 + (k % 3), 700 + k * 2 + 30)], fill=(190, 220, 240, 255))

    # ---------- 墙体 ----------
    def wall_rect(x0, y0, x1, y1, face=10, solid=True):
        d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + face + 1], fill=K)
        d.rectangle([x0, y0, x1, y1], fill=WALL_T); d.rectangle([x0, y1, x1, y1 + face], fill=WALL_F)
        d.line([(x0, y1 + face - 1), (x1, y1 + face - 1)], fill=WALL_D)
        for x in range(x0 + 6, x1 - 2, 12): d.rectangle([x, y1 + 3, x + 5, y1 + 6], fill=(78, 84, 100))
        if solid: blocks.append((x0, y0, x1, y1 + face))
    # 迷宫（东西悬空台）
    def build_maze(x0, y0, cols, rows, cell, seed, open_side):
        hw, vw = maze(x0, y0, cols, rows, cell, seed); T = 14
        for r_ in range(rows + 1):
            for c_ in range(cols):
                if hw[r_][c_]: wall_rect(x0 + c_ * cell - T // 2, y0 + r_ * cell - T // 2, x0 + (c_ + 1) * cell + T // 2, y0 + r_ * cell + T // 2, 8)
        for r_ in range(rows):
            for c_ in range(cols + 1):
                if vw[r_][c_]:
                    if c_ == (cols if open_side == 'E' else 0) and r_ in (rows // 2, rows // 2 - 1, rows // 2 + 1): continue
                    wall_rect(x0 + c_ * cell - T // 2, y0 + r_ * cell - T // 2, x0 + c_ * cell + T // 2, y0 + (r_ + 1) * cell + T // 2, 8)
    WMZ = (140, 600, 6, 5, 84); EMZ = (1560, 600, 6, 5, 84)
    build_maze(*WMZ[:4], WMZ[4], 11, 'E'); build_maze(*EMZ[:4], EMZ[4], 29, 'W')

    # 宫殿台：黄金环 + 云纹
    d.ellipse([CX - 210, 690 - 130, CX + 210, 690 + 130], outline=GOLD_D, width=2); d.ellipse([CX - 190, 690 - 118, CX + 190, 690 + 118], outline=(120, 92, 60), width=1)
    for a in range(0, 360, 15):
        d.ellipse([CX + 200 * math.cos(math.radians(a)) - 3, 690 + 124 * math.sin(math.radians(a)) - 2, CX + 200 * math.cos(math.radians(a)) + 3, 690 + 124 * math.sin(math.radians(a)) + 2], fill=GOLD)
    # 主墓室台：水银海 + 石岛 + 中央石台（天象由虚空背景承担）
    RC = BUR_C
    d.ellipse([RC[0] - 330, RC[1] - 110, RC[0] + 330, RC[1] + 110], fill=K); d.ellipse([RC[0] - 324, RC[1] - 104, RC[0] + 324, RC[1] + 104], fill=MERC_D)
    for _ in range(9000):
        a, rr = random.random() * 6.283, random.random() ** 0.5; im.putpixel((int(RC[0] + 320 * rr * math.cos(a)), int(RC[1] + 100 * rr * math.sin(a))), random.choice([MERC, MERC_L, MERC_D]))
    islands = ((CX - 230, 220, 36), (CX + 230, 230, 40), (CX - 150, 290, 24), (CX + 160, 170, 28))
    for (ex, ey, er) in islands:
        d.ellipse([ex - er, ey - er * 0.6, ex + er, ey + er * 0.6], fill=K); d.ellipse([ex - er + 2, ey - er * 0.6 + 2, ex + er - 2, ey + er * 0.6 - 2], fill=(60, 78, 66))
    d.ellipse([CX - 110, 190, CX + 110, 262], fill=K); d.ellipse([CX - 106, 194, CX + 106, 258], fill=(80, 84, 94))

    # ---------- 物件 ----------
    SP = {k: f() for k, f in SPRITES.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    put('qn_gateS', CX, 1700, None); blocks += [(CX - 120, 1680, CX - 60, 1720), (CX + 60, 1680, CX + 120, 1720)]
    for y in (1650, 1700): put('qn_lamp', CX - 80, y, (-5, -6, 5, 0)); put('qn_lamp', CX + 80, y, (-5, -6, 5, 0))
    # 兵马俑大军
    for rr in range(9):
        for cc in range(26):
            x = 320 + cc * 62; y = 1090 + rr * 44
            if abs(x - CX) < 70 and y < 1180: continue                         # 中间留出通道
            if abs(x - CX) < 36: continue
            if random.random() < 0.06: continue
            put('qn_warrior%d' % ((cc + rr) % 3), x + random.randint(-2, 2), y, (-6, -8, 6, 0))
    for x in (520, 1680): put('qn_chariot', x, 1480, (-30, -14, 30, 0))
    for sx in (-1, 1): put('qn_beast', CX + sx * 90, 1480, (-12, -8, 12, 0)); put('qn_lamp', CX + sx * 150, 1180, (-5, -6, 5, 0))
    # 宫殿
    put('qn_hall', CX, 690, (-130, -96, 130, 0))
    for x in (CX - 250, CX - 190, CX + 190, CX + 250): put('qn_pillar', x, 740, (-9, -12, 9, 0))
    for sx in (-1, 1): put('qn_crane', CX + sx * 150, 810, (-9, -8, 9, 0)); put('qn_lamp', CX + sx * 220, 690, (-5, -6, 5, 0))
    for sx in (-1, 1): put('qn_beast', CX + sx * 76, 850, (-12, -8, 12, 0))
    # 迷宫宝箱、灯、骸骨、弩机
    for (x0, y0, cols, rows, cell) in (WMZ, EMZ):
        for r_ in range(rows):
            for c_ in range(cols):
                cx_, cy_ = x0 + c_ * cell + cell // 2, y0 + r_ * cell + cell // 2 + 14
                roll = random.random()
                if roll < 0.18: put('qn_chest', cx_, cy_, (-12, -8, 12, 0))
                elif roll < 0.32: put('qn_lamp', cx_ + 22, cy_ - 6, (-5, -6, 5, 0))
                elif roll < 0.44: put('qn_bones', cx_, cy_ + 4, None)
                elif roll < 0.54: put('qn_bow', cx_, cy_ + 10, (-8, -8, 8, 0))
    # 主墓室
    put('qn_coffin', CX, 250, (-70, -70, 70, 0))
    for sx in (-1, 1): put('qn_lamp', CX + sx * 150, 300, (-5, -6, 5, 0)); put('qn_beast', CX + sx * 100, 346, (-12, -8, 12, 0))

    # ---------- 通行网格 ----------
    cols, rows = W // CELL, H // CELL
    wm = np.array(walk.resize((cols, rows), Image.BILINEAR)) > 200               # 只有整格都在石台/台阶上才可走
    grid = (~wm).astype(np.uint8)
    for (x0, y0, x1, y1) in blocks:
        grid[max(0, y0 // CELL): min(rows, y1 // CELL + 1), max(0, x0 // CELL): min(cols, x1 // CELL + 1)] = 1
    for r_ in range(rows):                                                      # 主墓室水银海：不可走，石岛/中央石台可走
        for c_ in range(cols):
            x, y = c_ * CELL + 4, r_ * CELL + 4
            if ((x - RC[0]) / 324) ** 2 + ((y - RC[1]) / 104) ** 2 < 1.0:
                on_platform = ((x - CX) / 106) ** 2 + ((y - 226) / 32) ** 2 < 1.0
                on_island = any(((x - ex) / er) ** 2 + ((y - ey) / (er * 0.6)) ** 2 < 1.0 for ex, ey, er in islands)
                if not on_platform and not on_island: grid[r_, c_] = 1
    # 台阶所在行列保持畅通
    for (xc, ya, yb, ww) in ((CX, 1500, 1620, 100), (CX, 840, 1040, 110), (CX, 400, 520, 90)):
        grid[ya // CELL: yb // CELL + 1, (xc - ww // 2) // CELL: (xc + ww // 2) // CELL + 1] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for v in grid.flatten()), objs=objs, w=W, h=H,
                start=[CX, 1700], boss=[CX, 226], graves=[])
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
