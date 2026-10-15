# 新怪物像素图（紫/白/绿僵、女尸、半腐骷髅、尸煞）；文件末尾是示意图拼图
# 示意图：紫/白/绿僵进化线、行尸新外形、尸王第二阶段「不化骨」
from PIL import Image, ImageDraw, ImageFont
import random

g = {}
exec(open('sprites.py').read().split('\nsheet()')[0], g)
wg = {}
exec(open('walker.py').read().split('\nif __name__')[0], wg)
PAL = g['PAL']; K = (24, 14, 30)


def recolor(im, mp):
    out = im.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, gg, b, a = px[x, y]
            if a and (r, gg, b) in mp: px[x, y] = mp[(r, gg, b)] + (a,)
    return out


def pad(im, p=3):
    out = Image.new('RGBA', (im.width + 2 * p, im.height + 2 * p), (0, 0, 0, 0)); out.paste(im, (p, p), im); return out


def fuzz(im, cols, prob, seed=1, body=30):
    random.seed(seed); out = pad(im, 2); src = out.copy(); sp, op = src.load(), out.load(); W, H = out.size
    for y in range(H - 5):
        for x in range(W):
            if sp[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and sp[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and random.random() < prob:
                op[x, y] = random.choice(cols) + (255,)
    for _ in range(body):
        x, y = random.randrange(W), random.randrange(H - 6)
        if sp[x, y][3] and sp[x, y][:3] != K: op[x, y] = random.choice(cols) + (255,)
    return out


def outline(im):
    out = im.copy(); sp, op = im.load(), out.load(); W, H = im.size
    for y in range(H):
        for x in range(W):
            if sp[x, y][3]: continue
            if any(0 <= x + dx < W and 0 <= y + dy < H and sp[x + dx, y + dy][3] and sp[x + dx, y + dy][:3] != K for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                op[x, y] = K + (255,)
    return out


# ---------- 僵尸进化线 ----------
zb = g['zombie']().img()
Z, Zs = PAL['z'], PAL['Z']
purple = recolor(zb, {Z: (184, 156, 210), Zs: (132, 104, 164), PAL['n']: (70, 58, 104), PAL['N']: (44, 34, 72)})
white = fuzz(recolor(zb, {Z: (222, 226, 220), Zs: (172, 178, 172)}), [(240, 242, 246), (206, 210, 220), (186, 190, 204)], 0.7, 2, 40)
green = fuzz(recolor(zb, {Z: (128, 178, 112), Zs: (86, 130, 74)}), [(96, 196, 88), (60, 150, 70), (140, 220, 110)], 0.8, 3, 45)


# ---------- 行尸新外形 ----------
def walker_base(shirt, shade, skin=None, skinS=None):
    im = wg['walker']().img()
    WP = wg['PAL']; mp = {WP['d']: shirt, WP['D']: shade}
    if skin: mp.update({WP['u']: skin, WP['U']: skinS})
    return pad(recolor(im, mp), 4)


def female():
    im = walker_base((226, 222, 232), (176, 170, 190))           # 白寿衣
    d = ImageDraw.Draw(im); H = (34, 30, 44)
    for x, y0, y1 in [(10, 11, 30), (11, 10, 31), (12, 10, 29), (13, 11, 27), (14, 11, 22), (19, 12, 22), (20, 12, 20)]:
        d.line([(x, y0), (x, y1)], fill=H)                         # 长发披到背后、垂过脸侧
    d.rectangle([12, 31, 15, 33], fill=(196, 40, 52)); d.rectangle([18, 33, 21, 33], fill=(196, 40, 52))  # 红绣花鞋
    d.point([(13, 32), (19, 33)], fill=(240, 200, 80))
    return outline(im)


def old():
    im = walker_base((84, 80, 92), (56, 52, 64))                 # 灰布长衫
    d = ImageDraw.Draw(im)
    for x, y in [(15, 12), (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (21, 13), (14, 13), (14, 14), (14, 15), (15, 16), (14, 16)]: d.point((x, y), fill=(226, 226, 232))  # 白发
    d.line([(19, 21), (23, 21)], fill=(226, 226, 232)); d.line([(21, 22), (21, 25)], fill=(226, 226, 232)); d.point((22, 22), fill=(226, 226, 232))   # 白胡子
    d.line([(26, 22), (27, 35)], fill=(120, 80, 44), width=1); d.line([(25, 22), (27, 22)], fill=(120, 80, 44))  # 拐杖
    return outline(im)


def soldier():
    im = walker_base((150, 40, 40), (104, 26, 30))               # 清兵号衣
    d = ImageDraw.Draw(im)
    d.ellipse([15, 22, 19, 26], fill=(236, 230, 214)); d.point((17, 24), fill=(150, 40, 40))   # 胸口“兵”字圆补
    d.polygon([(11, 9), (21, 9), (18, 5), (14, 5)], fill=(46, 40, 34)); d.line([(15, 4), (17, 4)], fill=(200, 40, 40))  # 凉帽+红缨
    d.line([(24, 4), (24, 34)], fill=(120, 84, 48)); d.polygon([(23, 4), (25, 4), (24, 0)], fill=(200, 204, 214))       # 长矛
    return outline(im)


def skeleton():
    BONE, BS = (226, 220, 200), (170, 162, 140)
    im = walker_base((92, 84, 74), (60, 54, 48), BONE, BS)
    d = ImageDraw.Draw(im)
    d.rectangle([20, 14, 22, 16], fill=K); d.point((21, 15), fill=(230, 60, 60))       # 空眼窝红光
    d.rectangle([20, 19, 23, 19], fill=K); d.point([(20, 18), (22, 18)], fill=BONE)    # 牙
    for y in (21, 23, 25): d.line([(15, y), (19, y)], fill=BONE)                       # 外露肋骨
    d.line([(14, 21), (14, 26)], fill=BS)
    return outline(im)


walk0 = pad(wg['walker']().img(), 4)

# ---------- 尸王 → 不化骨 ----------
king = g['king']().img()


def buhuagu():
    S = g['Spr'](40, 50)
    B, Bs, Bh = 'E', 'h', 'H'                           # 墨黑骨头
    PAL['E'] = (58, 54, 66)
    r = S.rect
    r(14, 3, 25, 13, B); S.clear((14, 3), (25, 3)); r(14, 3, 16, 12, Bs)        # 头骨
    r(17, 7, 19, 9, 'k'); r(21, 7, 23, 9, 'k'); S.px(18, 8, 'r'); S.px(22, 8, 'r')
    r(18, 11, 22, 12, 'k'); S.px(19, 12, B); S.px(21, 12, B)
    r(13, 1, 26, 2, 'X'); r(18, 0, 21, 0, 'o')                                   # 残破官帽
    r(19, 14, 20, 34, B)                                                          # 脊骨
    for y in (16, 19, 22, 25): r(14, y, 25, y, B); S.px(14, y + 1, Bs); S.px(25, y + 1, Bs)   # 肋骨
    r(13, 15, 14, 27, 'v'); r(25, 15, 26, 27, 'v')                               # 残袍
    r(15, 30, 24, 33, B)                                                          # 骨盆
    r(26, 16, 34, 17, B); r(34, 17, 36, 22, B); S.px(37, 23, 'k'); S.px(36, 24, 'k'); S.px(35, 23, 'k')   # 前伸骨爪
    r(5, 16, 13, 17, B); r(3, 17, 5, 22, B); S.px(2, 23, 'k'); S.px(3, 24, 'k')
    r(15, 34, 16, 44, B); r(23, 34, 24, 44, B); r(13, 45, 17, 46, B); r(22, 45, 26, 46, B)   # 腿骨
    for x, y in [(9, 30), (30, 29), (12, 38), (28, 40), (6, 26), (33, 12)]: S.px(x, y, 'V')  # 黑气
    S.outline()
    im = S.img()
    W2, H2 = im.width + 60, im.height + 40
    out = Image.new('RGBA', (W2, H2), (0, 0, 0, 0)); od = ImageDraw.Draw(out)
    random.seed(7)
    # rising smoke plumes (purple-black), pixel blobs
    for i in range(110):
        x = random.gauss(W2 / 2 + 4, 10); y = random.uniform(12, H2 - 10)
        r = random.choice((0, 1, 1, 1, 2)); a = random.randint(50, 120)
        col = random.choice([(70, 30, 96), (44, 20, 60), (96, 46, 130), (30, 14, 40)])
        od.rectangle([x - r, y - r, x + r, y + r], fill=col + (a,))
    # afterimage trail (two fading copies to the left)
    for k, al in ((26, 60), (14, 110)):
        ghost = im.copy(); ghost.putalpha(ghost.getchannel('A').point(lambda v: min(v, al)))
        tint = Image.new('RGBA', ghost.size, (80, 40, 110, 0)); tint.putalpha(ghost.getchannel('A'))
        out.alpha_composite(tint, (30 - k, 20))
    out.alpha_composite(im, (30, 20))
    # chest ember: the unspent breath
    cx, cy = 30 + 19, 20 + 20
    for rr, a in ((7, 50), (5, 90), (3, 160)): od.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(220, 40, 40, a))
    od.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=(255, 150, 110, 255))
    # wisps rising from shoulders/head
    for x0 in (cx - 10, cx, cx + 11):
        for j in range(8): od.point((x0 + int(3 * random.uniform(-1, 1)), 18 - j * 2), fill=(110, 60, 150, 140))
    return out


def shasha(plain=False):
    """尸煞：尸王怨气化形——仍是僵尸，但官袍破烂、白发狂乱、獠牙利爪更凶"""
    base = g['king']().img()
    P = g['PAL']
    im = recolor(base, {P['q']: (112, 124, 114), P['Q']: (72, 82, 78),          # 更死灰的脸
                        P['v']: (112, 42, 78), P['V']: (72, 24, 52),            # 褪色发黑的官袍
                        P['o']: (150, 110, 40), P['O']: (100, 72, 30)})
    im = pad(im, 8); d = ImageDraw.Draw(im); px = im.load(); T = (0, 0, 0, 0)
    ox, oy = 8, 8
    # 折断的孔雀翎：清掉
    for x in range(0, 13):
        for y in range(3, 12):
            if px[ox + x, oy + y][:3] in ((40, 140, 124), (90, 200, 130), (232, 180, 48), K) and x < 11: px[ox + x, oy + y] = T
    # 帽子裂口、歪斜
    d.line([(ox + 17, oy + 3), (ox + 19, oy + 8)], fill=K); d.point((ox + 22, oy + 4), fill=K)
    # 狂乱白发：向后飞散
    HW, HG = (236, 238, 244), (170, 176, 196)
    for (x0, y0, x1, y1) in [(9, 10, 3, 18), (9, 12, 2, 24), (10, 14, 4, 30), (11, 16, 6, 34), (10, 11, 5, 14), (12, 18, 8, 36)]:
        d.line([(ox + x0, oy + y0), (ox + x1, oy + y1)], fill=HW)
    for (x0, y0, x1, y1) in [(9, 13, 3, 21), (11, 15, 5, 28)]:
        d.line([(ox + x0, oy + y0), (ox + x1, oy + y1)], fill=HG)
    # 血红怒目 + 更长獠牙
    d.rectangle([ox + 16, oy + 12, ox + 18, oy + 14], fill=(230, 40, 40)); d.rectangle([ox + 21, oy + 12, ox + 23, oy + 14], fill=(230, 40, 40))
    d.point([(ox + 17, oy + 13), (ox + 22, oy + 13)], fill=(255, 220, 160))
    d.line([(ox + 15, oy + 11), (ox + 18, oy + 12)], fill=K); d.line([(ox + 24, oy + 11), (ox + 21, oy + 12)], fill=K)   # 竖眉
    d.line([(ox + 20, oy + 20), (ox + 20, oy + 22)], fill=(250, 250, 246)); d.line([(ox + 23, oy + 20), (ox + 23, oy + 22)], fill=(250, 250, 246))
    # 胸口撕开：露出肋骨与暗红的那口气
    d.rectangle([ox + 13, oy + 27, ox + 23, oy + 34], fill=(30, 12, 26))
    for y in (28, 30, 32): d.line([(ox + 14, oy + y), (ox + 22, oy + y)], fill=(150, 140, 120))
    # 衣摆、袖口撕成锯齿
    random.seed(11)
    for x in range(9, 28):
        cut = random.choice((0, 1, 2, 3, 4, 5))
        for y in range(40 - cut, 41): px[ox + x, oy + y] = T if px[ox + x, oy + y][3] else px[ox + x, oy + y]
    for x in range(21, 31, 2): px[ox + x, oy + 27] = T
    for (x, y) in [(11, 29), (12, 33), (25, 30), (26, 35), (10, 36)]: d.rectangle([ox + x, oy + y, ox + x + 1, oy + y + 2], fill=(20, 8, 18))   # 破洞
    for x in range(21, 31): 
        if random.random() < 0.6: px[ox + x, oy + 27] = T; px[ox + x, oy + 26] = T if random.random() < 0.3 else px[ox + x, oy + 26]
    # 更长的利爪
    for i, (x, y) in enumerate([(33, 31), (34, 32), (35, 33)]): d.line([(ox + x, oy + y), (ox + x + 2, oy + y + 4)], fill=K)
    im = outline(im)
    if plain: return im
    # 煞气、胸口光
    W2, H2 = im.width + 30, im.height + 20
    out = Image.new('RGBA', (W2, H2), (0, 0, 0, 0)); od = ImageDraw.Draw(out)
    random.seed(7)
    for i in range(90):
        x = random.gauss(W2 / 2, 11); y = random.uniform(6, H2 - 8); r = random.choice((0, 1, 1, 2)); a = random.randint(40, 110)
        od.rectangle([x - r, y - r, x + r, y + r], fill=random.choice([(70, 30, 96), (44, 20, 60), (96, 46, 130)]) + (a,))
    for k, al in ((18, 50), (9, 90)):
        gh = im.copy(); tint = Image.new('RGBA', gh.size, (80, 40, 110, 0)); tint.putalpha(gh.getchannel('A').point(lambda v: min(v, al)))
        out.alpha_composite(tint, (15 - k, 10))
    out.alpha_composite(im, (15, 10))
    cx, cy = 15 + ox + 18, 10 + oy + 30
    for rr, a in ((5, 40), (4, 80), (2, 160)): od.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(220, 40, 40, a))
    od.point((cx, cy), fill=(255, 170, 120, 255))
    return out


# ---------- 拼图 ----------
SC = 5
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
fT, fH, fN, fS = (ImageFont.truetype(FONT, s) for s in (40, 28, 22, 17))
W = 1280
sheet = Image.new('RGB', (W, 1460), (26, 18, 40)); d = ImageDraw.Draw(sheet)
d.text((W // 2, 40), '暂时停止呼吸 · 新怪物示意图', font=fT, fill=(244, 228, 168), anchor='mm')


def put(im, cx, base, sc=SC):
    big = im.resize((im.width * sc, im.height * sc), Image.NEAREST)
    sheet.paste(big, (cx - big.width // 2, base - big.height), big)


def section(y, title, sub):
    d.rectangle([30, y, W - 30, y + 2], fill=(74, 56, 102))
    d.text((40, y + 14), title, font=fH, fill=(240, 192, 32)); d.text((40, y + 52), sub, font=fS, fill=(169, 156, 200))


def label(cx, y, name, desc, col=(236, 228, 255)):
    d.text((cx, y), name, font=fN, fill=col, anchor='mm')
    for i, line in enumerate(desc.split('\n')): d.text((cx, y + 28 + i * 22), line, font=fS, fill=(169, 156, 200), anchor='mm')


# 1. 进化线
section(80, '一、僵尸进化线（随时辰推进）', '同一种僵尸按时间换装变强；红衣跳尸、游魂、行尸保持不变')
xs = [190, 480, 770, 1060]; base = 420
for x, im in zip(xs, [zb, purple, white, green]): put(im, x, base)
for a, b in zip(xs[1:], xs[2:]): d.text(((a + b) // 2, base - 90), '→', font=fT, fill=(240, 192, 32), anchor='mm')
label(xs[0], base + 30, '现在的普通僵尸', '（对比用）', (169, 156, 200))
label(xs[1], base + 30, '紫僵 · 0:00 起', '刚尸变，淡紫皮肤\n走得慢、血少，前期主力', (196, 168, 230))
label(xs[2], base + 30, '白僵 · 1:00 起', '一层白毛，怕火怕光\n雷法/金光/八卦阵 伤害×2', (240, 240, 246))
label(xs[3], base + 30, '绿僵 · 2:00 起', '绿色长毛，走得快\n会蓄力扑跳', (140, 220, 110))

# 2. 行尸外形
y2 = 560
section(y2, '二、行尸新外形（能力相同，随机出现）', '共同特征：驼背前倾、摇晃行走；只换发型、衣服和道具。半腐骷髅是唯一有特殊能力的变种')
xs = [300, 640, 980]; base = y2 + 300
for x, im in zip(xs, [walk0, female(), skeleton()]): put(im, x, base)
label(xs[0], base + 30, '原版行尸', '粗布衣', (169, 156, 200))
label(xs[1], base + 30, '女尸', '披发、白寿衣、红绣鞋')
label(xs[2], base + 30, '半腐骷髅（特殊）', '骷髅头、外露肋骨\n打散后会重新站起来一次', (255, 138, 122))

# 3. 尸王第二阶段
y3 = 1010
section(y3, '三、尸王第二阶段：尸煞（概念）', '“葬了十年还不化……这口气，没咽下去。”——尸王倒下，那口怨气化形而出')
base = y3 + 340
put(king, 400, base, 6); put(shasha(), 880, base + 72, 6)
d.text((640, base - 130), '→', font=fT, fill=(240, 192, 32), anchor='mm')
label(400, base + 28, '尸王（第一阶段）', '吸星大法 / 空气斩 / 泰山压顶 / 尸吼')
label(880, base + 28, '尸煞（第二阶段）', '官袍破烂、白发狂乱、血目獠牙，缠紫黑煞气\n胸口撕开露出暗红光=那口气（弱点）', (200, 150, 240))
sheet.save('/tmp/claude-0/-home-claude-jiangshi/bca195c0-0ab4-58df-abab-e3800b33c5f6/scratchpad/新怪物示意图.png')
print('ok')
