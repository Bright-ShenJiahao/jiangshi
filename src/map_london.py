"""第四章·欧洲（雾都伦敦）：维多利亚晚期的雾夜。北面是国会大厦与大本钟，泰晤士河与塔桥横在城南，
西边荒原（狼人）、西侧实验室（科学怪人）、东边哥特墓园和吸血鬼地下墓室、东南炼金术士与黑魔法师宅邸，河南是码头贫民窟（丧尸）。
build() 返回 (bg图, sprites字典, data字典, SP锚点表)。"""
import math, random
from PIL import Image, ImageDraw, ImageFont
import map_jp as J
import map_heian as Hn
import map_nanyang as Ny
from map_jp import K, canvas, box, shadow, STONE, STONE_D, STONE_L, WOOD, WOOD_D, RED, RED_D, RED_L, GLOW

W, H = 2200, 1600
CELL = 8
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
COBBLE = [(58, 64, 80), (52, 58, 74), (64, 70, 86)]
GRASS = [(30, 62, 54), (26, 54, 50), (38, 72, 60)]
BRICK, BRICK_D, BRICK_L = (122, 66, 60), (90, 48, 48), (156, 92, 76)
SAND, SAND_D, SAND_L = (158, 144, 118), (120, 108, 92), (190, 176, 146)
SLATE, SLATE_D, SLATE_L = (48, 54, 70), (34, 40, 54), (78, 86, 108)
THAMES, THAMES_D, THAMES_L = (26, 48, 70), (18, 36, 56), (66, 100, 130)
ELEC = (120, 200, 255)


def fnt(sz):
    try: return ImageFont.truetype(FONT, sz, index=2)
    except Exception: return ImageFont.load_default()


def terrace(w=76, var=0, floors=3):
    """联排砖房：红褐砖墙、白窗框、石板屋顶带烟囱、门前台阶"""
    r = random.Random(var * 9 + 2)
    fh = 30; h = fh * floors + 40
    im, d = canvas(w + 12, h); x0 = 6; cx = (w + 12) // 2; by = h - 3
    shadow(d, cx, by, w // 2 + 3, 4)
    top = by - fh * floors - 4
    d.rectangle([x0, top, x0 + w, by], fill=K); d.rectangle([x0 + 1, top + 1, x0 + w - 1, by - 1], fill=BRICK if var % 2 == 0 else (110, 74, 66))
    for y in range(top + 2, by, 4): d.line([(x0 + 1, y), (x0 + w - 1, y)], fill=BRICK_D)
    for y in range(top + 4, by, 8):
        for x in range(x0 + 3 + (y // 8 % 2) * 3, x0 + w - 2, 6): d.point((x, y), fill=BRICK_L)
    d.polygon([(x0 - 4, top + 2), (x0 + w + 4, top + 2), (x0 + w - 6, top - 14), (x0 + 6, top - 14)], fill=K)
    d.polygon([(x0 - 3, top + 1), (x0 + w + 3, top + 1), (x0 + w - 5, top - 13), (x0 + 5, top - 13)], fill=SLATE)
    for x in range(x0 - 2, x0 + w + 3, 4): d.line([(x, top + 1), (x + (cx - x) // 8, top - 12)], fill=SLATE_D)
    for ch in (x0 + 12, x0 + w - 14):
        d.rectangle([ch - 4, top - 24, ch + 4, top - 10], fill=K); d.rectangle([ch - 3, top - 23, ch + 3, top - 11], fill=BRICK_D)
        for ox in (-2, 1): d.rectangle([ch + ox, top - 30, ch + ox + 2, top - 24], fill=K); d.rectangle([ch + ox + 1, top - 29, ch + ox + 1, top - 25], fill=(150, 90, 70))
    for k in range(floors):
        y1 = top + 6 + k * fh; n = 2 if w < 90 else 3
        for i in range(n):
            wx = x0 + 8 + i * (w - 16) // n + (0 if k < floors - 1 else (w - 16) // n // 3 if i == n - 1 and False else 0)
            ww = (w - 16) // n - 8
            if k == floors - 1 and i == 0: continue                                    # 底层这一格是门
            lit = r.random() < 0.3
            d.rectangle([wx - 1, y1 - 1, wx + ww + 1, y1 + 19], fill=(214, 210, 196)); d.rectangle([wx, y1, wx + ww, y1 + 18], fill=(242, 202, 112) if lit else (28, 34, 52))
            d.line([(wx + ww // 2, y1), (wx + ww // 2, y1 + 18)], fill=(214, 210, 196)); d.line([(wx, y1 + 9), (wx + ww, y1 + 9)], fill=(214, 210, 196))
    dx = x0 + 8 + (w - 16) // (2 if w < 90 else 3) // 2 - 2
    d.rectangle([dx - 7, by - 24, dx + 7, by], fill=K); d.rectangle([dx - 6, by - 23, dx + 6, by - 1], fill=(40, 70, 70))
    d.ellipse([dx - 6, by - 28, dx + 6, by - 20], fill=(244, 200, 110)); d.rectangle([dx - 6, by - 24, dx + 6, by - 1], fill=(40, 70, 70)); d.point((dx + 4, by - 10), fill=(220, 190, 90))
    for y in range(by - 3, by + 1): d.line([(dx - 9, y), (dx + 9, y)], fill=(130, 126, 136))
    return im, cx, by


def parliament():
    """国会大厦 + 大本钟：砂岩哥特立面，尖拱窗，尖顶；左侧是钟楼"""
    w, h = 400, 250
    im, d = canvas(w, h); by = h - 4
    shadow(d, 200, by, 190, 8)
    x0, x1 = 70, 390
    box(d, x0, by - 90, x1, by, SAND)
    d.rectangle([x0 + 1, by - 90, x1 - 1, by - 84], fill=SAND_L)
    for x in range(x0 + 12, x1 - 6, 26):
        d.rectangle([x - 1, by - 76, x + 11, by - 8], fill=SAND_D)
        d.polygon([(x - 1, by - 76), (x + 11, by - 76), (x + 5, by - 90)], fill=SAND_D) if False else None
        d.rectangle([x, by - 70, x + 10, by - 8], fill=(246, 204, 112) if (x // 26) % 3 else (60, 54, 70))
        d.polygon([(x - 1, by - 70), (x + 11, by - 70), (x + 5, by - 82)], fill=K); d.polygon([(x, by - 70), (x + 10, by - 70), (x + 5, by - 79)], fill=(246, 204, 112) if (x // 26) % 3 else (60, 54, 70))
        d.line([(x + 5, by - 70), (x + 5, by - 8)], fill=SAND_D); d.line([(x, by - 40), (x + 10, by - 40)], fill=SAND_D)
    for x in range(x0 + 4, x1, 26): d.rectangle([x - 1, by - 88, x + 1, by - 6], fill=SAND_L)
    d.polygon([(x0 - 2, by - 90), (x1 + 2, by - 90), (x1 - 12, by - 112), (x0 + 12, by - 112)], fill=K)
    d.polygon([(x0, by - 91), (x1, by - 91), (x1 - 12, by - 110), (x0 + 12, by - 110)], fill=SLATE)
    for x in range(x0 + 4, x1, 5): d.line([(x, by - 91), (x + (230 - x) // 14, by - 110)], fill=SLATE_D)
    for x in range(x0 + 20, x1, 52):                                                       # 小尖塔
        d.rectangle([x - 3, by - 126, x + 3, by - 108], fill=K); d.rectangle([x - 2, by - 125, x + 2, by - 109], fill=SAND); d.polygon([(x - 4, by - 124), (x + 4, by - 124), (x, by - 140)], fill=K); d.polygon([(x - 3, by - 125), (x + 3, by - 125), (x, by - 137)], fill=SLATE_L)
    # 大本钟塔
    tx0, tx1 = 6, 62
    box(d, tx0, by - 176, tx1, by, SAND); d.rectangle([tx0 + 1, by - 176, tx1 - 1, by - 170], fill=SAND_L)
    for y in range(by - 8, by - 150, -22):
        d.rectangle([tx0 + 8, y - 18, tx0 + 14, y - 4], fill=(246, 204, 112)); d.polygon([(tx0 + 8, y - 18), (tx0 + 14, y - 18), (tx0 + 11, y - 24)], fill=(246, 204, 112))
        d.rectangle([tx1 - 14, y - 18, tx1 - 8, y - 4], fill=(246, 204, 112)); d.polygon([(tx1 - 14, y - 18), (tx1 - 8, y - 18), (tx1 - 11, y - 24)], fill=(246, 204, 112))
    for x in (tx0 + 2, tx1 - 2): d.rectangle([x - 2, by - 176, x + 2, by], fill=SAND_L)
    cx_, cy_ = 34, by - 134
    d.ellipse([cx_ - 22, cy_ - 22, cx_ + 22, cy_ + 22], fill=K); d.ellipse([cx_ - 20, cy_ - 20, cx_ + 20, cy_ + 20], fill=(180, 150, 70)); d.ellipse([cx_ - 17, cy_ - 17, cx_ + 17, cy_ + 17], fill=(248, 240, 206))
    for a in range(0, 360, 30): d.point((cx_ + 15 * math.cos(math.radians(a)), cy_ + 15 * math.sin(math.radians(a))), fill=K)
    d.line([(cx_, cy_), (cx_, cy_ - 12)], fill=K, width=2); d.line([(cx_, cy_), (cx_ + 8, cy_ + 5)], fill=K, width=2)
    d.polygon([(tx0 - 2, by - 176), (tx1 + 2, by - 176), (tx1 - 6, by - 196), (tx0 + 6, by - 196)], fill=K); d.polygon([(tx0, by - 177), (tx1, by - 177), (tx1 - 6, by - 195), (tx0 + 6, by - 195)], fill=SAND_D)
    d.polygon([(tx0 + 6, by - 196), (tx1 - 6, by - 196), (34, by - 244)], fill=K); d.polygon([(tx0 + 8, by - 197), (tx1 - 8, by - 197), (34, by - 240)], fill=(60, 96, 84))
    for y in range(by - 200, by - 240, -6): d.line([(34 - (by - 196 - y) // 3 * 0 - (y - (by - 240)) // 3, y), (34 + (y - (by - 240)) // 3, y)], fill=(40, 70, 64))
    d.ellipse([31, by - 250, 37, by - 244], fill=(210, 176, 80))
    return im, 34 + (w // 2 - 34), by


def tower_bridge():
    """塔桥：两座哥特塔楼 + 高空步道，桥面从塔间穿过"""
    w, h = 400, 190
    im, d = canvas(w, h); by = h - 4
    for tx in (60, 340):
        box(d, tx - 36, by - 140, tx + 36, by, (112, 120, 138)); d.rectangle([tx - 35, by - 140, tx + 35, by - 134], fill=(150, 158, 176))
        for yy in range(by - 6, by - 126, -24):
            for ox in (-18, 6): d.rectangle([tx + ox, yy - 16, tx + ox + 10, yy - 4], fill=(246, 204, 112)); d.polygon([(tx + ox, yy - 16), (tx + ox + 10, yy - 16), (tx + ox + 5, yy - 24)], fill=(246, 204, 112))
        for ox in (-36, 36):
            d.rectangle([tx + ox - 5, by - 160, tx + ox + 5, by - 130], fill=K); d.rectangle([tx + ox - 4, by - 159, tx + ox + 4, by - 131], fill=(132, 140, 158))
            d.polygon([(tx + ox - 6, by - 160), (tx + ox + 6, by - 160), (tx + ox, by - 178)], fill=K); d.polygon([(tx + ox - 5, by - 160), (tx + ox + 5, by - 160), (tx + ox, by - 175)], fill=(54, 100, 100))
        d.polygon([(tx - 38, by - 140), (tx + 38, by - 140), (tx + 24, by - 164), (tx - 24, by - 164)], fill=K); d.polygon([(tx - 36, by - 141), (tx + 36, by - 141), (tx + 23, by - 162), (tx - 23, by - 162)], fill=(50, 96, 100))
    box(d, 90, by - 126, 310, by - 112, (112, 120, 138))                       # 高空步道
    for x in range(98, 306, 12): d.rectangle([x, by - 122, x + 6, by - 116], fill=(246, 204, 112))
    for yy in (by - 100, by - 90):                                              # 悬索
        pass
    d.line([(90, by - 112), (160, by - 80), (240, by - 80), (310, by - 112)], fill=(60, 110, 150), width=2)
    return im, w // 2, by


def lab_tower():
    """科学怪人的实验室：哥特石塔 + 玻璃顶 + 避雷针，电光"""
    w, h = 190, 240
    im, d = canvas(w, h); cx = w // 2; by = h - 4
    shadow(d, cx, by, 80, 7)
    box(d, 20, by - 70, w - 20, by, (86, 90, 108))                                    # 厂房
    for x in range(26, w - 26, 6): d.line([(x, by - 66), (x, by - 4)], fill=(70, 74, 92))
    for x in range(34, w - 40, 36):
        d.rectangle([x, by - 56, x + 22, by - 20], fill=K); d.rectangle([x + 2, by - 54, x + 20, by - 22], fill=(120, 200, 255))
        d.line([(x + 11, by - 54), (x + 11, by - 22)], fill=K); d.line([(x + 2, by - 38), (x + 20, by - 38)], fill=K)
    d.polygon([(14, by - 70), (w - 14, by - 70), (w - 40, by - 96), (40, by - 96)], fill=K); d.polygon([(17, by - 71), (w - 17, by - 71), (w - 42, by - 94), (42, by - 94)], fill=SLATE)
    box(d, cx - 32, by - 170, cx + 32, by - 70, (96, 100, 120))                       # 主塔
    for y in range(by - 164, by - 74, 10): d.line([(cx - 31, y), (cx + 31, y)], fill=(80, 84, 104))
    d.rectangle([cx - 10, by - 150, cx + 10, by - 114], fill=K); d.rectangle([cx - 8, by - 148, cx + 8, by - 116], fill=(120, 200, 255)); d.ellipse([cx - 8, by - 154, cx + 8, by - 142], fill=(120, 200, 255))
    d.line([(cx, by - 148), (cx, by - 116)], fill=K)
    d.polygon([(cx - 38, by - 170), (cx + 38, by - 170), (cx + 30, by - 188), (cx - 30, by - 188)], fill=K); d.polygon([(cx - 36, by - 171), (cx + 36, by - 171), (cx + 29, by - 186), (cx - 29, by - 186)], fill=SLATE_L)
    d.ellipse([cx - 22, by - 218, cx + 22, by - 180], fill=K); d.ellipse([cx - 20, by - 216, cx + 20, by - 182], fill=(70, 150, 200)); d.ellipse([cx - 14, by - 210, cx + 6, by - 192], fill=(160, 226, 255))   # 玻璃穹顶
    for x in (cx - 22, cx + 22): d.line([(x, by - 188), (x, by - 226)], fill=K, width=3); d.line([(x, by - 188), (x, by - 226)], fill=(180, 180, 196), width=1); d.ellipse([x - 3, by - 232, x + 3, by - 226], fill=ELEC)
    d.line([(cx - 22, by - 230), (cx - 14, by - 238), (cx - 6, by - 232), (cx + 4, by - 240), (cx + 12, by - 234), (cx + 22, by - 230)], fill=(230, 246, 255), width=1)   # 电弧
    return im, cx, by


def tesla():
    im, d = canvas(30, 62); cx, by = 15, 60
    shadow(d, cx, by, 10, 3)
    box(d, cx - 8, by - 10, cx + 8, by, (70, 74, 92)); d.rectangle([cx - 2, 14, cx + 2, by - 10], fill=K); d.rectangle([cx - 1, 15, cx + 1, by - 11], fill=(150, 150, 166))
    d.ellipse([cx - 9, 4, cx + 9, 20], fill=K); d.ellipse([cx - 8, 5, cx + 8, 19], fill=(130, 140, 160)); d.ellipse([cx - 4, 7, cx + 2, 13], fill=(200, 210, 226))
    d.line([(cx + 8, 10), (cx + 14, 4), (cx + 11, 0)], fill=ELEC); d.line([(cx - 8, 12), (cx - 14, 6)], fill=ELEC)
    return im, cx, by


def mausoleum():
    """哥特地下墓室入口：石殿，尖拱铁门，十字架，门口有石天使"""
    w, h = 130, 140
    im, d = canvas(w, h); cx = w // 2; by = h - 4
    shadow(d, cx, by, 56, 6)
    box(d, 14, by - 72, w - 14, by, (92, 96, 112)); d.rectangle([15, by - 72, w - 15, by - 66], fill=(118, 122, 140))
    for y in range(by - 62, by - 4, 8): d.line([(15, y), (w - 15, y)], fill=(76, 80, 98))
    d.polygon([(8, by - 72), (w - 8, by - 72), (cx, by - 118)], fill=K); d.polygon([(11, by - 73), (w - 11, by - 73), (cx, by - 114)], fill=SLATE)
    d.polygon([(cx - 24, by), (cx - 24, by - 38), (cx, by - 56), (cx + 24, by - 38), (cx + 24, by)], fill=K); d.polygon([(cx - 21, by), (cx - 21, by - 37), (cx, by - 52), (cx + 21, by - 37), (cx + 21, by)], fill=(14, 10, 20))
    for x in range(cx - 18, cx + 20, 6): d.line([(x, by - 2), (x, by - 40)], fill=(60, 64, 76))             # 铁栏
    d.line([(cx - 20, by - 24), (cx + 20, by - 24)], fill=(60, 64, 76)); d.ellipse([cx - 4, by - 16, cx + 4, by - 8], fill=(200, 60, 60))   # 血红封印
    d.rectangle([cx - 2, by - 132, cx + 2, by - 112], fill=K); d.rectangle([cx - 7, by - 128, cx + 7, by - 124], fill=K); d.rectangle([cx - 1, by - 131, cx + 1, by - 113], fill=(190, 190, 204)); d.rectangle([cx - 6, by - 127, cx + 6, by - 125], fill=(190, 190, 204))
    for x in (22, w - 22): d.polygon([(x - 6, by - 74), (x + 6, by - 74), (x, by - 94)], fill=K); d.polygon([(x - 4, by - 74), (x + 4, by - 74), (x, by - 90)], fill=(118, 122, 140))
    return im, cx, by


def angel_statue(var=0):
    im, d = canvas(34, 56); cx, by = 17, 54
    shadow(d, cx, by, 12, 3)
    box(d, cx - 10, by - 8, cx + 10, by, STONE_D); box(d, cx - 7, by - 16, cx + 7, by - 8, STONE)
    d.polygon([(cx - 6, by - 16), (cx + 6, by - 16), (cx + 4, by - 36), (cx - 4, by - 36)], fill=K); d.polygon([(cx - 5, by - 17), (cx + 5, by - 17), (cx + 3, by - 35), (cx - 3, by - 35)], fill=STONE_L)
    d.ellipse([cx - 5, by - 46, cx + 5, by - 35], fill=K); d.ellipse([cx - 4, by - 45, cx + 4, by - 36], fill=STONE_L)
    for s in (-1, 1):
        d.polygon([(cx + s * 3, by - 34), (cx + s * 16, by - 50), (cx + s * 15, by - 28), (cx + s * 3, by - 22)], fill=K); d.polygon([(cx + s * 4, by - 33), (cx + s * 14, by - 47), (cx + s * 13, by - 30), (cx + s * 4, by - 24)], fill=(160, 160, 176))
    if var: d.line([(cx - 5, by - 28), (cx - 5, by - 18)], fill=K)
    return im, cx, by


def cross_grave(var=0):
    im, d = canvas(22, 40); cx, by = 11, 38
    shadow(d, cx, by, 8, 3)
    box(d, cx - 8, by - 5, cx + 8, by, STONE_D)
    d.rectangle([cx - 2, by - 32, cx + 2, by - 5], fill=K); d.rectangle([cx - 1, by - 31, cx + 1, by - 6], fill=STONE); d.rectangle([cx - 7, by - 26, cx + 7, by - 22], fill=K); d.rectangle([cx - 6, by - 25, cx + 6, by - 23], fill=STONE_L)
    if var % 2: d.ellipse([cx - 4, by - 30, cx + 4, by - 22], outline=STONE_L)                    # 凯尔特十字环
    return im, cx, by


def alchemist():
    """炼金术士的店：半木结构、绿光冒泡的窗、挂着烧瓶招牌"""
    w, h = 130, 150
    im, d = canvas(w, h); cx = w // 2; by = h - 3
    shadow(d, cx, by, 56, 5)
    d.rectangle([8, by - 84, w - 8, by], fill=K); d.rectangle([9, by - 83, w - 9, by - 1], fill=(168, 150, 120))
    for x in range(9, w - 8, 22): d.line([(x, by - 83), (x, by - 1)], fill=(64, 44, 40), width=2)
    d.line([(9, by - 44), (w - 9, by - 44)], fill=(64, 44, 40), width=2)
    for i, x in enumerate(range(18, w - 24, 40)):
        d.rectangle([x, by - 76, x + 22, by - 52], fill=K); d.rectangle([x + 1, by - 75, x + 21, by - 53], fill=(70, 240, 150)); d.ellipse([x + 5, by - 70, x + 11, by - 64], fill=(190, 255, 210)); d.ellipse([x + 12, by - 62, x + 16, by - 58], fill=(190, 255, 210))
    box(d, cx - 12, by - 38, cx + 12, by - 1, (30, 22, 30)); d.rectangle([cx - 10, by - 36, cx + 10, by - 2], fill=(70, 240, 150)); d.line([(cx, by - 36), (cx, by - 2)], fill=K)
    for x in (24, w - 36): d.rectangle([x, by - 38, x + 14, by - 10], fill=(40, 30, 40)); d.rectangle([x + 2, by - 36, x + 12, by - 12], fill=(100, 220, 170))
    d.polygon([(2, by - 84), (w - 2, by - 84), (w - 20, by - 124), (20, by - 124)], fill=K); d.polygon([(5, by - 85), (w - 5, by - 85), (w - 21, by - 122), (21, by - 122)], fill=SLATE)
    for x in range(8, w - 6, 5): d.line([(x, by - 85), (x + (cx - x) // 4, by - 122)], fill=SLATE_D)
    d.rectangle([w - 34, by - 140, w - 24, by - 112], fill=K); d.rectangle([w - 33, by - 139, w - 25, by - 113], fill=BRICK_D)
    d.line([(w - 6, by - 60), (w + 0, by - 60)], fill=K)                                                       # 招牌：烧瓶
    d.line([(8, by - 70), (-0, by - 70)], fill=K) if False else None
    d.ellipse([cx - 10, by - 106, cx + 10, by - 90], fill=K); d.ellipse([cx - 8, by - 104, cx + 8, by - 92], fill=(70, 240, 150)); d.rectangle([cx - 3, by - 114, cx + 3, by - 104], fill=K); d.rectangle([cx - 2, by - 113, cx + 2, by - 105], fill=(180, 220, 200))
    return im, cx, by


def manor():
    """黑魔法师的宅邸：黑色哥特老宅、尖顶、血红的窗、倒挂的符号"""
    w, h = 190, 190
    im, d = canvas(w, h); cx = w // 2; by = h - 4
    shadow(d, cx, by, 84, 7)
    box(d, 20, by - 90, w - 20, by, (46, 40, 56))
    for x in range(24, w - 22, 5): d.line([(x, by - 86), (x, by - 4)], fill=(38, 32, 48))
    for x in range(38, w - 40, 34):
        d.rectangle([x, by - 76, x + 14, by - 40], fill=K); d.polygon([(x, by - 76), (x + 14, by - 76), (x + 7, by - 90)], fill=K)
        d.rectangle([x + 1, by - 74, x + 13, by - 42], fill=(220, 50, 56)); d.polygon([(x + 1, by - 75), (x + 13, by - 75), (x + 7, by - 87)], fill=(220, 50, 56)); d.line([(x + 7, by - 86), (x + 7, by - 42)], fill=K)
    box(d, cx - 14, by - 44, cx + 14, by, (24, 18, 30)); d.polygon([(cx - 14, by - 44), (cx + 14, by - 44), (cx, by - 62)], fill=K); d.rectangle([cx - 11, by - 40, cx + 11, by - 2], fill=(90, 20, 40))
    d.polygon([(10, by - 90), (w - 10, by - 90), (w - 36, by - 130), (36, by - 130)], fill=K); d.polygon([(13, by - 91), (w - 13, by - 91), (w - 37, by - 128), (37, by - 128)], fill=(34, 30, 46))
    for x in range(14, w - 10, 6): d.line([(x, by - 91), (x + (cx - x) // 4, by - 128)], fill=(26, 22, 36))
    for tx in (28, w - 28):
        d.rectangle([tx - 12, by - 150, tx + 12, by - 90], fill=K); d.rectangle([tx - 11, by - 149, tx + 11, by - 91], fill=(40, 34, 52))
        d.polygon([(tx - 15, by - 150), (tx + 15, by - 150), (tx, by - 184)], fill=K); d.polygon([(tx - 13, by - 151), (tx + 13, by - 151), (tx, by - 180)], fill=(30, 26, 42))
        d.rectangle([tx - 3, by - 132, tx + 3, by - 116], fill=(220, 50, 56))
    d.polygon([(cx - 22, by - 130), (cx + 22, by - 130), (cx, by - 168)], fill=K); d.polygon([(cx - 20, by - 131), (cx + 20, by - 131), (cx, by - 164)], fill=(40, 34, 52))
    d.line([(cx, by - 164), (cx, by - 184)], fill=K, width=2); d.ellipse([cx - 4, by - 190, cx + 4, by - 182], fill=(220, 50, 56))
    return im, cx, by


def hansom():
    """双轮马车"""
    im, d = canvas(78, 56); cx, by = 39, 54
    shadow(d, cx, by, 28, 4)
    d.ellipse([cx - 20, by - 24, cx + 4, by], outline=K, width=3); d.ellipse([cx - 18, by - 22, cx + 2, by - 2], outline=(150, 120, 80))
    box(d, cx - 14, by - 40, cx + 6, by - 16, (36, 36, 48)); d.polygon([(cx - 16, by - 40), (cx + 8, by - 40), (cx + 2, by - 50), (cx - 10, by - 50)], fill=K); d.polygon([(cx - 14, by - 41), (cx + 6, by - 41), (cx + 1, by - 49), (cx - 9, by - 49)], fill=(30, 30, 40))
    d.rectangle([cx - 10, by - 36, cx + 2, by - 22], fill=(242, 202, 112))
    d.rectangle([cx + 6, by - 20, cx + 34, by - 14], fill=K); d.line([(cx + 6, by - 17), (cx + 34, by - 17)], fill=(150, 120, 80))
    d.rectangle([cx + 22, by - 34, cx + 40, by - 18], fill=K); d.rectangle([cx + 23, by - 33, cx + 39, by - 19], fill=(60, 44, 40))
    d.ellipse([cx + 34, by - 42, cx + 46, by - 30], fill=K); d.ellipse([cx + 35, by - 41, cx + 45, by - 31], fill=(60, 44, 40))
    for x in (cx + 24, cx + 36): d.rectangle([x, by - 18, x + 2, by - 2], fill=K)
    return im, cx, by


def postbox():
    im, d = canvas(16, 34); cx, by = 8, 32
    shadow(d, cx, by, 6, 2)
    box(d, cx - 5, by - 22, cx + 5, by, (190, 40, 44)); d.ellipse([cx - 6, by - 28, cx + 6, by - 20], fill=K); d.ellipse([cx - 5, by - 27, cx + 5, by - 21], fill=(210, 52, 52))
    d.rectangle([cx - 3, by - 16, cx + 3, by - 14], fill=K)
    return im, cx, by


def dead_tree(var=0):
    r = random.Random(var + 17)
    im, d = canvas(70, 90); cx, by = 35, 86
    shadow(d, cx, by, 14, 3)
    d.polygon([(cx - 6, by), (cx - 3, by - 40), (cx + 3, by - 40), (cx + 6, by)], fill=K); d.polygon([(cx - 4, by - 1), (cx - 2, by - 40), (cx + 2, by - 40), (cx + 4, by - 1)], fill=(52, 44, 54))
    def br(x, y, ang, L, depth):
        if depth == 0 or L < 5: return
        ex, ey = x + L * math.cos(ang), y + L * math.sin(ang)
        d.line([(x, y), (ex, ey)], fill=K, width=max(1, depth)); d.line([(x, y), (ex, ey)], fill=(60, 52, 62), width=1)
        br(ex, ey, ang - 0.5 + r.uniform(-0.2, 0.2), L * 0.7, depth - 1); br(ex, ey, ang + 0.5 + r.uniform(-0.2, 0.2), L * 0.7, depth - 1)
    br(cx, by - 38, -math.pi / 2, 22, 4); br(cx, by - 30, -math.pi / 2 - 0.9, 16, 3); br(cx, by - 30, -math.pi / 2 + 0.9, 16, 3)
    return im, cx, by


def yew():
    im, d = canvas(40, 78); cx, by = 20, 74
    shadow(d, cx, by, 12, 3)
    d.polygon([(cx - 15, by), (cx - 10, by - 40), (cx, by - 72), (cx + 10, by - 40), (cx + 15, by)], fill=K)
    d.polygon([(cx - 13, by - 1), (cx - 9, by - 40), (cx, by - 68), (cx + 9, by - 40), (cx + 13, by - 1)], fill=(24, 54, 52))
    d.polygon([(cx - 13, by - 1), (cx - 9, by - 40), (cx, by - 68), (cx - 2, by - 40), (cx - 3, by - 1)], fill=(18, 42, 44))
    return im, cx, by


def factory():
    """河南的砖厂 + 大烟囱"""
    im, d = canvas(130, 160); cx, by = 65, 156
    shadow(d, cx, by, 54, 5)
    box(d, 8, by - 70, 100, by, (92, 56, 54))
    for y in range(by - 66, by - 2, 4): d.line([(9, y), (99, y)], fill=(70, 42, 44))
    for x in range(16, 96, 18): d.rectangle([x, by - 56, x + 10, by - 36], fill=K); d.rectangle([x + 1, by - 55, x + 9, by - 37], fill=(242, 202, 112) if (x // 18) % 2 else (28, 34, 52))
    box(d, 40, by - 22, 66, by, (30, 24, 34))
    d.polygon([(4, by - 70), (104, by - 70), (92, by - 92), (16, by - 92)], fill=K); d.polygon([(7, by - 71), (101, by - 71), (91, by - 90), (17, by - 90)], fill=SLATE)
    d.rectangle([100, by - 150, 122, by], fill=K); d.rectangle([101, by - 149, 121, by - 1], fill=(104, 62, 58))
    for y in range(by - 146, by - 2, 4): d.line([(101, y), (121, y)], fill=(80, 48, 48))
    d.rectangle([98, by - 154, 124, by - 148], fill=(60, 36, 40))
    d.ellipse([92, by - 176, 130, by - 148], fill=(70, 74, 90, 150))
    return im, cx, by


SPRITES = {
    'ln_parl': parliament, 'ln_bridge': tower_bridge, 'ln_lab': lab_tower, 'ln_tesla': tesla, 'ln_maus': mausoleum, 'ln_angel0': lambda: angel_statue(0), 'ln_angel1': lambda: angel_statue(1),
    'ln_cross0': lambda: cross_grave(0), 'ln_cross1': lambda: cross_grave(1), 'ln_alch': alchemist, 'ln_manor': manor, 'ln_cab': hansom, 'ln_post': postbox,
    'ln_dead0': lambda: dead_tree(0), 'ln_dead1': lambda: dead_tree(1), 'ln_yew': yew, 'ln_factory': factory,
    'ln_lamp': Ny.gaslamp, 'ln_crates': Ny.crates, 'ln_barrel': Ny.barrel, 'ln_godown': Ny.godown, 'jp_rock0': lambda: J.rock(0), 'jp_rock1': lambda: J.rock(1),
}
for i in range(6): SPRITES['ln_t%d' % i] = (lambda i=i: terrace(70 + (i % 3) * 10, i, 3 if i % 2 == 0 else 4))


def build(seed=71):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), COBBLE[0] + (255,)); d = ImageDraw.Draw(im)
    blocks = []
    for _ in range(120000): im.putpixel((random.randrange(W), random.randrange(H)), random.choice(COBBLE) + (255,))
    # 鹅卵石纹
    for _ in range(5200):
        x, y = random.randrange(W), random.randrange(H)
        d.arc([x, y, x + 6, y + 4], 0, 180, fill=(44, 50, 66))
    CX = 1100; RY = 830
    # 西侧荒原（狼人）与公园
    for _ in range(60000):
        x, y = random.randrange(0, 700), random.randrange(300, 1000)
        if (x - 330) ** 2 / 360 ** 2 + (y - 640) ** 2 / 330 ** 2 < 1: im.putpixel((x, y), random.choice(GRASS) + (255,))
    # 东侧墓园
    for _ in range(50000):
        x, y = random.randrange(1500, 2200), random.randrange(260, 800)
        if (x - 1850) ** 2 / 330 ** 2 + (y - 540) ** 2 / 270 ** 2 < 1: im.putpixel((x, y), random.choice([(30, 56, 52, 255), (26, 48, 48, 255), (36, 64, 58, 255)]))
    for _ in range(1800):
        x, y = random.randrange(0, 2200), random.randrange(200, 1000)
        for dx, hh in ((0, 2), (1, 4), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 84, 78)) if im.getpixel((x, y))[:3] in GRASS else None
    # 北：远处伦敦天际线
    d.rectangle([0, 0, W, 170], fill=(24, 30, 46))
    for k, col in enumerate([(30, 36, 54), (22, 28, 44)]):
        x = 0
        while x < W:
            bw = random.randint(30, 70); bh = random.randint(20, 70) + (30 if k == 0 else 0)
            d.rectangle([x, 170 - bh, x + bw, 170], fill=col)
            if random.random() < 0.4: d.polygon([(x, 170 - bh), (x + bw, 170 - bh), (x + bw // 2, 170 - bh - 18)], fill=col)
            x += bw
    d.rectangle([0, 168, W, 176], fill=K)
    # 月亮在 preview 里不画（背景是顶视角）
    # 主街与横街（石板）
    def street(x0, y0, x1, y1, w=84):
        d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], fill=(40, 46, 62)); d.rectangle([x0, y0, x1, y1], fill=(78, 84, 100))
        for _ in range(int((x1 - x0) * (y1 - y0) / 40)): im.putpixel((random.randint(x0, x1), random.randint(y0, y1)), random.choice([(70, 76, 92, 255), (88, 94, 110, 255), (64, 70, 86, 255)]))
    street(CX - 42, 380, CX + 42, 1500)
    street(120, RY - 36, 2080, RY + 36)
    d.ellipse([CX - 130, RY - 90, CX + 130, RY + 90], fill=(40, 46, 62)); d.ellipse([CX - 126, RY - 86, CX + 126, RY + 86], fill=(86, 92, 108))
    for a in range(0, 360, 20): d.arc([CX - 100, RY - 66, CX + 100, RY + 66], a, a + 10, fill=(100, 106, 122))
    d.ellipse([CX - 10, RY - 6, CX + 10, RY + 6], fill=(50, 56, 72)); d.ellipse([CX - 4, RY - 3, CX + 4, RY + 3], fill=(120, 126, 142))
    # 国会前广场
    d.rectangle([CX - 220, 380, CX + 220, 440], fill=(70, 76, 94))
    # 泰晤士河
    def tx(y): return 0
    def river_y(x): return 1130 + 36 * math.sin(x / 260) + 14 * math.sin(x / 83)
    RW = 100
    for x in range(W):
        cy = river_y(x)
        d.line([(x, cy - RW // 2 - 6), (x, cy + RW // 2 + 6)], fill=(60, 56, 64)); d.line([(x, cy - RW // 2), (x, cy + RW // 2)], fill=THAMES)
        d.line([(x, cy - RW // 2 - 3), (x, cy - RW // 2)], fill=(90, 84, 90)); d.line([(x, cy + RW // 2), (x, cy + RW // 2 + 3)], fill=(90, 84, 90))
    for _ in range(9000):
        x = random.randrange(W); y = int(river_y(x) + random.randint(-RW // 2, RW // 2)); im.putpixel((x, y), random.choice([THAMES_D, THAMES_L, (36, 66, 92, 255)]))
    for _ in range(200):
        x = random.randrange(W); y = int(river_y(x) + random.randint(-RW // 2 + 6, RW // 2 - 6)); d.line([(x, y), (x + 9, y)], fill=(92, 130, 160))
    BX = CX
    # 塔桥桥面（石板路，横跨河）
    cy = river_y(BX)
    d.rectangle([BX - 44, cy - RW // 2 - 24, BX + 44, cy + RW // 2 + 24], fill=(40, 46, 62)); d.rectangle([BX - 42, cy - RW // 2 - 24, BX + 42, cy + RW // 2 + 24], fill=(84, 90, 106))
    for yy in range(int(cy - RW // 2 - 24), int(cy + RW // 2 + 24), 6): d.line([(BX - 42, yy), (BX + 42, yy)], fill=(72, 78, 94))
    for sx in (BX - 44, BX + 44): d.line([(sx, cy - RW // 2 - 24), (sx, cy + RW // 2 + 24)], fill=(60, 110, 150), width=3)
    # 河南：街与贫民窟小巷
    street(120, 1400, 2080, 1470, 60); street(CX - 42, 1250, CX + 42, 1500)
    # 实验室庭院（西）：铁栅栏 + 石板地
    LX0, LY0, LX1, LY1 = 190, 560, 600, 880
    d.rectangle([LX0, LY0, LX1, LY1], fill=(52, 58, 72))
    for _ in range(9000): im.putpixel((random.randrange(LX0, LX1), random.randrange(LY0, LY1)), random.choice([(46, 52, 68, 255), (58, 64, 80, 255), (50, 58, 74, 255)]))
    for x in range(LX0, LX1 + 1, 12):
        for yy in (LY0, LY1):
            if yy == LY1 and 360 < x < 430: continue
            d.line([(x, yy - 12), (x, yy + 2)], fill=K, width=2); d.point((x, yy - 13), fill=(150, 150, 166))
    for y in range(LY0, LY1 + 1, 12):
        for xx in (LX0, LX1): d.line([(xx - 2, y), (xx + 2, y)], fill=K, width=2)
    d.line([(LX0, LY0 - 4), (LX1, LY0 - 4)], fill=(90, 90, 106)); d.line([(LX0, LY1 - 4), (LX1, LY1 - 4)], fill=(90, 90, 106))
    blocks += [(LX0, LY0 - 6, LX1, LY0 + 2), (LX0 - 2, LY0, LX0 + 3, LY1), (LX1 - 3, LY0, LX1 + 2, LY1), (LX0, LY1 - 6, 360, LY1 + 2), (430, LY1 - 6, LX1, LY1 + 2)]
    d.line([(395, LY1), (395, 930)], fill=(80, 86, 100), width=28) if False else None
    street(CX - 400, RY - 12, 620, RY + 12, 24) if False else None
    # 黑魔法师宅邸前的血色法阵（东南）
    MX, MY = 1720, 1010
    d.ellipse([MX - 90, MY - 56, MX + 90, MY + 56], outline=(180, 30, 40), width=2); d.ellipse([MX - 80, MY - 50, MX + 80, MY + 50], outline=(120, 20, 36), width=1)
    pts = [(MX + 78 * math.cos(math.radians(-90 + i * 72)), MY + 48 * math.sin(math.radians(-90 + i * 72))) for i in range(5)]
    for i in range(5): d.line([pts[i], pts[(i + 2) % 5]], fill=(220, 50, 60), width=2)
    for p in pts: d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(250, 210, 120))
    # 公园小径
    J.road(d, [(CX - 42, RY), (700, RY - 20), (520, 960)], 28, col=(70, 76, 90))
    J.road(d, [(CX + 42, RY), (1500, RY), (1620, 960)], 28, col=(70, 76, 90))
    J.road(d, [(1500, RY), (1650, 640), (1820, 560)], 28, col=(70, 76, 90))
    # 边界
    for x in range(0, W, 20): d.ellipse([x - 12, -10 + random.randint(-4, 4), x + 12, 22], fill=(22, 38, 46)); d.ellipse([x - 12, H - 22 + random.randint(-4, 4), x + 12, H + 10], fill=(22, 38, 46))
    for y in range(0, H, 20): d.ellipse([-6 + random.randint(-4, 4), y - 12, 22, y + 12], fill=(22, 38, 46)); d.ellipse([W - 22 + random.randint(-4, 4), y - 12, W + 6, y + 12], fill=(22, 38, 46))
    blocks += [(0, 0, W, 24), (0, H - 20, W, H), (0, 0, 22, H), (W - 22, 0, W, H)]

    SP = {k: f() for k, f in SPRITES.items()}
    objs = []
    def put(key, x, y, solid=None):
        objs.append(dict(img=key, x=x, y=y))
        if solid: blocks.append((x + solid[0], y + solid[1], x + solid[2], y + solid[3]))
    # 国会与大本钟
    put('ln_parl', CX, 400, (-160, -90, 190, 0))
    for x in (CX - 200, CX + 200): put('ln_lamp', x, 440, (-3, -4, 3, 0))
    # 联排房屋
    def row(x_start, y, specs):
        x = x_start
        for i, w_ in specs:
            key = 'ln_t%d' % i
            if key not in SP: SP[key] = terrace(w_, i, 3 if i % 2 == 0 else 4)
            hh = 3 if i % 2 == 0 else 4
            put(key, x + w_ // 2, y, (-w_ // 2, -(30 * hh + 10), w_ // 2, 0)); x += w_
    row(640, 600, [(0, 70), (1, 80), (2, 90), (3, 70), (4, 80), (5, 90)])
    row(1160, 600, [(5, 90), (4, 80), (3, 70), (2, 90), (1, 80), (0, 70)])
    row(650, 770, [(1, 80), (2, 90), (3, 70), (4, 80), (5, 90)])
    row(1160, 770, [(2, 90), (3, 70), (4, 80), (5, 90), (0, 70)])
    row(560, 1040, [(3, 70), (4, 80), (5, 90), (0, 70)]) if False else None
    # 街灯、邮筒、马车
    for y in (500, 700, 960):
        put('ln_lamp', CX - 52, y, (-3, -4, 3, 0)); put('ln_lamp', CX + 52, y, (-3, -4, 3, 0))
    for x in range(180, 2060, 220):
        if abs(x - CX) < 160: continue
        put('ln_lamp', x, RY + 56, (-3, -4, 3, 0))
    put('ln_post', CX + 96, RY + 70, (-5, -6, 5, 0)); put('ln_post', CX - 96, RY - 50, (-5, -6, 5, 0))
    put('ln_cab', CX + 200, RY + 60, (-24, -14, 24, 0)); put('ln_cab', 840, RY - 50, (-24, -14, 24, 0))
    # 泰晤士河与塔桥
    cyb = river_y(BX)
    put('ln_bridge', BX, cyb + 90, None)
    blocks += [(BX - 190 - 38, cyb - 78, BX - 190 + 38, cyb + 94), (BX + 190 - 38, cyb - 78, BX + 190 + 38, cyb + 94)] if False else []
    # 实验室
    put('ln_lab', 395, 760, (-70, -70, 70, 0)); put('ln_tesla', 260, 840, (-8, -8, 8, 0)); put('ln_tesla', 530, 840, (-8, -8, 8, 0)); put('ln_tesla', 260, 620, (-8, -8, 8, 0)); put('ln_tesla', 530, 620, (-8, -8, 8, 0))
    # 荒原（狼人）：枯树
    for x, y in ((120, 360), (230, 420), (340, 380), (470, 420), (600, 400), (120, 980), (250, 1010), (400, 1000), (560, 1000), (650, 940), (80, 760), (110, 560), (660, 560), (680, 700), (660, 860)): put('ln_dead%d' % (x % 2), x, y, (-5, -6, 5, 0))
    for x, y in ((180, 480), (640, 480), (150, 900), (620, 960)): put('jp_rock%d' % (x % 2), x, y, (-12, -8, 12, 0))
    # 东：哥特墓园
    put('ln_maus', 1900, 440, (-52, -70, 52, 0))
    for x, y in ((1600, 380), (1690, 400), (1780, 320), (2010, 330), (2080, 410), (2050, 520)): put('ln_yew', x, y, (-5, -6, 5, 0))
    graves = []
    for r_ in range(6):
        for c_ in range(10):
            x, y = 1620 + c_ * 46 + (r_ % 2) * 14, 530 + r_ * 48
            if (x - 1850) ** 2 / 340 ** 2 + (y - 570) ** 2 / 270 ** 2 > 1: continue
            if abs(y - 500 - (x - 1650) * 0.0) < 8 and False: continue
            if random.random() < 0.18: continue
            if abs(x - 1900) < 40 and y < 640: continue
            x += random.randint(-5, 5); y += random.randint(-5, 5)
            put('ln_cross%d' % random.randint(0, 1), x, y, (-8, -6, 8, 0)); graves.append([x, y])
            if random.random() < 0.12: put('ln_angel%d' % random.randint(0, 1), x + 18, y + 4, (-9, -6, 9, 0))
    # 东南：炼金术士 + 黑魔法师
    put('ln_alch', 1380, 1000, (-52, -50, 52, 0)); put('ln_manor', 1960, 1100, (-86, -60, 86, 0))
    for x, y in ((1540, 1120), (1820, 1180), (1560, 940), (1900, 940)): put('ln_dead%d' % (x % 2), x, y, (-5, -6, 5, 0))
    # 河南：工厂、仓库、贫民窟
    put('ln_factory', 420, 1380, (-56, -70, 56, 0)); put('ln_factory', 1720, 1380, (-56, -70, 56, 0)); put('ln_godown', 700, 1360, (-52, -46, 52, 0)); put('ln_godown', 1500, 1360, (-52, -46, 52, 0))
    for x, y in ((880, 1330), (960, 1340), (1260, 1330), (1330, 1340), (300, 1290), (2000, 1300)): put('ln_crates', x, y, (-18, -22, 18, 0))
    for x, y in ((850, 1300), (1300, 1300), (330, 1330), (2040, 1340)): put('ln_barrel', x, y, (-8, -10, 8, 0))
    row(180, 1540, [(0, 70), (1, 80), (2, 90)]) if False else None
    for x in range(160, 2060, 220):
        if abs(x - CX) < 160: continue
        put('ln_lamp', x, 1380, (-3, -4, 3, 0))
    for x, y in ((1160, 1280), (1040, 1300)): put('ln_dead%d' % (x % 2), x, y, (-5, -6, 5, 0))

    # ---------------- 通行网格 ----------------
    cols, rows = W // CELL, H // CELL
    grid = [[0] * cols for _ in range(rows)]
    for (x0, y0, x1, y1) in blocks:
        for r_ in range(max(0, y0 // CELL), min(rows, y1 // CELL + 1)):
            for c_ in range(max(0, x0 // CELL), min(cols, x1 // CELL + 1)): grid[r_][c_] = 1
    for c_ in range(cols):                                                       # 泰晤士河：水不可走，桥可走
        x = c_ * CELL + 4; cy = river_y(x)
        for r_ in range(int((cy - RW // 2 - 6) // CELL), int((cy + RW // 2 + 6) // CELL) + 1):
            if r_ >= rows: continue
            if abs(x - BX) < 46: continue
            grid[r_][c_] = 1
    # 塔桥塔楼底座
    cyb = river_y(BX)
    for (a, b, c, e) in ((BX - 190 - 36, cyb - 28, BX - 190 + 36, cyb + 28),):
        pass
    for r_ in range(int((RY - 90) // CELL), int((RY + 90) // CELL)):
        for c_ in range(int((CX - 130) // CELL), int((CX + 130) // CELL)): grid[r_][c_] = 0
    for r_ in range(int(440 // CELL), int(1500 // CELL)):
        for c_ in range(int((CX - 40) // CELL), int((CX + 40) // CELL)):
            if not any(abs(c_ * CELL - o['x']) < 20 and abs(r_ * CELL - o['y']) < 10 for o in objs if o['img'] in ('ln_lamp', 'ln_post')): grid[r_][c_] = 0
    sprites = {k: v[0] for k, v in SP.items()}
    anchors = {k: [v[1], v[2]] for k, v in SP.items()}
    for o in objs: o['ax'], o['ay'] = anchors[o['img']]
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for row in grid for v in row), objs=objs, w=W, h=H,
                start=[CX, RY], boss=[1900, 470], lab=[395, 700], graves=graves)
    return im, sprites, data, SP


def fog(full, seed=5):
    r = random.Random(seed)
    layer = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(layer)
    for _ in range(150):
        x, y = r.randint(0, full.width), r.randint(180, full.height); rx, ry = r.randint(60, 200), r.randint(10, 28)
        g.ellipse([x - rx, y - ry, x + rx, y + ry], fill=(176, 190, 214, r.randint(10, 22)))
    full.alpha_composite(layer)


def preview(path, scale=1.0, crop=None):
    im, sprites, data, SP = build()
    full = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        spr, ax, ay = SP[o['img']]
        full.alpha_composite(spr, (int(o['x'] - ax), int(o['y'] - ay)))
    glow = Image.new('RGBA', full.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for o in data['objs']:
        if o['img'] == 'ln_lamp':
            for k, rr in enumerate((36, 24, 12)): g.ellipse([o['x'] - rr, o['y'] - 46 - rr * 0.8, o['x'] + rr, o['y'] - 46 + rr * 0.8], fill=(255, 214, 120, 14 + k * 8))
        if o['img'] == 'ln_lab':
            for k, rr in enumerate((100, 60, 30)): g.ellipse([o['x'] - rr, o['y'] - 180 - rr * 0.6, o['x'] + rr, o['y'] - 180 + rr * 0.6], fill=(120, 200, 255, 14 + k * 8))
        if o['img'] == 'ln_alch': g.ellipse([o['x'] - 70, o['y'] - 70, o['x'] + 70, o['y'] + 10], fill=(70, 240, 150, 22))
        if o['img'] == 'ln_manor': g.ellipse([o['x'] - 100, o['y'] - 110, o['x'] + 100, o['y'] + 10], fill=(220, 50, 56, 18))
        if o['img'] == 'ln_parl': g.ellipse([o['x'] - 220, o['y'] - 140, o['x'] + 180, o['y']], fill=(246, 204, 112, 14))
    full.alpha_composite(glow)
    fog(full)
    if crop: full = full.crop(crop)
    if scale != 1: full = full.resize((int(full.width * scale), int(full.height * scale)), Image.NEAREST)
    full.convert('RGB').save(path)


if __name__ == '__main__':
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else 'ln_preview.png', 0.45)
