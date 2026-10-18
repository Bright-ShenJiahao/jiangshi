"""第五章·地下皇宫（秦始皇陵）：自南向北——墓道、兵马俑坑、外门、前殿庭院、水银河、中殿、内宫门、主墓室（水银为江海、星象为天）。
东西两翼是石墙迷宫（机关、宝箱、人鱼膏长明灯）。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw
import map_jp as J
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW

W, H = 2200, 1700
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


def maze(x0, y0, cols, rows, cell, seed):
    """递归回溯迷宫：返回 (hwalls, vwalls)；hwalls[r][c] 表示 (r,c) 上方的墙是否存在"""
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
    for _ in range(cols * rows // 6):                                         # 凿开几处环路，让它不那么"死胡同"
        rr, cc = r.randrange(rows), r.randrange(1, cols)
        vw[rr][cc] = False
    return hw, vw


def build(seed=88):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), FLOOR[0] + (255,)); d = ImageDraw.Draw(im)
    blocks = []
    for _ in range(120000): im.putpixel((random.randrange(W), random.randrange(H)), random.choice(FLOOR) + (255,))
    for x in range(0, W, 28): d.line([(x, 0), (x, H)], fill=(28, 34, 40))
    for y in range(0, H, 28): d.line([(0, y), (W, y)], fill=(28, 34, 40))
    CX = 1100

    def wall_rect(x0, y0, x1, y1, face=10, solid=True):
        d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + face + 1], fill=K)
        d.rectangle([x0, y0, x1, y1], fill=WALL_T); d.rectangle([x0, y1, x1, y1 + face], fill=WALL_F)
        d.line([(x0, y1 + face - 1), (x1, y1 + face - 1)], fill=WALL_D)
        for x in range(x0 + 6, x1 - 2, 12): d.rectangle([x, y1 + 3, x + 5, y1 + 6], fill=(78, 84, 100))                      # 云雷纹
        for x in range(x0 + 2, x1, 14): d.point((x, y0 + 2), fill=(122, 126, 138))
        if solid: blocks.append((x0, y0, x1, y1 + face))

    # 外墙
    wall_rect(0, 0, W, 34); wall_rect(0, 0, 34, H - 20, 0); wall_rect(W - 34, 0, W, H - 20, 0)
    wall_rect(0, H - 40, CX - 70, H - 30); wall_rect(CX + 70, H - 40, W, H - 30)
    # ---- 墓道（南入口）----
    d.rectangle([CX - 70, 1520, CX + 70, H], fill=(44, 50, 56))
    for i in range(10): d.rectangle([CX - 70, 1520 + i * 18, CX + 70, 1520 + i * 18 + 6], fill=(70, 76, 86)); d.rectangle([CX - 70, 1520 + i * 18 + 6, CX + 70, 1520 + i * 18 + 16], fill=(52, 58, 66))
    # ---- 兵马俑坑（两侧，下沉）----
    pits = [(160, 1080, 840, 1440), (1360, 1080, 2040, 1440)]
    for (a, b, c, e) in pits:
        d.rectangle([a - 8, b - 8, c + 8, e + 8], fill=K); d.rectangle([a - 6, b - 6, c + 6, e + 6], fill=(96, 84, 76))
        d.rectangle([a, b, c, e], fill=(52, 40, 38))
        for x in range(a + 10, c, 44): d.rectangle([x, b, x + 20, e], fill=(60, 46, 42))                    # 夯土隔墙（俑坑的承重土墙）
        for _ in range(7000): im.putpixel((random.randrange(a, c), random.randrange(b, e)), random.choice([(60, 46, 42, 255), (46, 36, 34, 255), (68, 52, 46, 255)]))
        blocks.append((a - 8, b - 8, c + 8, b)); blocks.append((a - 8, e, c + 8, e + 8)); blocks.append((a - 8, b - 8, a, e + 8))
        blocks.append((c, b - 8, c + 8, e + 8)) if False else None
    blocks += [(840, 1072, 848, 1190), (840, 1340, 848, 1448), (1352, 1072, 1360, 1190), (1352, 1340, 1360, 1448)]     # 坑口留出入口
    for (a, b, c, e) in pits: d.rectangle([c - 8 if a < CX else a, 1190, c + 8 if a < CX else a + 8, 1340], fill=(52, 40, 38))
    # ---- 中轴石板路 ----
    d.rectangle([CX - 56, 140, CX + 56, 1520], fill=(44, 50, 56))
    for y in range(140, 1520, 20): d.line([(CX - 56, y), (CX + 56, y)], fill=(38, 44, 50))
    d.rectangle([CX - 6, 140, CX + 6, 1520], fill=(64, 70, 80))
    # ---- 外门（y=1010）----
    wall_rect(34, 1004, CX - 110, 1022); wall_rect(CX + 110, 1004, W - 34, 1022)
    # ---- 前殿庭院 y 700-1004 ----
    d.rectangle([34, 700, W - 34, 1004], fill=(38, 46, 50))
    for x in range(34, W - 34, 56):
        for y in range(700, 1004, 56): d.rectangle([x, y, x + 55, y + 55], outline=(32, 40, 46))
    # ---- 水银河 y≈640 ----
    def merc_y(x): return 640 + 22 * math.sin(x / 190) + 10 * math.sin(x / 61)
    MW = 96
    for x in range(34, W - 34):
        cy = merc_y(x)
        d.line([(x, cy - MW // 2 - 6), (x, cy + MW // 2 + 6)], fill=K); d.line([(x, cy - MW // 2 - 3), (x, cy + MW // 2 + 3)], fill=(88, 94, 104)); d.line([(x, cy - MW // 2), (x, cy + MW // 2)], fill=MERC_D)
    for _ in range(14000):
        x = random.randrange(34, W - 34); y = int(merc_y(x) + random.randint(-MW // 2, MW // 2)); im.putpixel((x, y), random.choice([MERC, MERC_L, MERC_D, (120, 140, 164, 255)]))
    for _ in range(300):
        x = random.randrange(34, W - 60); y = int(merc_y(x) + random.randint(-MW // 2 + 8, MW // 2 - 8)); d.line([(x, y), (x + 14, y)], fill=MERC_L)
    # 三座桥：中间大桥 + 左右小桥
    bridges = [CX, 520, 1680]
    for bx in bridges:
        bw = 56 if bx == CX else 36; cy = merc_y(bx)
        d.rectangle([bx - bw - 2, cy - MW // 2 - 14, bx + bw + 2, cy + MW // 2 + 14], fill=K); d.rectangle([bx - bw, cy - MW // 2 - 12, bx + bw, cy + MW // 2 + 12], fill=(96, 100, 110))
        for yy in range(int(cy - MW // 2 - 12), int(cy + MW // 2 + 12), 8): d.line([(bx - bw, yy), (bx + bw, yy)], fill=(80, 84, 96))
        for sx in (bx - bw, bx + bw - 4): d.rectangle([sx, cy - MW // 2 - 12, sx + 4, cy + MW // 2 + 12], fill=BRONZE); d.line([(sx + 1, cy - MW // 2 - 12), (sx + 1, cy + MW // 2 + 12)], fill=PATINA)
    # ---- 中殿 y 380-600 ----
    d.rectangle([34, 380, W - 34, 600], fill=(40, 48, 52))
    for x in range(34, W - 34, 56):
        for y in range(380, 600, 56): d.rectangle([x, y, x + 55, y + 55], outline=(34, 42, 48))
    # ---- 主墓室 y 40-370：圆形水银海 + 星象 ----
    d.rectangle([34, 34, W - 34, 380], fill=(30, 36, 48))
    for x in range(34, W - 34, 28): d.line([(x, 34), (x, 380)], fill=(26, 32, 44))
    for y in range(34, 380, 28): d.line([(34, y), (W - 34, y)], fill=(26, 32, 44))
    for _ in range(260):                                                            # 地面镶嵌的金色星象
        x, y = random.randrange(40, W - 40), random.randrange(40, 370)
        d.point((x, y), fill=random.choice([GOLD, GOLD_D, (150, 170, 220)]))
        if random.random() < 0.15: d.point((x + 1, y), fill=GOLD_L); d.point((x, y + 1), fill=GOLD_L)
    RC = (CX, 210)
    d.ellipse([RC[0] - 420, RC[1] - 150, RC[0] + 420, RC[1] + 150], fill=K); d.ellipse([RC[0] - 414, RC[1] - 144, RC[0] + 414, RC[1] + 144], fill=MERC_D)
    for _ in range(12000):
        a, rr = random.random() * 6.283, random.random() ** 0.5; im.putpixel((int(RC[0] + 410 * rr * math.cos(a)), int(RC[1] + 140 * rr * math.sin(a))), random.choice([MERC, MERC_L, MERC_D]))
    # 水银"九州"：几块不规则大陆（石岛）
    for (ex, ey, er) in ((CX - 260, 190, 40), (CX - 180, 250, 26), (CX + 260, 200, 44), (CX + 200, 160, 30), (CX - 330, 150, 22), (CX + 330, 260, 24)):
        d.ellipse([ex - er, ey - er * 0.6, ex + er, ey + er * 0.6], fill=K); d.ellipse([ex - er + 2, ey - er * 0.6 + 2, ex + er - 2, ey + er * 0.6 - 2], fill=(60, 78, 66))
    d.ellipse([CX - 130, 170, CX + 130, 262], fill=K); d.ellipse([CX - 126, 174, CX + 126, 258], fill=(80, 84, 94))      # 中央石台
    for a in range(0, 360, 20): d.ellipse([CX + 120 * math.cos(math.radians(a)) - 4, 216 + 40 * math.sin(math.radians(a)) - 3, CX + 120 * math.cos(math.radians(a)) + 4, 216 + 40 * math.sin(math.radians(a)) + 3], fill=GOLD)
    # 内宫门 y=380
    wall_rect(34, 374, CX - 90, 392); wall_rect(CX + 90, 374, W - 34, 392)
    # ---- 左右迷宫（前殿以北到中殿的两翼 + 前殿以南）----
    MZ = []
    # 西翼迷宫 x 60-440? 用 y 1030-1070? 迷宫放在东西两侧 y 400-960 里不合适(殿内)。改为：殿以南 y 1030..1070 是外门；迷宫放前殿两翼 x 60..420 / 1780..2140，y 720..1000
    def build_maze(x0, y0, cols, rows, cell, seed, gate_side):
        hw, vw = maze(x0, y0, cols, rows, cell, seed); T = 14
        for r_ in range(rows + 1):
            for c_ in range(cols):
                if hw[r_][c_]:
                    if r_ in (0, rows) and False: continue
                    wall_rect(x0 + c_ * cell - T // 2, y0 + r_ * cell - T // 2, x0 + (c_ + 1) * cell + T // 2, y0 + r_ * cell + T // 2, 8)
        for r_ in range(rows):
            for c_ in range(cols + 1):
                if vw[r_][c_]:
                    if c_ == (cols if gate_side == 'E' else 0) and r_ in (rows // 2, rows // 2 - 1): continue         # 迷宫朝向中殿一侧开口
                    wall_rect(x0 + c_ * cell - T // 2, y0 + r_ * cell - T // 2, x0 + c_ * cell + T // 2, y0 + (r_ + 1) * cell + T // 2, 8)
        return hw, vw
    # 迷宫区域：西 x 70..470 (4 cols×100)… 使用 cell=110
    WEST = (70, 424, 5, 7, 80); EAST = (1730, 424, 5, 7, 80)
    # 把迷宫区域放在前殿与中殿的两侧会与殿重叠，所以让迷宫占据 y 420..970（中殿+前殿侧面），殿的主体宽度限制在 x 560..1640
    d.rectangle([34, 392, 520, 1004], fill=(34, 40, 46)); d.rectangle([1680, 392, W - 34, 1004], fill=(34, 40, 46))
    for x in range(34, 520, 28): d.line([(x, 392), (x, 1004)], fill=(28, 34, 40))
    for x in range(1680, W - 34, 28): d.line([(x, 392), (x, 1004)], fill=(28, 34, 40))
    build_maze(*WEST[:4], WEST[4], 11, 'E'); build_maze(*EAST[:4], EAST[4], 29, 'W')
    # 殿侧墙（迷宫与殿之间）
    wall_rect(520, 392, 534, 640, 6); wall_rect(520, 740, 534, 1004, 6); wall_rect(1666, 392, 1680, 640, 6); wall_rect(1666, 740, 1680, 1004, 6)
    # 外围迷宫 2（南部两侧：兵马俑坑上方）
    d.rectangle([34, 1022, 150, 1500], fill=(34, 40, 46)); d.rectangle([2050, 1022, W - 34, 1500], fill=(34, 40, 46))

    # 边界已在 wall_rect
    # ---------------- 物件 ----------------
    SP = {k: f() for k, f in SPRITES.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    # 墓道火炬
    for y in (1560, 1620): put('qn_lamp', CX - 56, y, (-5, -6, 5, 0)); put('qn_lamp', CX + 56, y, (-5, -6, 5, 0))
    # 外门
    put('qn_gate', CX, 1022, None); blocks += [(CX - 110 - 60, 1004, CX - 110, 1022), (CX + 110, 1004, CX + 110 + 60, 1022)]
    for sx in (-1, 1): put('qn_beast', CX + sx * 150, 1060, (-12, -8, 12, 0))
    # 兵马俑：整齐列阵（每坑 5 路纵队，面向北）
    for pi, (a, b, c, e) in enumerate(pits):
        for col_ in range(6):
            x = a + 50 + col_ * 110
            for row_ in range(7):
                y = b + 54 + row_ * 46
                if random.random() < 0.08: continue
                put('qn_warrior%d' % ((col_ + row_) % 3), x + random.randint(-2, 2), y, (-6, -8, 6, 0))
    # 铜车马
    put('qn_chariot', 520, 1010 - 20, (-30, -14, 30, 0)) if False else None
    put('qn_chariot', 640, 900, (-30, -14, 30, 0)); put('qn_chariot', 1560, 900, (-30, -14, 30, 0))
    # 前殿：两排漆柱、长明灯
    for x in range(560, 1660, 130):
        if abs(x - CX) < 70: continue
        put('qn_pillar', x, 790, (-9, -12, 9, 0)); put('qn_pillar', x, 960, (-9, -12, 9, 0))
    for x in (CX - 120, CX + 120): put('qn_lamp', x, 880, (-5, -6, 5, 0))
    for sx in (-1, 1): put('qn_crane', CX + sx * 200, 860, (-9, -8, 9, 0))
    # 中殿：柱列
    for x in range(560, 1660, 130):
        if abs(x - CX) < 70: continue
        put('qn_pillar', x, 440, (-9, -12, 9, 0)); put('qn_pillar', x, 580, (-9, -12, 9, 0))
    for x in (CX - 150, CX + 150): put('qn_lamp', x, 520, (-5, -6, 5, 0))
    # 迷宫内：宝箱、灯、骸骨、弩机（随机放在迷宫格中心）
    for (x0, y0, cols, rows, cell) in (WEST, EAST):
        for r_ in range(rows):
            for c_ in range(cols):
                cx_, cy_ = x0 + c_ * cell + cell // 2, y0 + r_ * cell + cell // 2 + 14
                roll = random.random()
                if roll < 0.18: put('qn_chest', cx_, cy_, (-12, -8, 12, 0))
                elif roll < 0.32: put('qn_lamp', cx_ + 22, cy_ - 6, (-5, -6, 5, 0))
                elif roll < 0.44: put('qn_bones', cx_, cy_ + 4, None)
                elif roll < 0.54: put('qn_bow', cx_, cy_ + 10, (-8, -8, 8, 0))
    # 主墓室
    put('qn_coffin', CX, 270, (-70, -70, 70, 0))
    for sx in (-1, 1): put('qn_lamp', CX + sx * 150, 310, (-5, -6, 5, 0)); put('qn_beast', CX + sx * 100, 360, (-12, -8, 12, 0))
    for x in range(CX - 300, CX + 301, 100):
        if abs(x - CX) < 140: continue
        put('qn_pillar', x, 372, (-9, -12, 9, 0))

    # ---------------- 通行网格 ----------------
    cols, rows = W // CELL, H // CELL
    grid = [[0] * cols for _ in range(rows)]
    for (x0, y0, x1, y1) in blocks:
        for r_ in range(max(0, y0 // CELL), min(rows, y1 // CELL + 1)):
            for c_ in range(max(0, x0 // CELL), min(cols, x1 // CELL + 1)): grid[r_][c_] = 1
    for c_ in range(cols):                                                      # 水银河：不可走，桥可走
        x = c_ * CELL + 4
        if x < 40 or x > W - 40: continue
        cy = merc_y(x)
        for r_ in range(int((cy - MW // 2 - 6) // CELL), int((cy + MW // 2 + 6) // CELL) + 1):
            if any(abs(x - bx) < (58 if bx == CX else 38) for bx in bridges): continue
            if 0 <= r_ < rows: grid[r_][c_] = 1
    # 主墓室水银海：椭圆内不可走（中央石台 + 石岛可走）
    for r_ in range(rows):
        for c_ in range(cols):
            x, y = c_ * CELL + 4, r_ * CELL + 4
            if ((x - RC[0]) / 410) ** 2 + ((y - RC[1]) / 140) ** 2 < 1.0:
                on_platform = ((x - CX) / 128) ** 2 + ((y - 216) / 42) ** 2 < 1.0
                on_island = any(((x - ex) / er) ** 2 + ((y - ey) / (er * 0.6)) ** 2 < 1.0 for ex, ey, er in ((CX - 260, 190, 40), (CX - 180, 250, 26), (CX + 260, 200, 44), (CX + 200, 160, 30), (CX - 330, 150, 22), (CX + 330, 260, 24)))
                if not on_platform and not on_island: grid[r_][c_] = 1
    # 中央石台通路：从内宫门到石台留出石桥
    for r_ in range(int(256 // CELL), int(380 // CELL) + 1):
        for c_ in range(int((CX - 34) // CELL), int((CX + 34) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(1020 // CELL), int(1500 // CELL)):                    # 中轴走廊
        for c_ in range(int((CX - 56) // CELL), int((CX + 56) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(1500 // CELL), rows):
        for c_ in range(int((CX - 70) // CELL), int((CX + 70) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(1022 // CELL), int(1060 // CELL)):
        for c_ in range(int((CX - 110) // CELL), int((CX + 110) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(392 // CELL), int(1004 // CELL)):                      # 殿内主通道（避开柱）
        for c_ in range(int((CX - 40) // CELL), int((CX + 40) // CELL)): grid[r_][c_] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for row in grid for v in row), objs=objs, w=W, h=H,
                start=[CX, 1560], boss=[CX, 216], graves=[])
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
    full.alpha_composite(glow)
    # 暗角：地下很黑，只有灯光附近亮
    vig = Image.new('RGBA', full.size, (0, 0, 0, 70)); full.alpha_composite(vig)
    full.alpha_composite(glow)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'qin_preview.png', 0.45)
