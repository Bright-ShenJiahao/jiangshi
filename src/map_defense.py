"""守卫龙脉（防守地图）：竖版地图。
最上方鬼门关三路出怪，中间一条河、三座桥，河两岸四个野外点（古墓 / 洋人教堂 / 乱葬岗 / 义庄），
最下方是任家镇：城墙上开三道门（西门、正门牌坊、东门），三路各进一道门，在镇中心的龙脉汇合。
复用 map_gen5 里的房子、牌坊、酒楼、教堂、树、芭蕉的像素图。"""
import random, math
from PIL import Image, ImageDraw
import map_gen5 as M

W, H = 960, 1640
CELL = 8
K = M.K
font = M.font

PORTALS = [(170, 70), (480, 70), (790, 70)]
RIVER_Y, RIVER_W = 600, 34
BRIDGES = [150, 480, 810]
WALL = (1166, 1192)                # 城墙上下沿
GATES = [(128, 176), (452, 508), (784, 832)]   # 西门、正门、东门
CORE = (480, 1490)                 # 龙脉
LANES = [
    [(170, 92), (150, 250), (140, 420), (150, 600), (150, 800), (152, 1000), (152, 1150), (152, 1214), (152, 1326), (300, 1346), (400, 1420), (466, 1470), CORE],
    [(480, 92), (480, 300), (480, 600), (480, 900), (480, 1150), (480, 1214), (480, 1340), CORE],
    [(790, 92), (810, 250), (820, 420), (810, 600), (810, 800), (808, 1000), (808, 1150), (808, 1214), (808, 1326), (660, 1346), (560, 1420), (494, 1470), CORE],
]
FIELDS = {   # 野外点：名字、中心、野外 BOSS 的家
    'tomb': dict(name='蜻蜓点水穴', c=(310, 400), home=(310, 446)),
    'church': dict(name='洋人教堂', c=(665, 520), home=(665, 556)),
    'grave': dict(name='乱葬岗', c=(340, 820), home=(340, 836)),
    'yz': dict(name='义庄', c=(620, 820), home=(626, 862)),
}


def longmai_img():
    """龙脉：八卦石台上立一块石碑，碑上刻「龙脉」，两侧一对盘龙石柱"""
    im = Image.new('RGBA', (96, 84), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, by = 48, 80
    # 石台（两层）
    d.ellipse([cx - 40, by - 18, cx + 40, by + 2], fill=K); d.ellipse([cx - 39, by - 17, cx + 39, by + 1], fill=(112, 106, 120))
    d.ellipse([cx - 30, by - 22, cx + 30, by - 6], fill=K); d.ellipse([cx - 29, by - 21, cx + 29, by - 7], fill=(150, 144, 158))
    for a in range(8):
        an = a * math.pi / 4; x, y = cx + math.cos(an) * 34, by - 8 + math.sin(an) * 7
        d.rectangle([x - 2, y - 1, x + 2, y + 1], fill=(70, 64, 80))
    # 盘龙石柱
    for sx in (cx - 30, cx + 30):
        d.rectangle([sx - 4, by - 52, sx + 4, by - 12], fill=K); d.rectangle([sx - 3, by - 51, sx + 3, by - 13], fill=(140, 136, 150))
        d.rectangle([sx + 1, by - 51, sx + 3, by - 13], fill=(110, 106, 122))
        for k in range(5):     # 绕柱的龙身
            y = by - 48 + k * 8; d.line([(sx - 4, y), (sx + 4, y + 4)], fill=(60, 140, 100), width=2)
        d.rectangle([sx - 6, by - 58, sx + 6, by - 51], fill=K); d.rectangle([sx - 5, by - 57, sx + 5, by - 52], fill=(70, 160, 112))
        d.point((sx - 2 if sx < cx else sx + 2, by - 55), fill=(250, 220, 90))
    # 石碑
    d.rectangle([cx - 13, by - 64, cx + 13, by - 14], fill=K); d.rectangle([cx - 12, by - 63, cx + 12, by - 15], fill=(176, 172, 186))
    d.rectangle([cx + 7, by - 63, cx + 12, by - 15], fill=(140, 136, 152))
    d.pieslice([cx - 15, by - 74, cx + 15, by - 56], 180, 360, fill=K); d.pieslice([cx - 14, by - 73, cx + 14, by - 57], 180, 360, fill=(160, 156, 172))
    d.rectangle([cx - 8, by - 56, cx + 6, by - 20], fill=(150, 146, 162))
    d.text((cx - 1, by - 48), '龍', font=font(11), fill=(40, 110, 76), anchor='mm')
    d.text((cx - 1, by - 32), '脈', font=font(11), fill=(40, 110, 76), anchor='mm')
    return im, cx, by


def guimen_img():
    """鬼门关：两根黑柱，挂白灯笼，横匾「鬼门关」"""
    im = Image.new('RGBA', (120, 74), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for x in (18, 102):
        d.rectangle([x - 6, 14, x + 6, 72], fill=K); d.rectangle([x - 5, 15, x + 5, 72], fill=(44, 36, 52)); d.rectangle([x - 5, 15, x - 3, 72], fill=(62, 52, 72))
        d.line([(x, 30), (x, 36)], fill=K); d.rectangle([x - 4, 36, x + 4, 46], fill=K); d.rectangle([x - 3, 37, x + 3, 45], fill=(232, 232, 220)); d.line([(x, 37), (x, 45)], fill=(40, 40, 40))
    d.polygon([(2, 16), (118, 16), (108, 2), (12, 2)], fill=K); d.polygon([(5, 14), (115, 14), (106, 4), (14, 4)], fill=(34, 26, 40))
    d.rectangle([34, 16, 86, 32], fill=K); d.rectangle([35, 17, 85, 31], fill=(20, 12, 20))
    d.text((60, 24), '鬼门关', font=font(11), fill=(220, 50, 44), anchor='mm')
    return im, 60, 72


def build(seed=7):
    random.seed(seed)
    im = Image.new('RGBA', (W, H), (58, 42, 80, 255)); d = ImageDraw.Draw(im)
    blocks, objs = [], []
    sprites = {'tree': M.tree_img(), 'treeB': M.tree_img(True)}
    def block(x0, y0, x1, y1): blocks.append((x0, y0, x1, y1))

    for _ in range(30000):
        im.putpixel((random.randrange(W), random.randrange(H)), random.choice([(70, 52, 96, 255), (46, 33, 64, 255), (64, 48, 88, 255)]))
    for _ in range(500):
        x, y = random.randrange(W), random.randrange(H)
        for dx, hh in ((0, 2), (1, 3), (2, 2)): d.line([(x + dx, y), (x + dx, y - hh)], fill=(52, 86, 84))

    # ---------- 阴气：越往上越暗、越紫 ----------
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for y in range(0, 520):
        a = int(70 * (1 - y / 520) ** 1.6); sd.line([(0, y), (W, y)], fill=(30, 6, 30, a))
    im.alpha_composite(sh)

    def road(pts, w=30, col=(98, 80, 94)):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 3) + 1
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                d.ellipse([x - w / 2, y - w / 2.6, x + w / 2, y + w / 2.6], fill=col)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 6) + 1
            for i in range(n):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                for c, p in (((120, 100, 112, 255), 0.6), ((78, 62, 80, 255), 0.3)):
                    if random.random() < p:
                        px_, py_ = int(x + random.randint(-9, 9)), int(y + random.randint(-6, 6))
                        if 0 <= px_ < W and 0 <= py_ < H: im.putpixel((px_, py_), c)
    for L in LANES: road([p for p in L if p[1] <= 1190], 30)

    def near_lane(x, y, r):
        for L in LANES:
            for (x0, y0), (x1, y1) in zip(L, L[1:]):
                L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2 or 1; t = max(0, min(1, ((x - x0) * (x1 - x0) + (y - y0) * (y1 - y0)) / L2))
                if (x - (x0 + (x1 - x0) * t)) ** 2 + (y - (y0 + (y1 - y0) * t)) ** 2 < r * r: return True
        return False

    # ---------- 河 + 三座桥 ----------
    def ry(x): return RIVER_Y + 7 * math.sin(x / 61) + 4 * math.sin(x / 23)
    for x in range(W):
        c = ry(x)
        d.line([(x, c - RIVER_W / 2 - 4), (x, c + RIVER_W / 2 + 4)], fill=(40, 34, 52))
        d.line([(x, c - RIVER_W / 2), (x, c + RIVER_W / 2)], fill=(30, 46, 84))
        if x % 3 == 0:
            y = c + random.uniform(-RIVER_W / 2 + 3, RIVER_W / 2 - 3); d.line([(x, y), (x + random.randint(3, 7), y)], fill=(60, 92, 140))
        if x % 8 == 0 and not any(abs(x + 4 - bx) < 26 for bx in BRIDGES):
            block(x, int(c - RIVER_W / 2 - 3), x + 8, int(c + RIVER_W / 2 + 3))
    for bx in BRIDGES:
        x0, x1 = bx - 24, bx + 24; y0, y1 = int(ry(bx) - RIVER_W / 2 - 14), int(ry(bx) + RIVER_W / 2 + 14)
        d.rectangle([x0 - 2, y0, x1 + 2, y1], fill=K); d.rectangle([x0, y0 + 1, x1, y1 - 1], fill=(132, 126, 150))
        for y in range(y0 + 4, y1 - 2, 8): d.line([(x0 + 3, y), (x1 - 3, y)], fill=(110, 104, 130))
        for xx in (x0 - 2, x1 - 2):
            d.rectangle([xx, y0, xx + 4, y1], fill=K); d.rectangle([xx + 1, y0 + 1, xx + 3, y1 - 1], fill=(170, 164, 186))
            for y in range(y0 + 2, y1, 12): d.rectangle([xx - 1, y, xx + 5, y + 3], fill=K); d.rectangle([xx, y + 1, xx + 4, y + 2], fill=(190, 184, 204))
        block(x0 - 4, y0, x0 + 2, y1); block(x1 - 2, y0, x1 + 4, y1)

    # ---------- 鬼门关（三处地裂） ----------
    for i, (px, py) in enumerate(PORTALS):
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        for r in range(60, 6, -4): gd.ellipse([px - r, py - r * 0.5, px + r, py + r * 0.5], fill=(200, 30, 60, 10))
        im.alpha_composite(glow)
        d.ellipse([px - 34, py - 10, px + 34, py + 12], fill=(30, 10, 22)); d.ellipse([px - 28, py - 7, px + 28, py + 8], fill=(14, 4, 12))
        for k in range(9):
            an = random.uniform(0, 6.28); r0, r1 = 20, random.randint(34, 52)
            d.line([(px + math.cos(an) * r0, py + math.sin(an) * r0 * 0.45), (px + math.cos(an) * r1, py + math.sin(an) * r1 * 0.45)], fill=(120, 20, 40), width=2)
        d.ellipse([px - 16, py - 4, px + 16, py + 5], fill=(170, 30, 50)); d.ellipse([px - 9, py - 2, px + 9, py + 3], fill=(255, 90, 90))
        if i != 1:
            for sx in (px - 40, px + 40):
                d.rectangle([sx - 3, py - 26, sx + 3, py + 4], fill=K); d.rectangle([sx - 2, py - 25, sx + 2, py + 4], fill=(70, 60, 76))
                d.rectangle([sx - 4, py - 22, sx + 4, py - 12], fill=K); d.rectangle([sx - 3, py - 21, sx + 3, py - 13], fill=(232, 232, 220))
                block(sx - 3, py, sx + 3, py + 4)
    gimg, gax, gay = guimen_img(); sprites['guimen'] = gimg
    objs.append(dict(k='house', x=480, y=96, img='guimen', ax=gax, ay=gay)); block(480 - 48, 90, 480 - 36, 97); block(480 + 36, 90, 480 + 48, 97)

    # ---------- 上边界：荒山 ----------
    for layer, col in enumerate(((34, 30, 50), (46, 40, 64))):
        pts = [(0, 0)]
        for x in range(0, W + 14, 14): pts.append((x, 30 + 10 * math.sin(x / 47 + layer) + 6 * math.sin(x / 13) - layer * 8))
        pts += [(W, 0)]
        d.polygon(pts, fill=K); d.polygon([(a, b - 2) for a, b in pts], fill=col)
    block(0, 0, W, 34)

    # ---------- 背景树 ----------
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
        """蜻蜓点水穴：长坟包，中间窄竖坑，坑口盖着石灰，三脚架、无字碑"""
        d.ellipse([x - 62, y - 22, x + 62, y + 24], fill=(70, 52, 60)); d.ellipse([x - 54, y - 18, x + 50, y + 14], fill=(88, 66, 74))
        for dx, dy in ((-44, 6), (40, 8), (-30, -12), (36, -8)): d.ellipse([x + dx - 9, y + dy - 5, x + dx + 9, y + dy + 4], fill=(150, 120, 60)); d.ellipse([x + dx - 6, y + dy - 4, x + dx + 4, y + dy + 1], fill=(176, 144, 76))
        d.ellipse([x - 26, y - 12, x + 26, y + 14], fill=(206, 206, 200)); d.ellipse([x - 22, y - 9, x + 20, y + 10], fill=(226, 226, 220))
        for a, b in (((-18, -4), (-6, 2)), ((8, -8), (18, 4)), ((-10, 8), (4, 4))): d.line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], fill=(160, 158, 156))
        d.rectangle([x - 6, y - 7, x + 6, y + 8], fill=K); d.rectangle([x - 5, y - 6, x + 5, y + 7], fill=(18, 10, 16))
        top = (x, y - 46)
        for fx, fy in ((x - 22, y + 10), (x + 22, y + 10), (x + 2, y - 14)): d.line([top, (fx, fy)], fill=K, width=3); d.line([top, (fx, fy)], fill=(110, 72, 40), width=1)
        d.line([(x, y - 43), (x, y - 2)], fill=(200, 180, 130))
        tx, ty = x + 40, y - 10
        d.rectangle([tx - 7, ty - 18, tx + 7, ty], fill=K); d.rectangle([tx - 6, ty - 17, tx + 6, ty - 1], fill=(146, 140, 166)); d.rectangle([tx + 3, ty - 17, tx + 6, ty - 1], fill=(110, 104, 132))
        block(tx - 8, ty - 4, tx + 8, ty + 1); block(x - 6, y - 4, x + 6, y + 6)

    items = []   # (k, x, y)：按 y 排序后画进背景
    # 古墓
    tc = FIELDS['tomb']['c']; items.append(('tomb', tc[0], tc[1]))
    for (x, y) in ((230, 340), (390, 330), (400, 470), (225, 470)): items.append(('dd', x, y))
    for (x, y) in ((250, 300), (372, 296), (260, 500), (370, 506)): items.append(('g', x, y))
    # 教堂：十字架坟
    for (x, y) in ((592, 560), (614, 590), (720, 562), (740, 592), (598, 330), (736, 330)): items.append(('x', x, y))
    # 乱葬岗
    gc = FIELDS['grave']['c']; graves, coffins = [], []
    mg = Image.new('RGBA', (W, H), (0, 0, 0, 0)); md = ImageDraw.Draw(mg)
    for _ in range(20):
        x, y = gc[0] + random.randint(-70, 70), gc[1] + random.randint(-90, 90); r = random.randint(24, 56)
        md.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(18, 8, 22, 26))
    im.alpha_composite(mg)
    for _ in range(4000):
        if len(graves) >= 11: break
        x, y = gc[0] + random.randint(-75, 75), gc[1] + random.randint(-110, 100)
        if near_lane(x, y, 34) or (x - gc[0]) ** 2 + (y - FIELDS['grave']['home'][1]) ** 2 < 34 ** 2: continue
        if all((x - a) ** 2 + (y - b) ** 2 > 34 ** 2 for a, b in graves): graves.append((x, y))
    for (x, y) in graves: items.append(('g', x, y))
    for _ in range(3000):
        if len(coffins) >= 4: break
        x, y = gc[0] + random.randint(-70, 70), gc[1] + random.randint(-80, 90)
        if near_lane(x, y, 38) or (x - gc[0]) ** 2 + (y - FIELDS['grave']['home'][1]) ** 2 < 40 ** 2: continue
        if all((x - a) ** 2 + (y - b) ** 2 > 36 ** 2 for a, b in graves + coffins): coffins.append((x, y))
    for (x, y) in coffins: items.append(('c', x, y))
    for k in range(7): items.append(('f', gc[0] + random.randint(-80, 80), gc[1] + random.randint(-110, 100)))
    for _ in range(50):
        x, y = gc[0] + random.randint(-85, 85), gc[1] + random.randint(-110, 110)
        d.line([(x, y), (x + random.choice([-4, 4]), y + random.choice([-2, 2]))], fill=(220, 214, 200))
    # 义庄门口的棺材
    for (x, y, o) in ((574, 900, 0), (676, 904, 1), (610, 930, 1), (650, 934, 0)): items.append(('c2', x, y, o))
    # 地图左右边界的树林
    for y in range(40, 1160, 24):
        items.append(('td', 12 + random.randint(-4, 4), y)); items.append(('td', W - 12 + random.randint(-4, 4), y))
    block(0, 0, 24, H); block(W - 24, 0, W, H)
    # 枯树散落
    for _ in range(200):
        x, y = random.randrange(40, W - 40), random.randrange(130, 1140)
        if near_lane(x, y, 34) or abs(y - RIVER_Y) < 40: continue
        if any((x - f['c'][0]) ** 2 + (y - f['c'][1]) ** 2 < 120 ** 2 for f in FIELDS.values()): continue
        if sum(1 for it in items if it[0] == 'dd') > 26: break
        if all((x - it[1]) ** 2 + (y - it[2]) ** 2 > 40 ** 2 for it in items): items.append(('dd', x, y))

    for it in sorted(items, key=lambda t: t[2]):
        k, x, y = it[0], it[1], it[2]
        if k == 'td': bgtree(x, y)
        elif k == 'dd': bgtree(x, y, True)
        elif k == 'g': r = random.random(); grave(x, y, r < 0.25, 0.25 <= r < 0.45)
        elif k == 'c': coffin(x, y, random.random() < 0.4)
        elif k == 'c2': coffin(x, y, bool(it[3]))
        elif k == 'f': flag(x, y)
        elif k == 'x': cross(x, y, (x * 7 + y) % 3 - 1)
        elif k == 'tomb': grandpa(x, y)

    # 树（物件，会挡人、能被烧）
    trees = []
    for _ in range(6000):
        if len(trees) >= 46: break
        x, y = random.randrange(40, W - 40), random.randrange(130, 1150)
        if near_lane(x, y, 36) or abs(y - RIVER_Y) < 36: continue
        if any((x - f['c'][0]) ** 2 + (y - f['c'][1]) ** 2 < 125 ** 2 for f in FIELDS.values()): continue
        if any((x - a) ** 2 + (y - b) ** 2 < 70 ** 2 for a, b in PORTALS): continue
        if all((x - a) ** 2 + (y - b) ** 2 > 40 ** 2 for a, b in trees): trees.append((x, y))
    for x, y in trees: objs.append(dict(k='tree', x=x, y=y, img='tree', ax=15, ay=46)); block(x - 3, y - 4, x + 3, y + 1)

    # 洋人教堂（物件）
    cimg, cax, cay = M.church_img(); sprites['church'] = cimg
    cx, cy = FIELDS['church']['c']
    objs.append(dict(k='church', x=cx, y=cy, img='church', ax=cax, ay=cay, rect=[cx - 60, cy - 110, cx + 60, cy + 20], burn=False))
    block(cx - 58, cy - 104, cx + 58, cy - 2)
    # 义庄（物件）
    hn = [0]
    def house(x0, y0, w, h, plaque=None, lan=False, lc=(236, 236, 226)):
        img, ax, ay = M.house_img(w, h, plaque, lan, lc=lc); key = f'dh{hn[0]}'; hn[0] += 1; sprites[key] = img
        objs.append(dict(k='house', x=x0 + w // 2, y=y0 + 18 + h, img=key, ax=ax + w // 2, ay=ay, rect=[x0, y0, x0 + w, y0 + 18 + h], burn=False))
        block(x0 - 2, y0 + 10, x0 + w + 2, y0 + 18 + h)
    yc = FIELDS['yz']['c']; house(yc[0] - 60, yc[1] - 40, 120, 44, '义庄', True)

    # ---------- 城墙 + 三道门 ----------
    y0, y1 = WALL
    segs, x = [], 0
    for g0, g1 in GATES: segs.append((x, g0)); x = g1
    segs.append((x, W))
    for (a, b) in segs:
        d.rectangle([a, y0 - 2, b, y1 + 2], fill=K)
        d.rectangle([a + 1, y0, b - 1, y0 + 9], fill=(126, 120, 132))           # 墙顶走道
        d.rectangle([a + 1, y0 + 10, b - 1, y1], fill=(98, 92, 106))           # 墙面
        for x in range(a + 2, b - 4, 12):                                        # 垛口
            d.rectangle([x, y0 - 6, x + 6, y0], fill=K); d.rectangle([x + 1, y0 - 5, x + 5, y0], fill=(150, 144, 158))
        for yy in (y0 + 14, y0 + 20): d.line([(a + 1, yy), (b - 1, yy)], fill=(80, 74, 88))
        for x in range(a + 6, b - 2, 14): d.line([(x, y0 + 10), (x, y0 + 14)], fill=(80, 74, 88)); d.line([(x + 7, y0 + 14), (x + 7, y0 + 20)], fill=(80, 74, 88))
        block(a, y0 - 6, b, y1 + 2)
    pimg, pax, pay = M.paifang_img(); sprites['paifang'] = pimg
    objs.append(dict(k='house', x=480, y=y1 + 4, img='paifang', ax=pax, ay=pay, rect=[428, y1 - 80, 532, y1 + 4], burn=False))
    block(438, y1 - 8, 452, y1 + 5); block(508, y1 - 8, 522, y1 + 5)
    for (g0, g1), nm in ((GATES[0], '西门'), (GATES[2], '东门')):
        gi = Image.new('RGBA', (76, 64), (0, 0, 0, 0)); gd = ImageDraw.Draw(gi)
        for px_ in (6, 70):
            gd.rectangle([px_ - 5, 16, px_ + 5, 63], fill=K); gd.rectangle([px_ - 4, 17, px_ + 4, 63], fill=(150, 46, 40)); gd.rectangle([px_ - 4, 17, px_ - 2, 63], fill=(110, 30, 28))
        gd.polygon([(0, 18), (76, 18), (68, 6), (8, 6)], fill=K); gd.polygon([(3, 16), (73, 16), (66, 8), (10, 8)], fill=(52, 50, 72))
        gd.rectangle([22, 17, 54, 30], fill=K); gd.rectangle([23, 18, 53, 29], fill=(30, 26, 36)); gd.text((38, 24), nm, font=font(10), fill=(240, 200, 90), anchor='mm')
        key = 'gate' + nm; sprites[key] = gi; cx = (g0 + g1) // 2
        objs.append(dict(k='house', x=cx, y=y1 + 4, img=key, ax=38, ay=63, rect=[cx - 38, y1 - 60, cx + 38, y1 + 4], burn=False))
        block(g0 - 10, y1 - 8, g0, y1 + 5); block(g1, y1 - 8, g1 + 10, y1 + 5)

    # ---------- 任家镇 ----------
    for L in LANES: road([p for p in L if p[1] >= 1150], 34)
    road([(130, 1340), (830, 1340)], 26)
    # 龙脉广场 + 一路通到地图最下方的龙脉金线
    d.ellipse([CORE[0] - 78, CORE[1] - 46, CORE[0] + 78, CORE[1] + 40], fill=K)
    d.ellipse([CORE[0] - 76, CORE[1] - 44, CORE[0] + 76, CORE[1] + 38], fill=(104, 96, 110))
    for r in (66, 50):
        d.ellipse([CORE[0] - r, CORE[1] - r * 0.58 - 3, CORE[0] + r, CORE[1] + r * 0.58 - 3], outline=(86, 80, 94))
    for a in range(16):
        an = a * math.pi / 8; d.line([(CORE[0] + math.cos(an) * 50, CORE[1] - 3 + math.sin(an) * 29), (CORE[0] + math.cos(an) * 66, CORE[1] - 3 + math.sin(an) * 38)], fill=(86, 80, 94))
    vx, vy = CORE[0], CORE[1] + 36
    vein = [(vx, vy)]
    while vy < H:
        vx += random.randint(-10, 10); vy += random.randint(10, 18); vein.append((vx, vy))
    d.line(vein, fill=(20, 60, 44), width=6); d.line(vein, fill=(70, 200, 130), width=2)
    for (x, y) in vein[1:-1]:
        if random.random() < 0.5: d.line([(x, y), (x + random.choice([-1, 1]) * random.randint(8, 16), y + random.randint(2, 8))], fill=(50, 150, 100), width=1)
    limg, lax, lay = longmai_img(); sprites['longmai'] = limg
    objs.append(dict(k='house', x=CORE[0], y=CORE[1] + 2, img='longmai', ax=lax, ay=lay, rect=[CORE[0] - 40, CORE[1] - 70, CORE[0] + 40, CORE[1] + 4], burn=False))
    block(CORE[0] - 14, CORE[1] - 8, CORE[0] + 14, CORE[1] + 2)
    # 房子：避开三条进镇的路
    house(196, 1212, 120, 48, '任府', True, (220, 60, 50))
    house(330, 1226, 96, 40, '衙门', True, (220, 60, 50))
    timg, tax, tay = M.teahouse_img(); sprites['tea'] = timg
    objs.append(dict(k='house', x=588, y=1306, img='tea', ax=tax, ay=tay, rect=[532, 1160, 644, 1306], burn=False)); block(542, 1256, 636, 1306)
    house(660, 1230, 100, 40, '棺材铺')
    house(36, 1396, 120, 44, '杂货铺', True, (240, 200, 90))
    house(186, 1430, 92, 38, '祠堂', True, (220, 60, 50))
    house(690, 1430, 90, 38, '米铺')
    house(806, 1396, 110, 44)
    d.ellipse([40, 1250, 64, 1264], fill=K); d.ellipse([42, 1251, 62, 1262], fill=(110, 108, 124)); d.ellipse([46, 1253, 58, 1260], fill=(20, 30, 50)); block(40, 1252, 64, 1264)   # 水井
    for (x, y) in ((440, 1262), (520, 1262), (420, 1440), (540, 1440)):
        d.line([(x, y), (x, y - 22)], fill=K, width=2); d.rectangle([x - 4, y - 30, x + 4, y - 20], fill=K); d.rectangle([x - 3, y - 29, x + 3, y - 21], fill=(220, 60, 50)); block(x - 2, y - 3, x + 2, y + 1)
    # 下边界：竹林
    for x in range(10, W, 22):
        if abs(x - CORE[0]) < 40: continue
        bgtree(x + random.randint(-3, 3), H - 6 - random.randint(0, 8))
    block(0, H - 24, W, H)
    # 芭蕉（镇外，西路和正路之间）
    PL = []
    for v in range(3): sprites['plant%d' % v] = M.plant_img(v)
    for _ in range(3000):
        if len(PL) >= 16: break
        x, y = random.randrange(220, 420), random.randrange(1000, 1150)
        if near_lane(x, y, 30): continue
        if all((x - a) ** 2 + (y - b) ** 2 > 26 ** 2 for a, b in PL): PL.append((x, y))
    for k2, (x, y) in enumerate(PL): objs.append(dict(k='plant', x=x, y=y, img='plant%d' % (k2 % 3), ax=28, ay=48)); block(x - 3, y - 3, x + 3, y + 1)
    for x, y in [(x, 1150) for x in range(540, 940, 30)] + [(x, 1150) for x in range(30, 130, 30)]:
        if not near_lane(x, y, 30): objs.append(dict(k='tree', x=x, y=y, img='tree', ax=15, ay=46)); block(x - 3, y - 4, x + 3, y + 1)

    # 雾
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
    for _ in range(70):
        x, y = random.randrange(-60, W), random.randrange(0, 1160); fd.ellipse([x, y, x + 170, y + 16], fill=(170, 160, 210, 20))
    im.alpha_composite(fog)

    cols, rows = W // CELL, H // CELL
    grid = bytearray(cols * rows)
    for x0, y0, x1, y1 in blocks:
        for cy in range(max(0, int(y0) // CELL), min(rows - 1, int(y1) // CELL) + 1):
            for cx in range(max(0, int(x0) // CELL), min(cols - 1, int(x1) // CELL) + 1):
                grid[cy * cols + cx] = 1
    # 路上一定走得通：沿路把格子清空（树、坟不会挡在路上，这里只是保险）
    for L in LANES:
        for (x0, y0), (x1, y1) in zip(L, L[1:]):
            n = int(math.hypot(x1 - x0, y1 - y0) / 4) + 1
            for i in range(n + 1):
                x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
                if (x - CORE[0]) ** 2 + (y - CORE[1]) ** 2 < 20 ** 2: continue
                for dx in (-8, 0, 8):
                    cx, cy = int(x + dx) // CELL, int(y) // CELL
                    if 0 <= cx < cols and 0 <= cy < rows: grid[cy * cols + cx] = 0
    data = dict(cols=cols, rows=rows, cell=CELL, grid=''.join('1' if v else '0' for v in grid), objs=objs, w=W, h=H,
                lanes=LANES, portals=PORTALS, core=list(CORE), gate=[480, WALL[1]], wall=list(WALL), riverY=RIVER_Y,
                fields={k: dict(name=v['name'], c=list(v['c']), home=list(v['home'])) for k, v in FIELDS.items()},
                townY=WALL[1] + 4, shop=[96, 1466], guards=[[452, 1226], [512, 1226], [184, 1226], [776, 1226]], guardsX=[[110, 1300], [850, 1300], [430, 1420], [530, 1420]],
                simu=[480, 1408], watch=[540, 1240], gates=[(a + b) // 2 for a, b in GATES])
    return im, sprites, data


if __name__ == '__main__':
    im, sprites, data = build()
    out = im.copy()
    for o in sorted(data['objs'], key=lambda o: o['y']):
        s = sprites[o['img']]; out.alpha_composite(s, (o['x'] - o['ax'], o['y'] - o['ay']))
    import sys
    out.convert('RGB').save(sys.argv[1] if len(sys.argv) > 1 else 'map_defense.png'); print(len(data['objs']))
