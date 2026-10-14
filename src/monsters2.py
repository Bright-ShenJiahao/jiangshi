# 新怪物与道具：吸血鬼、红衣厉鬼、毛僵、宝箱（原创像素图）
# 需先 exec sprites.py 的定义（Spr / PAL / ghost / zombie）
from PIL import Image
import random


def vampire():
    """西洋吸血鬼：背头美人尖、苍白脸、红眼獠牙、立领黑斗篷红里子"""
    s = Spr(30, 38)
    # cape back (wide, red lining visible at sides)
    s.rect(4, 14, 25, 34, 'k'); s.rect(5, 15, 24, 33, 'h')
    s.rect(5, 18, 7, 33, 'X'); s.rect(22, 18, 24, 33, 'X')
    s.rect(3, 30, 6, 35, 'h'); s.rect(23, 30, 26, 35, 'h')
    # high collar
    s.rect(7, 10, 9, 17, 'X'); s.rect(20, 10, 22, 17, 'X'); s.rect(7, 10, 7, 14, 'r'); s.rect(22, 10, 22, 14, 'r')
    # head
    s.rect(10, 4, 19, 15, 'W'); s.rect(10, 4, 11, 14, 'G')
    s.rect(9, 2, 20, 6, 'k'); s.rect(10, 1, 19, 2, 'k'); s.px(15, 7, 'k'); s.px(14, 7, 'k')  # slick hair + widow's peak
    s.rect(9, 6, 9, 10, 'k'); s.rect(20, 6, 20, 9, 'k')
    s.rect(12, 9, 13, 9, 'k'); s.rect(16, 9, 17, 9, 'k')                                     # brows
    s.px(12, 10, 'r'); s.px(17, 10, 'r'); s.px(13, 10, 'R'); s.px(16, 10, 'R')               # red eyes
    s.rect(13, 13, 16, 13, 'X'); s.px(13, 14, 'w'); s.px(16, 14, 'w')                         # mouth + fangs
    # vest / shirt
    s.rect(11, 16, 18, 27, 'v'); s.rect(14, 16, 15, 22, 'w'); s.px(14, 17, 'r'); s.px(15, 17, 'r')
    s.rect(11, 24, 18, 24, 'o')
    # arms (claw hands forward)
    s.rect(8, 17, 10, 25, 'h'); s.rect(19, 17, 21, 25, 'h'); s.rect(21, 22, 24, 24, 'h')
    s.rect(24, 22, 26, 24, 'W'); s.px(27, 22, 'k'); s.px(27, 24, 'k')
    s.rect(8, 26, 10, 27, 'W')
    # legs
    s.rect(11, 28, 13, 34, 'k'); s.rect(16, 28, 18, 34, 'k'); s.rect(11, 35, 14, 36, 'h'); s.rect(16, 35, 19, 36, 'h')
    s.outline()
    return s


def recolor(im, mapping):
    out = im.copy(); px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a and (r, g, b) in mapping: px[x, y] = mapping[(r, g, b)] + (a,)
    return out


def red_ghost(g):
    """红衣厉鬼：游魂白衣换成血红"""
    P = g['PAL']
    im = g['ghost']().img()
    return recolor(im, {P['W']: (196, 38, 38), P['G']: (130, 22, 26), P['g']: (236, 214, 214)})


def hairy(im, seed=3, col=(226, 230, 236)):
    """毛僵：在轮廓外随机长出白毛"""
    random.seed(seed)
    W, H = im.width + 4, im.height + 4
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.paste(im, (2, 2), im)
    for k, prob in ((0, 0.85), (1, 0.5)):
        src = out.copy(); sp, op = src.load(), out.load()
        for y in range(H):
            for x in range(W):
                if sp[x, y][3]: continue
                n = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H and sp[x + dx, y + dy][3])
                if n and random.random() < prob and y < H - 5: op[x, y] = (col if random.random() < 0.7 else (176, 180, 196)) + (255,)
    sp = im.copy().load()
    # a few tufts on the body
    for _ in range(40):
        x, y = random.randrange(W), random.randrange(H - 6)
        if 2 <= x < W - 2 and 2 <= y < H - 2 and sp[x - 2, y - 2][3] and sp[x - 2, y - 2][:3] != (24, 14, 30): op[x, y] = col + (255,)
    return out


def chest(big=False):
    s = Spr(22 if big else 16, 18 if big else 14)
    w, h = (22, 18) if big else (16, 14)
    s.rect(1, h // 2, w - 2, h - 2, 'B'); s.rect(1, 2, w - 2, h // 2, 'b'); s.rect(2, 1, w - 3, 2, 'b')
    s.rect(1, h // 2, w - 2, h // 2, 'k')
    for x in (3, w - 4): s.rect(x, 1, x, h - 2, 'o' if big else 'O')
    s.rect(w // 2 - 2, h // 2 - 2, w // 2 + 1, h // 2 + 2, 'o'); s.px(w // 2 - 1, h // 2, 'k')
    if big: s.rect(2, 3, w - 3, 3, 'L')
    s.outline()
    return s
