# 防守版新怪（原创像素图）：灵幻先生 / 驱魔警察 / 僵尸道长 里的反派。全部朝右。
# 需先 exec sprites.py（Spr / PAL）
PAL.update({
    'a': (200, 196, 210), 'A': (140, 136, 156),            # 灰白（头发、旧布）
    'i': (196, 232, 250), 'I': (120, 176, 214),            # 冰
    'T': (255, 150, 50), 't': (255, 220, 110),              # 火、裂缝
    'x': (36, 30, 34), 'd': (60, 50, 56),                   # 焦黑
    'F': (178, 220, 210), 'K': (110, 160, 160),             # 鬼魂青白
    '1': (240, 180, 200), '2': (190, 110, 140),             # 和服粉
    '3': (120, 70, 40), '4': (200, 150, 70), '5': (90, 54, 30),   # 蛾翅
    '6': (180, 30, 40), '7': (110, 10, 20),                 # 血红
    '8': (70, 60, 110), '9': (40, 30, 70),                  # 深紫
})
PAL.setdefault('P', (236, 112, 104))


def wangpo():
    """王婆：马贼帮的老巫婆，灰发挽髻，黑衣红边，驼背，手里一根骷髅拐杖"""
    s = Spr(28, 36)
    s.rect(9, 1, 15, 4, 'a'); s.rect(11, 0, 14, 1, 'A'); s.px(15, 2, 'r')            # 发髻 + 红簪
    s.rect(8, 4, 16, 13, 's'); s.rect(8, 4, 10, 12, 'a'); s.clear((8, 13), (16, 13))
    s.px(14, 7, 'k'); s.px(15, 7, 'r'); s.rect(13, 9, 15, 9, 'S'); s.rect(12, 11, 16, 11, 'S'); s.px(14, 12, 'k')
    s.px(17, 8, 's'); s.px(17, 9, 'S')
    s.rect(6, 14, 18, 30, 'h'); s.rect(6, 14, 8, 30, 'k'); s.rect(5, 26, 19, 30, 'h')
    s.rect(12, 14, 12, 30, 'r'); s.rect(5, 30, 19, 30, 'r'); s.rect(10, 20, 15, 21, 'r')
    s.rect(17, 16, 21, 18, 'h'); s.rect(21, 16, 22, 18, 's')                          # 前伸的手
    s.rect(23, 4, 23, 33, 'B'); s.rect(22, 1, 25, 4, 'w'); s.px(23, 2, 'k'); s.px(25, 2, 'k')   # 骷髅拐杖
    s.rect(8, 31, 11, 33, 'k'); s.rect(13, 31, 16, 33, 'k')
    s.outline(); return s


def wangpo_ghost():
    """王婆死后：鬼王。白发散开，青白脸，红眼，黑袍下摆化成烟"""
    s = Spr(32, 40)
    for x in range(5, 23): s.rect(x, 2 + abs(x - 14) // 3, x, 14 + (x * 7) % 5, 'a')
    s.rect(9, 4, 18, 14, 'F'); s.rect(9, 4, 10, 13, 'K')
    s.rect(14, 7, 16, 8, 'r'); s.px(15, 8, 'w'); s.rect(13, 11, 17, 11, 'k'); s.px(14, 12, 'w'); s.px(16, 12, 'w')
    s.rect(6, 15, 21, 26, 'h'); s.rect(6, 15, 8, 26, 'k'); s.rect(13, 15, 13, 26, 'r')
    for x in range(6, 22): s.rect(x, 27, x, 27 + (x * 5) % 9, 'h' if x % 3 else 'H')
    s.rect(20, 16, 27, 18, 'h'); s.rect(27, 15, 30, 19, 'F'); s.px(31, 15, 'k'); s.px(31, 19, 'k')
    s.rect(2, 16, 6, 19, 'h'); s.rect(0, 16, 2, 19, 'F')
    s.outline(); return s


def tan_ghost():
    """谭百万家的厉鬼：长发遮脸，灰白寿衣，嘴角流血"""
    s = Spr(24, 34)
    s.rect(6, 0, 17, 20, 'h'); s.rect(5, 6, 18, 22, 'h')
    s.rect(11, 6, 15, 14, 'F'); s.px(13, 9, 'r'); s.px(14, 9, 'r'); s.rect(12, 12, 14, 12, 'k'); s.px(13, 13, 'r'); s.px(13, 14, 'r')
    s.rect(7, 18, 17, 28, 'a'); s.rect(7, 18, 8, 28, 'A'); s.rect(12, 18, 12, 28, 'A')
    for x in range(7, 18): s.rect(x, 29, x, 29 + (x * 3) % 4, 'a')
    s.rect(16, 19, 22, 21, 'a'); s.rect(22, 19, 23, 21, 'F')
    s.outline(); return s


def bandit(fat=False):
    """马贼鬼魂：山狗（瘦，拿刀）/ 山猪（胖），头缠布，半透明青色"""
    s = Spr(26, 34)
    x0, x1 = (6, 19) if fat else (8, 16)
    s.rect(x0 + 1, 1, x1 - 1, 3, 'r'); s.px(x0, 2, 'r'); s.px(x0 - 1, 3, 'r')                # 头巾
    s.rect(x0 + 1, 4, x1 - 1, 12, 'F'); s.rect(x0 + 1, 4, x0 + 2, 11, 'K'); s.clear((x0 + 1, 12), (x1 - 1, 12))
    s.rect(x1 - 4, 7, x1 - 3, 7, 'k'); s.rect(x1 - 5, 10, x1 - 2, 10, 'k')
    if fat: s.rect(x1 - 6, 11, x1 - 2, 11, 'k')
    s.rect(x0, 13, x1, 25, 'K'); s.rect(x0 + 2, 13, x1 - 2, 25, 'B'); s.rect(x0 + 4, 14, x1 - 4, 25, 'F')   # 敞开的坎肩
    s.rect(x0, 22, x1, 23, 'h')
    s.rect(x0 + 1, 26, x0 + 4, 31, 'h'); s.rect(x1 - 4, 26, x1 - 1, 31, 'h')
    s.rect(x1, 15, x1 + 4, 17, 'F')
    if not fat: s.rect(x1 + 4, 8, x1 + 5, 16, 'W'); s.rect(x1 + 3, 16, x1 + 6, 17, 'B')   # 刀
    else: s.rect(x1 + 4, 14, x1 + 6, 18, 'F')
    s.outline(); return s


def dabao():
    """大宝：老实的成年鬼，圆脸，灰布衫，有点憨"""
    s = Spr(22, 32)
    s.rect(6, 1, 15, 3, 'h'); s.rect(6, 4, 15, 12, 'F'); s.rect(6, 4, 7, 11, 'K'); s.clear((6, 12), (15, 12))
    s.px(11, 7, 'k'); s.px(14, 7, 'k'); s.rect(11, 10, 14, 10, 'k'); s.px(10, 9, '1'); s.px(15, 9, '1')
    s.rect(5, 13, 16, 24, 'A'); s.rect(5, 13, 6, 24, 'a'); s.rect(10, 13, 11, 24, 'a')
    for x in range(5, 17): s.rect(x, 25, x, 25 + (x * 3) % 4, 'A')
    s.rect(16, 15, 19, 17, 'A'); s.rect(19, 15, 20, 17, 'F')
    s.outline(); return s


def xiaobao():
    """小宝：童鬼，冲天辫，机灵"""
    s = Spr(16, 24)
    s.rect(7, 0, 8, 2, 'h'); s.px(9, 0, 'r')
    s.rect(4, 3, 11, 10, 'F'); s.rect(4, 3, 5, 9, 'K'); s.clear((4, 10), (11, 10))
    s.px(8, 6, 'k'); s.px(10, 6, 'k'); s.rect(8, 8, 10, 8, 'k'); s.px(7, 7, '1')
    s.rect(4, 11, 11, 17, 'r'); s.rect(4, 11, 5, 17, 'X')
    for x in range(4, 12): s.rect(x, 18, x, 18 + (x * 5) % 4, 'r' if x % 2 else 'X')
    s.rect(11, 12, 14, 13, 'r'); s.rect(14, 11, 15, 13, 'F')
    s.outline(); return s


def oil_ghost():
    """半生熟油炸鬼：浑身漆黑焦脆，身上裂口透出火光，黄眼"""
    s = Spr(28, 38)
    s.rect(9, 2, 18, 13, 'x'); s.rect(9, 2, 11, 12, 'd'); s.clear((9, 13), (18, 13))
    s.rect(14, 6, 16, 7, 'p'); s.px(16, 7, 'k'); s.rect(13, 10, 17, 11, 'T'); s.px(14, 10, 'x'); s.px(16, 10, 'x')
    s.rect(6, 14, 21, 28, 'x'); s.rect(6, 14, 8, 28, 'd')
    for (a, b, c, d2) in ((10, 16, 13, 19), (15, 18, 18, 22), (9, 23, 12, 26), (16, 25, 19, 27)):
        s.px(a, b, 't'); s.px(c, d2, 't'); s.px((a + c) // 2, (b + d2) // 2, 'T')
    s.rect(20, 15, 26, 18, 'x'); s.rect(25, 15, 27, 19, 'd'); s.px(27, 20, 'T')
    s.rect(2, 15, 6, 18, 'x')
    s.rect(8, 29, 12, 35, 'x'); s.rect(15, 29, 19, 35, 'x'); s.px(10, 32, 'T'); s.px(17, 31, 't')
    s.outline(); return s


def ice_corpse(woman=False):
    """冰封行尸（运毒死尸）：青白脸、结霜，穿九十年代的衬衫/连衣裙，直挺挺地走"""
    s = Spr(24, 36)
    if woman: s.rect(7, 1, 16, 14, 'h'); s.rect(6, 6, 7, 20, 'h')
    else: s.rect(8, 1, 15, 3, 'h')
    s.rect(8, 4, 15, 13, 'i'); s.rect(8, 4, 9, 12, 'I'); s.clear((8, 13), (15, 13))
    s.rect(12, 7, 14, 7, 'W'); s.px(13, 7, 'C'); s.rect(12, 11, 14, 11, 'I')
    if woman:
        s.rect(7, 14, 16, 27, 'C'); s.rect(7, 14, 8, 27, 'n'); s.rect(6, 24, 17, 28, 'C')
    else:
        s.rect(7, 14, 16, 24, 'w'); s.rect(7, 14, 8, 24, 'G'); s.rect(11, 14, 12, 18, 'C')
        s.rect(7, 25, 16, 30, 'B'); s.rect(11, 27, 12, 30, 'k')
    s.rect(16, 15, 21, 17, 'w' if not woman else 'C'); s.rect(21, 15, 22, 17, 'i')
    for (x, y) in ((9, 16), (14, 20), (10, 26), (19, 15)): s.px(x, y, 'g')
    s.rect(8, 31 if not woman else 29, 11, 33, 'k'); s.rect(13, 31 if not woman else 29, 16, 33, 'k')
    s.outline(); return s


def thug(big=False):
    """邪术打手：一个泰拳手（短裤、绑手），一个练健身的大块头（背心），身上冒紫气"""
    s = Spr(28, 36)
    x0, x1 = (6, 21) if big else (8, 19)
    s.rect(x0 + 3, 1, x1 - 3, 3, 'h' if big else 'r')
    s.rect(x0 + 3, 3, x1 - 3, 11, 'S' if big else 's'); s.rect(x0 + 3, 3, x0 + 4, 10, 'b'); s.clear((x0 + 3, 11), (x1 - 3, 11))
    s.px(x1 - 5, 6, 'v'); s.px(x1 - 4, 6, 'k'); s.rect(x1 - 6, 9, x1 - 4, 9, 'k')
    if big:
        s.rect(x0, 12, x1, 23, 'S'); s.rect(x0 + 3, 12, x1 - 3, 23, 'k'); s.rect(x0 + 4, 13, x1 - 4, 23, 'h')
        s.rect(x0, 13, x0 + 2, 20, 'b'); s.rect(x1 - 2, 13, x1, 20, 'b')
        s.rect(x0 + 1, 24, x1 - 1, 30, 'n')
    else:
        s.rect(x0 + 1, 12, x1 - 1, 23, 's'); s.rect(x0 + 1, 12, x0 + 2, 23, 'S'); s.rect(x0 + 5, 16, x1 - 5, 16, 'S'); s.rect(x0 + 5, 19, x1 - 5, 19, 'S')
        s.rect(x0 + 1, 24, x1 - 1, 28, 'r'); s.rect(x0 + 1, 24, x1 - 1, 24, 'w'); s.rect(x0 + 2, 29, x0 + 4, 31, 's'); s.rect(x1 - 4, 29, x1 - 2, 31, 's')
    s.rect(x1, 13, x1 + 5, 16, 'S' if big else 's'); s.rect(x1 + 5, 12, x1 + 7, 17, 'w' if not big else 'S')
    s.rect(x0 - 3, 14, x0, 17, 'S' if big else 's'); s.rect(x0 - 4, 13, x0 - 3, 17, 'w' if not big else 'S')
    if big: s.rect(x0 + 2, 31, x0 + 5, 33, 'k'); s.rect(x1 - 5, 31, x1 - 2, 33, 'k')
    else: s.rect(x0 + 2, 32, x0 + 4, 33, 'k'); s.rect(x1 - 4, 32, x1 - 2, 33, 'k')
    s.outline(); return s


def jiuju(demon=False):
    """九菊一派女教主：白衣红袴、黑长发；魔化后灰皮、生角、披头散发、指甲变爪"""
    s = Spr(28, 40)
    skin, skin2 = ('A', '8') if demon else ('s', 'S')
    s.rect(8, 1, 18, 4, 'h'); s.rect(7, 4, 9, 24 if demon else 20, 'h'); s.rect(18, 4, 19, 10, 'h')
    if demon:
        s.rect(9, 0, 10, 2, 'w'); s.rect(16, 0, 17, 2, 'w'); s.px(8, 0, 'w'); s.px(18, 0, 'w')
        for x in range(5, 22, 2): s.rect(x, 3, x, 6 + (x * 3) % 6, 'h')
    else:
        s.rect(12, 0, 14, 1, 'r')
    s.rect(10, 4, 17, 13, skin); s.rect(10, 4, 11, 12, skin2); s.clear((10, 13), (17, 13))
    s.px(14, 7, 'k'); s.px(16, 7, 'r' if demon else 'k'); s.px(15, 7, 'r' if demon else 's')
    s.rect(14, 10, 16, 10, 'r'); s.px(17, 10, 'r')
    robe, robe2, pants = ('9', '8', '7') if demon else ('w', 'G', 'r')
    s.rect(8, 14, 19, 25, robe); s.rect(8, 14, 9, 25, robe2); s.rect(12, 14, 13, 20, robe2); s.rect(8, 20, 19, 21, 'v' if not demon else '7')
    s.rect(7, 26, 20, 35, pants); s.rect(7, 26, 8, 35, 'X'); s.rect(13, 27, 13, 35, 'X')
    s.rect(18, 15, 24, 18, robe); s.rect(23, 18, 24, 20, skin)
    if demon: s.px(25, 19, 'w'); s.px(25, 21, 'w'); s.px(24, 21, 'w')
    else: s.rect(24, 13, 26, 15, 'p'); s.px(25, 14, 'r')                       # 符
    s.rect(3, 16, 8, 19, robe); s.rect(3, 19, 4, 20, skin)
    s.rect(9, 36, 12, 38, 'w' if not demon else 'k'); s.rect(15, 36, 18, 38, 'w' if not demon else 'k')
    s.outline(); return s


def feitou():
    """飞降（飞头降）：只有一颗头飞着，长发，下面拖着肠子"""
    s = Spr(20, 30)
    s.rect(5, 0, 14, 3, 'h'); s.rect(3, 3, 5, 14, 'h'); s.rect(14, 3, 16, 12, 'h')
    s.rect(6, 3, 13, 12, 'F'); s.rect(6, 3, 7, 11, 'K')
    s.rect(9, 6, 10, 6, 'r'); s.rect(12, 6, 13, 6, 'r'); s.rect(9, 9, 13, 10, 'k'); s.px(10, 10, 'w'); s.px(12, 10, 'w')
    s.rect(7, 13, 12, 13, 'F')
    for i, x in enumerate((8, 10, 12)):
        for y in range(14, 27 - i * 2): s.px(x + ((y + i) // 3) % 2, y, '6' if (y + i) % 3 else '7')
    s.rect(9, 14, 11, 16, '2')
    s.outline(); return s


def xiaozun():
    """小尊（小僵尸）：小孩个子，清朝小帽，青脸，伸手"""
    s = Spr(18, 26)
    s.rect(5, 0, 12, 3, 'h'); s.rect(8, 0, 9, 0, 'r'); s.rect(4, 3, 13, 3, 'H')
    s.rect(5, 4, 12, 11, 'z'); s.rect(5, 4, 6, 10, 'Z'); s.clear((5, 11), (12, 11))
    s.px(9, 6, 'k'); s.px(11, 6, 'k'); s.px(9, 9, 'w'); s.px(11, 9, 'w'); s.rect(9, 8, 11, 8, 'k')
    s.rect(4, 12, 13, 20, 'n'); s.rect(4, 12, 5, 20, 'N'); s.rect(8, 12, 9, 20, 'o')
    s.rect(13, 13, 17, 15, 'n'); s.rect(17, 13, 17, 15, 'z')
    s.rect(5, 21, 7, 24, 'k'); s.rect(10, 21, 12, 24, 'k')
    s.outline(); return s


def moth():
    """大罗金仙（蛾妖）：蛾翅上有两只眼纹，触角，人身披金纱"""
    s = Spr(40, 38)
    for sx in (-1, 1):
        cx = 20
        for y in range(4, 30):
            w = int(16 * (1 - abs(y - 14) / 16) ** 0.7) if y < 30 else 0
            for x in range(1, w + 1):
                c = '3' if (x + y) % 5 else '5'
                if x > w - 2: c = '5'
                s.px(cx + sx * (x + 2), y, c)
        for (ex, ey) in ((9, 11), (8, 22)):
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx * dx + dy * dy <= 5: s.px(cx + sx * (ex + 2) + dx, ey + dy, '4')
            s.px(cx + sx * (ex + 2), ey, 'k'); s.px(cx + sx * (ex + 2) + 1, ey - 1, 'w')
    s.px(18, 1, 'h'); s.px(17, 0, 'h'); s.px(22, 1, 'h'); s.px(23, 0, 'h')
    s.rect(17, 2, 23, 9, 's'); s.rect(17, 2, 23, 3, 'h'); s.px(21, 6, 'k'); s.px(22, 6, '4'); s.rect(20, 8, 22, 8, 'r')
    s.rect(17, 10, 23, 26, 'o'); s.rect(17, 10, 18, 26, 'O'); s.rect(19, 10, 21, 26, 'p')
    s.rect(17, 27, 23, 33, 'O'); s.rect(18, 34, 19, 36, 's'); s.rect(21, 34, 22, 36, 's')
    s.outline(); return s


def xuemo():
    """罗平（血魔）：浑身血红，青筋，红眼，獠牙，滴血的爪子"""
    s = Spr(28, 38)
    s.rect(9, 1, 18, 3, 'h'); s.rect(9, 3, 18, 13, '6'); s.rect(9, 3, 11, 12, '7'); s.clear((9, 13), (18, 13))
    s.rect(14, 6, 16, 6, 'p'); s.px(16, 6, 'k'); s.rect(13, 10, 17, 10, 'k'); s.px(14, 11, 'w'); s.px(16, 11, 'w')
    s.rect(6, 14, 21, 26, '6'); s.rect(6, 14, 8, 26, '7'); s.rect(10, 17, 17, 17, '7'); s.rect(10, 21, 17, 21, '7'); s.rect(13, 14, 13, 26, '7')
    s.rect(7, 27, 20, 30, 'x')
    s.rect(21, 15, 25, 18, '6'); s.rect(25, 14, 27, 19, '7'); s.px(27, 20, '6'); s.px(26, 22, '6')
    s.rect(2, 15, 6, 18, '6'); s.rect(1, 18, 2, 20, '7')
    s.rect(8, 31, 12, 35, '6'); s.rect(15, 31, 19, 35, '6'); s.rect(8, 35, 12, 36, '7'); s.rect(15, 35, 19, 36, '7')
    s.outline(); return s


def cixi():
    """慈禧太后（尸变）：大拉翅头饰带花、青白脸、黄缎绣袍、长长的金护甲"""
    s = Spr(32, 42)
    s.rect(6, 0, 23, 5, 'h'); s.rect(5, 1, 24, 3, 'h'); s.px(9, 1, 'r'); s.px(14, 2, 'P'); s.px(19, 1, 'r'); s.px(16, 0, 'o')
    s.rect(11, 6, 12, 8, 'o'); s.rect(9, 6, 19, 15, 'z'); s.rect(9, 6, 10, 14, 'Z'); s.clear((9, 15), (19, 15))
    s.rect(14, 9, 16, 9, 'k'); s.px(17, 9, 'k'); s.rect(15, 13, 17, 13, 'r'); s.px(15, 14, 'w')
    s.rect(6, 16, 22, 36, 'y'); s.rect(6, 16, 8, 36, 'Y'); s.rect(5, 30, 23, 36, 'y')
    s.rect(9, 16, 19, 18, 'n'); s.rect(13, 19, 15, 36, 'O')
    for (x, y) in ((10, 23), (18, 23), (10, 31), (18, 31)): s.rect(x - 1, y - 1, x + 1, y + 1, 'r'); s.px(x, y, 'o')
    s.rect(22, 17, 27, 20, 'y'); s.rect(27, 18, 28, 20, 'z')
    for k in range(3): s.rect(28 + k, 17 + k, 28 + k, 17 + k, 'o')
    s.px(31, 20, 'o'); s.px(30, 21, 'o')
    s.rect(2, 17, 6, 20, 'y'); s.rect(1, 20, 2, 22, 'o')
    s.rect(9, 37, 12, 40, 'w'); s.rect(16, 37, 19, 40, 'w'); s.rect(9, 40, 12, 40, 'k'); s.rect(16, 40, 19, 40, 'k')   # 花盆底鞋
    s.outline(); return s


def qingbing():
    """清兵僵尸：红缨凉帽，胸前一个「勇」字补子，青脸"""
    s = Spr(26, 36)
    s.rect(6, 3, 18, 4, 'b'); s.rect(8, 1, 16, 3, 'L'); s.rect(11, 0, 13, 1, 'r'); s.rect(10, 2, 14, 3, 'r')
    s.rect(8, 5, 16, 13, 'z'); s.rect(8, 5, 9, 12, 'Z'); s.clear((8, 13), (16, 13))
    s.px(13, 8, 'k'); s.px(15, 8, 'k'); s.rect(13, 11, 15, 11, 'k'); s.px(14, 12, 'w')
    s.rect(6, 14, 17, 27, 'n'); s.rect(6, 14, 7, 27, 'N'); s.rect(6, 14, 17, 15, 'r')
    s.rect(9, 18, 14, 23, 'w'); s.rect(10, 19, 13, 22, 'r'); s.px(11, 20, 'w'); s.px(12, 21, 'w')      # 勇
    s.rect(17, 15, 23, 17, 'n'); s.rect(23, 15, 24, 17, 'z')
    s.rect(7, 28, 10, 33, 'h'); s.rect(13, 28, 16, 33, 'h'); s.rect(7, 33, 10, 34, 'k'); s.rect(13, 33, 16, 34, 'k')
    s.outline(); return s


def xuankui():
    """僵尸王玄魁：清朝亲王，黑底金龙袍、红顶冠，青白脸长獠牙，身后披风，能飞"""
    s = Spr(36, 42)
    for y in range(14, 38): s.rect(3, y, 7 + (y - 14) // 4, y, '7')                  # 披风
    s.rect(10, 0, 21, 4, 'h'); s.rect(9, 4, 22, 5, 'h'); s.rect(14, 0, 17, 1, 'r'); s.px(15, -0, 'o')
    s.rect(11, 6, 20, 15, 'W'); s.rect(11, 6, 12, 14, 'G'); s.clear((11, 15), (20, 15))
    s.rect(16, 9, 18, 9, 'r'); s.px(18, 9, 'k'); s.rect(15, 12, 19, 12, 'k'); s.px(16, 13, 'w'); s.px(16, 14, 'w'); s.px(18, 13, 'w'); s.px(18, 14, 'w')
    s.rect(8, 16, 23, 34, 'h'); s.rect(8, 16, 10, 34, 'k'); s.rect(15, 16, 16, 34, 'o')
    for (x, y) in ((12, 20), (19, 22), (12, 28), (19, 30)): s.px(x, y, 'o'); s.px(x + 1, y + 1, 'o'); s.px(x - 1, y + 1, 'O')
    s.rect(23, 17, 30, 20, 'h'); s.rect(30, 17, 31, 20, 'W'); s.px(32, 18, 'w'); s.px(32, 20, 'w')
    s.rect(10, 35, 13, 39, 'k'); s.rect(18, 35, 21, 39, 'k')
    s.outline(); return s


def yangfy():
    """杨飞云（入魔）：算命先生的长衫变成黑紫，头上冒黑气，眼睛发绿光，手托罗盘"""
    s = Spr(28, 40)
    for x in range(8, 19): s.rect(x, 0, x, 2 + (x * 7) % 4, '9')
    s.rect(9, 3, 18, 13, 'A'); s.rect(9, 3, 11, 12, '8'); s.clear((9, 13), (18, 13))
    s.rect(14, 7, 16, 7, 'j'); s.px(16, 7, 'w'); s.rect(13, 10, 17, 10, 'k')
    s.rect(11, 12, 17, 15, 'a')                                                     # 胡子
    s.rect(7, 14, 20, 34, '9'); s.rect(7, 14, 9, 34, 'k'); s.rect(13, 16, 14, 34, '8'); s.rect(6, 28, 21, 34, '9')
    s.rect(20, 16, 23, 19, '9'); s.rect(23, 14, 27, 19, 'o'); s.rect(24, 15, 26, 18, 'O'); s.px(25, 16, 'r')   # 罗盘
    s.rect(3, 17, 7, 20, '9'); s.rect(2, 20, 3, 21, 'A')
    s.rect(9, 35, 12, 37, 'k'); s.rect(15, 35, 18, 37, 'k')
    s.outline(); return s


def xieshen():
    """邪神（大魔神）：巨大的魔神真身，双角、四臂、三只眼，周身黑红火焰"""
    s = Spr(52, 60)
    for x in range(10, 42): s.rect(x, 8 + (x * 5) % 6, x, 12, '7')                  # 火焰头光
    s.rect(17, 2, 18, 9, 'w'); s.rect(33, 2, 34, 9, 'w'); s.px(16, 1, 'w'); s.px(35, 1, 'w')
    s.rect(18, 8, 33, 22, '6'); s.rect(18, 8, 20, 21, '7'); s.clear((18, 22), (33, 22))
    s.rect(25, 10, 26, 12, 'p'); s.rect(22, 14, 24, 15, 'p'); s.rect(28, 14, 30, 15, 'p'); s.px(23, 15, 'k'); s.px(29, 15, 'k')
    s.rect(22, 18, 30, 19, 'k'); s.px(23, 20, 'w'); s.px(29, 20, 'w')
    s.rect(13, 23, 38, 44, 'x'); s.rect(13, 23, 16, 44, 'k'); s.rect(18, 26, 33, 41, '6'); s.rect(24, 26, 27, 41, '7')
    s.rect(15, 43, 36, 46, 'o'); s.rect(15, 46, 36, 52, '7')
    for (y, ln) in ((25, 12), (33, 11)):
        s.rect(38, y, 38 + ln, y + 3, '6'); s.rect(46, y - 2, 50, y + 4, '7')
        s.rect(13 - ln, y, 13, y + 3, '6'); s.rect(1, y - 2, 5, y + 4, '7')
    s.rect(17, 53, 22, 58, 'x'); s.rect(29, 53, 34, 58, 'x')
    s.outline(); return s


def possessed(im):
    """被马贼附身的保安：整个人泛青，眼睛发红"""
    out = im.copy(); px_ = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g_, b_, a_ = px_[x, y]
            if a_ and (r, g_, b_) != (24, 14, 30):
                l = (r + g_ + b_) / 3; px_[x, y] = (int(l * 0.5), int(min(255, l * 0.9 + 30)), int(min(255, l * 0.85 + 40)), a_)
    return out


# ---------------- 僵尸八大等级里新加的四种 ----------------
def fei_zombie():
    """飞僵：官服破成条，衣摆飘起，脚下一团黑云"""
    s = Spr(28, 38)
    s.rect(9, 0, 18, 3, 'h'); s.rect(13, 0, 14, 0, 'r'); s.rect(8, 3, 19, 4, 'H')
    s.rect(9, 5, 18, 13, 'q'); s.rect(9, 5, 10, 12, 'Q'); s.clear((9, 13), (18, 13))
    s.rect(14, 8, 16, 8, 'r'); s.px(16, 8, 'k'); s.rect(13, 11, 17, 11, 'k'); s.px(14, 12, 'w'); s.px(16, 12, 'w')
    s.rect(7, 14, 20, 24, 'n'); s.rect(7, 14, 8, 24, 'N'); s.rect(12, 16, 15, 20, 'o')
    for x in range(5, 23): s.rect(x, 25, x, 25 + (x * 7) % 6, 'n' if x % 2 else 'N')    # 飘起的破衣摆
    s.rect(20, 15, 26, 17, 'n'); s.rect(26, 15, 27, 17, 'q')
    s.rect(3, 15, 7, 17, 'n'); s.rect(1, 15, 3, 17, 'q')
    for x in range(6, 22): s.rect(x, 33 + (x % 3 == 0), x, 36, 'h' if x % 4 else 'H')     # 黑云
    s.outline(); return s


def you_zombie():
    """游尸：灰扑扑的破长衫，斗笠歪着，身子半透明，四处游荡"""
    s = Spr(24, 36)
    s.rect(4, 3, 19, 4, 'A'); s.rect(7, 0, 16, 3, 'a'); s.px(17, 1, 'a')
    s.rect(8, 5, 15, 13, 'K'); s.rect(8, 5, 9, 12, 'h'); s.clear((8, 13), (15, 13))
    s.px(12, 8, 'W'); s.px(14, 8, 'W'); s.rect(12, 11, 14, 11, 'k')
    s.rect(6, 14, 17, 28, 'A'); s.rect(6, 14, 7, 28, 'h'); s.rect(11, 14, 12, 28, 'a')
    for x in range(6, 18): s.rect(x, 29, x, 29 + (x * 3) % 3, 'A')
    s.rect(17, 16, 21, 18, 'A'); s.rect(21, 16, 22, 18, 'K')
    s.rect(8, 32, 10, 34, 'h'); s.rect(13, 32, 15, 34, 'h')
    s.outline(); return s


def fu_zombie():
    """伏尸：从地脉里钻出来，满身泥土，脸埋在土里只露出眼睛"""
    s = Spr(26, 34)
    s.rect(8, 2, 17, 12, 'b'); s.rect(8, 2, 10, 11, 'B'); s.clear((8, 12), (17, 12))
    s.rect(13, 6, 15, 6, 'j'); s.px(15, 6, 'k'); s.rect(12, 9, 16, 9, 'B')
    for (x, y) in ((9, 3), (16, 4), (11, 10)): s.px(x, y, 'L')
    s.rect(6, 13, 19, 25, 'B'); s.rect(6, 13, 7, 25, 'k'); s.rect(10, 15, 15, 22, 'b')
    for (x, y) in ((8, 16), (17, 18), (12, 24), (9, 21)): s.px(x, y, 'L')
    s.rect(19, 14, 24, 16, 'B'); s.rect(24, 13, 25, 17, 'b')
    s.rect(2, 25, 23, 31, 'B'); s.rect(4, 24, 21, 25, 'b')      # 下半身还埋在土里
    for x in range(3, 23, 3): s.px(x, 27 + x % 2, 'L'); s.px(x + 1, 30, 'b')
    s.outline(); return s


def bugu():
    """不化骨：只剩一副骨头，骨头硬得发黄发亮，眼窝里两点绿火，套着破官帽"""
    s = Spr(28, 40)
    s.rect(9, 0, 18, 3, 'h'); s.rect(8, 3, 19, 4, 'H'); s.rect(13, 0, 14, 0, 'r')
    s.rect(9, 5, 18, 13, 'p'); s.rect(9, 5, 10, 12, 'o'); s.clear((9, 13), (18, 13))
    s.rect(12, 7, 13, 8, 'k'); s.rect(15, 7, 16, 8, 'k'); s.px(12, 7, 'j'); s.px(15, 7, 'j')
    s.px(14, 10, 'k'); for_teeth = [s.px(x, 12, 'k') for x in (11, 13, 15, 17)]
    s.rect(13, 14, 14, 30, 'p')                                                     # 脊骨
    for y in (16, 19, 22, 25):
        s.rect(8, y, 19, y, 'p'); s.px(8, y + 1, 'o'); s.px(19, y + 1, 'o')         # 肋骨
    s.rect(9, 27, 18, 29, 'o')
    s.rect(19, 16, 26, 17, 'p'); s.rect(25, 15, 27, 18, 'o')
    s.rect(2, 16, 8, 17, 'p'); s.rect(1, 15, 2, 18, 'o')
    s.rect(10, 30, 11, 37, 'p'); s.rect(16, 30, 17, 37, 'p'); s.rect(9, 37, 12, 38, 'o'); s.rect(15, 37, 18, 38, 'o')
    s.outline(); return s


# ---------------- 20 波版新增：人物和怪 ----------------
def wencai():
    """文才：圆脸、中分头、灰蓝短褂，腰上挂着引魂铃"""
    s = Spr(22, 32)
    s.rect(6, 1, 15, 4, 'h'); s.px(10, 1, 's')
    s.rect(6, 4, 15, 12, 's'); s.rect(6, 4, 7, 11, 'S'); s.clear((6, 12), (15, 12))
    s.px(11, 7, 'k'); s.px(14, 7, 'k'); s.rect(11, 10, 14, 10, 'k'); s.px(15, 9, 's')
    s.rect(5, 13, 16, 23, 'C'); s.rect(5, 13, 6, 23, 'n'); s.rect(10, 13, 11, 23, 'w')
    s.rect(15, 18, 17, 21, 'o'); s.px(16, 22, 'O')
    s.rect(16, 14, 19, 16, 'C'); s.rect(19, 14, 20, 16, 's')
    s.rect(6, 24, 15, 28, 'h'); s.rect(6, 29, 9, 30, 'k'); s.rect(12, 29, 15, 30, 'k')
    s.outline(); return s


def xiaofeng():
    """王小凤：被放过的女鬼，白衣素裙，黑发垂肩，脸色青白但神情温和"""
    s = Spr(22, 32)
    s.rect(6, 0, 15, 3, 'h'); s.rect(5, 3, 7, 15, 'h'); s.rect(14, 3, 16, 12, 'h')
    s.rect(8, 3, 14, 11, 'F'); s.rect(8, 3, 9, 10, 'K')
    s.px(11, 6, 'k'); s.px(13, 6, 'k'); s.rect(11, 9, 13, 9, 'P')
    s.rect(6, 12, 15, 24, 'W'); s.rect(6, 12, 7, 24, 'G'); s.rect(10, 12, 11, 15, 'P')
    for x in range(6, 16): s.rect(x, 25, x, 25 + (x * 3) % 4, 'W')
    s.rect(15, 14, 18, 16, 'W'); s.rect(18, 14, 19, 16, 'F')
    s.outline(); return s


def royal_zombie():
    """皇族僵尸：明黄龙袍、红顶朝冠、朝珠，青脸长指甲（金墨棺里出来的）"""
    s = Spr(30, 40)
    s.rect(9, 0, 20, 3, 'h'); s.rect(13, 0, 16, 0, 'r'); s.rect(14, -0, 15, 0, 'o'); s.rect(8, 3, 21, 4, 'H')
    s.rect(10, 5, 19, 14, 'z'); s.rect(10, 5, 11, 13, 'Z'); s.clear((10, 14), (19, 14))
    s.rect(15, 8, 17, 8, 'r'); s.px(17, 8, 'k'); s.rect(14, 11, 18, 11, 'k'); s.px(15, 12, 'w'); s.px(17, 12, 'w')
    s.rect(7, 15, 22, 33, 'y'); s.rect(7, 15, 9, 33, 'Y'); s.rect(14, 15, 15, 33, 'O')
    for y in range(16, 30, 3): s.px(12, y, 'r'); s.px(17 + (y % 2), y, 'r')
    for (x, y) in ((10, 20), (19, 24), (11, 28)): s.px(x, y, 'n'); s.px(x + 1, y + 1, 'n')
    s.rect(22, 16, 28, 19, 'y'); s.rect(28, 16, 29, 19, 'z')
    s.rect(9, 34, 12, 38, 'k'); s.rect(17, 34, 20, 38, 'k')
    s.outline(); return s


def ronin():
    """东洋浪人：散乱发髻、灰色和服、腰挎武士刀，一脸凶相"""
    s = Spr(28, 36)
    s.rect(11, 0, 15, 2, 'h'); s.rect(9, 2, 17, 4, 'h')
    s.rect(9, 4, 17, 12, 's'); s.rect(9, 4, 10, 11, 'S'); s.clear((9, 12), (17, 12))
    s.rect(13, 7, 15, 7, 'k'); s.rect(12, 6, 16, 6, 'h'); s.rect(12, 10, 16, 10, 'h'); s.rect(12, 11, 16, 11, 'h')
    s.rect(7, 13, 19, 24, 'A'); s.rect(7, 13, 8, 24, 'h'); s.rect(12, 13, 14, 18, 's'); s.rect(7, 20, 19, 21, 'h')
    s.rect(6, 25, 20, 31, 'h'); s.rect(6, 25, 7, 31, 'k'); s.rect(12, 26, 13, 31, 'k')
    s.rect(4, 21, 22, 21, 'B'); s.rect(4, 20, 5, 22, 'o')
    s.rect(19, 14, 23, 16, 'A'); s.rect(23, 14, 24, 16, 's'); s.rect(24, 4, 25, 15, 'W'); s.rect(23, 15, 26, 16, 'o')
    s.rect(8, 32, 11, 33, 'B'); s.rect(15, 32, 18, 33, 'B')
    s.outline(); return s


def jiangtou_corpse():
    """降头尸：民国长衫，脸上爬满黑色降头纹，眼睛翻白"""
    s = Spr(24, 36)
    s.rect(8, 1, 15, 3, 'h')
    s.rect(8, 4, 15, 13, 'q'); s.rect(8, 4, 9, 12, 'Q'); s.clear((8, 13), (15, 13))
    s.rect(12, 7, 14, 7, 'W'); for_marks = [s.px(x, y, 'k') for (x, y) in ((10, 5), (11, 9), (14, 10), (9, 11), (15, 5))]
    s.rect(12, 11, 14, 11, 'k')
    s.rect(6, 14, 17, 31, '8'); s.rect(6, 14, 7, 31, '9'); s.rect(11, 14, 12, 31, '9')
    for y in (16, 19, 22): s.px(14, y, 'o')
    s.rect(17, 15, 22, 17, '8'); s.rect(22, 15, 23, 17, 'q')
    s.rect(8, 32, 10, 34, 'k'); s.rect(13, 32, 15, 34, 'k')
    s.outline(); return s


def tulong():
    """屠龙：九叔的师弟，紫黑道袍，摇着赶尸铃，表情奸滑"""
    s = Spr(26, 36)
    s.rect(9, 0, 15, 4, 'h'); s.rect(8, 4, 16, 5, 'H'); s.rect(11, 1, 13, 2, 'v')
    s.rect(8, 6, 16, 15, 's'); s.rect(8, 6, 9, 14, 'S'); s.clear((8, 15), (16, 15))
    s.rect(12, 9, 13, 9, 'k'); s.rect(15, 9, 16, 9, 'k'); s.rect(12, 12, 16, 12, 'k'); s.px(11, 13, 'h'); s.px(17, 13, 'h')
    s.rect(7, 16, 17, 30, 'v'); s.rect(7, 16, 8, 30, 'V'); s.rect(6, 25, 18, 30, 'v'); s.rect(10, 16, 14, 16, 'o')
    s.rect(16, 17, 20, 19, 'v'); s.rect(20, 15, 21, 17, 's'); s.rect(21, 11, 24, 15, 'o'); s.px(22, 16, 'O')
    s.rect(4, 17, 7, 22, 'V'); s.rect(4, 22, 5, 23, 's')
    s.rect(8, 31, 11, 33, 'h'); s.rect(13, 31, 16, 33, 'h')
    s.outline(); return s


def old_priest_vampire():
    """老神父（吸血鬼）：黑袍白领，胸口插着断掉的十字架，青白脸、红眼、獠牙"""
    s = Spr(28, 40)
    s.rect(9, 1, 18, 3, 'a')
    s.rect(9, 4, 18, 13, 'W'); s.rect(9, 4, 10, 12, 'G'); s.clear((9, 13), (18, 13))
    s.rect(14, 7, 16, 7, 'r'); s.px(16, 7, 'k'); s.rect(13, 10, 17, 10, 'k'); s.px(14, 11, 'w'); s.px(16, 11, 'w')
    s.rect(6, 14, 21, 34, 'h'); s.rect(6, 14, 8, 34, 'k'); s.rect(12, 14, 15, 15, 'w')
    s.rect(13, 18, 14, 27, 'B'); s.rect(10, 20, 17, 21, 'B'); s.px(13, 26, '6'); s.px(14, 28, '6')
    s.rect(21, 15, 26, 18, 'h'); s.rect(26, 15, 27, 18, 'W')
    s.rect(2, 15, 6, 18, 'h'); s.rect(1, 15, 2, 18, 'W')
    s.rect(9, 35, 12, 38, 'k'); s.rect(15, 35, 18, 38, 'k')
    s.outline(); return s


def wu_priest():
    """吴神父：从梵蒂冈来的神父，戴礼帽、黑袍、胸前金十字，拿着圣水瓶"""
    s = Spr(26, 38)
    s.rect(6, 4, 19, 5, 'h'); s.rect(9, 0, 16, 4, 'h')
    s.rect(9, 6, 16, 14, 's'); s.rect(9, 6, 10, 13, 'S'); s.clear((9, 14), (16, 14))
    s.px(13, 9, 'k'); s.px(15, 9, 'k'); s.rect(12, 12, 15, 12, 'a'); s.rect(12, 13, 15, 14, 'a')
    s.rect(7, 15, 18, 33, 'h'); s.rect(7, 15, 8, 33, 'k'); s.rect(11, 15, 14, 16, 'w')
    s.rect(12, 18, 13, 24, 'o'); s.rect(10, 20, 15, 21, 'o')
    s.rect(18, 16, 22, 18, 'h'); s.rect(22, 13, 24, 18, 'c'); s.px(23, 12, 'w')
    s.rect(9, 34, 12, 36, 'k'); s.rect(13, 34, 16, 36, 'k')
    s.outline(); return s


def wax_corpse():
    """血蜡尸：被封进腊味坊、浑身裹着暗红血蜡的尸体，蜡一路往下滴"""
    s = Spr(26, 36)
    s.rect(8, 2, 17, 13, '6'); s.rect(8, 2, 10, 12, '7'); s.clear((8, 13), (17, 13))
    s.rect(13, 6, 15, 6, 'p'); s.px(15, 6, 'k'); s.rect(12, 10, 16, 10, '7')
    s.rect(6, 14, 19, 29, '6'); s.rect(6, 14, 8, 29, '7'); s.rect(11, 16, 15, 24, 'P')
    for x in (7, 10, 14, 18): s.rect(x, 30, x, 30 + x % 3, '6')
    s.rect(19, 15, 24, 18, '6'); s.rect(24, 15, 25, 19, '7'); s.px(25, 21, '6')
    s.rect(8, 30, 11, 33, '7'); s.rect(14, 30, 17, 33, '7')
    s.outline(); return s


def qiannian():
    """千年僵尸王：干瘪的古尸，长发披散，身上是锈烂的古代铠甲，眼睛两点红光"""
    s = Spr(32, 44)
    s.rect(10, 1, 21, 3, 'a')
    for x in list(range(7, 11)) + list(range(21, 25)): s.rect(x, 3, x, 18 + (x * 5) % 6, 'a')
    s.rect(11, 3, 20, 14, 'b'); s.rect(11, 3, 12, 13, 'B')
    s.rect(15, 7, 16, 8, 'r'); s.rect(18, 7, 19, 8, 'r'); s.rect(14, 11, 19, 12, 'k'); s.px(15, 12, 'w'); s.px(18, 12, 'w')
    s.rect(8, 17, 23, 34, '5'); s.rect(8, 17, 10, 34, 'k')
    for y in range(18, 34, 3): s.rect(11, y, 22, y, '3')
    s.rect(7, 16, 24, 18, 'A'); s.rect(13, 20, 18, 26, 'A')
    s.rect(23, 18, 29, 21, '5'); s.rect(29, 17, 31, 22, 'b'); s.px(31, 23, 'w')
    s.rect(3, 18, 8, 21, '5'); s.rect(1, 18, 3, 22, 'b')
    s.rect(10, 35, 14, 41, '5'); s.rect(17, 35, 21, 41, '5'); s.rect(10, 41, 14, 42, 'k'); s.rect(17, 41, 21, 42, 'k')
    s.outline(); return s


def shi_shaojian():
    """石少坚：油头粉面的少爷，长衫马褂，手里摇把扇子，学了旁门左道"""
    s = Spr(24, 36)
    s.rect(7, 1, 16, 4, 'h'); s.px(15, 2, 'H')
    s.rect(7, 4, 16, 13, 's'); s.rect(7, 4, 8, 12, 'S'); s.clear((7, 13), (16, 13))
    s.px(12, 7, 'k'); s.px(15, 7, 'k'); s.rect(12, 10, 15, 10, 'r'); s.px(16, 9, 's')
    s.rect(6, 14, 17, 22, 'm'); s.rect(6, 14, 7, 22, 'M'); s.rect(11, 14, 12, 22, 'o')
    s.rect(6, 23, 17, 31, 'c'); s.rect(6, 23, 7, 31, 'C')
    s.rect(17, 15, 20, 17, 'm'); s.rect(20, 11, 23, 16, 'w'); s.rect(21, 12, 22, 15, 'v')
    s.rect(8, 32, 10, 34, 'k'); s.rect(13, 32, 15, 34, 'k')
    s.outline(); return s


def yaoshi():
    """妖尸（石少坚尸变）：补过的尸体缝着线，皮肤发青紫，身上带着电光"""
    s = Spr(28, 38)
    s.rect(9, 1, 18, 4, 'h')
    s.rect(9, 4, 18, 13, 'v'); s.rect(9, 4, 10, 12, 'V'); s.clear((9, 13), (18, 13))
    s.rect(13, 7, 14, 7, 'c'); s.rect(16, 7, 17, 7, 'c'); s.rect(13, 10, 17, 10, 'k'); s.px(14, 11, 'w')
    for y in range(5, 13, 2): s.px(11, y, 'k')                                       # 缝线
    s.rect(7, 14, 20, 29, 'm'); s.rect(7, 14, 8, 29, 'M'); s.rect(13, 14, 14, 29, 'k')
    for y in range(15, 29, 2): s.px(12, y, 'w'); s.px(15, y, 'w')
    s.rect(20, 15, 25, 18, 'v'); s.rect(25, 15, 26, 18, 'c')
    s.rect(3, 15, 7, 18, 'v'); s.rect(2, 15, 3, 18, 'c')
    for (x, y) in ((1, 10), (26, 9), (4, 24), (24, 26)): s.px(x, y, 'g'); s.px(x + 1, y + 1, 'c'); s.px(x, y + 2, 'g')
    s.rect(9, 30, 12, 35, 'c'); s.rect(15, 30, 18, 35, 'c'); s.rect(9, 30, 12, 31, 'C'); s.rect(15, 30, 18, 31, 'C')
    s.outline(); return s


def shijian():
    """石坚：九叔的大师兄，一字眉、白须，红色八卦道袍，掌心冒着雷光"""
    s = Spr(28, 40)
    s.rect(10, 0, 17, 4, 'h'); s.rect(9, 4, 18, 5, 'H'); s.rect(12, 1, 15, 2, 'o')
    s.rect(9, 6, 18, 15, 's'); s.rect(9, 6, 10, 14, 'S'); s.clear((9, 15), (18, 15))
    s.rect(12, 8, 17, 8, 'k'); s.px(13, 9, 'k'); s.px(16, 9, 'k'); s.rect(12, 12, 17, 15, 'a'); s.rect(13, 16, 16, 17, 'a')
    s.rect(7, 16, 20, 33, 'r'); s.rect(7, 16, 8, 33, 'X'); s.rect(6, 28, 21, 33, 'r'); s.rect(12, 16, 15, 17, 'w')
    s.rect(11, 21, 16, 26, 'k'); s.rect(12, 22, 15, 25, 'o'); s.px(13, 23, 'k'); s.px(14, 24, 'w')
    s.rect(20, 17, 24, 19, 'r'); s.rect(24, 16, 26, 19, 's')
    for (x, y) in ((26, 13), (27, 15), (25, 12), (27, 11)): s.px(x, y, 'c')
    s.rect(3, 17, 7, 20, 'r'); s.rect(2, 20, 3, 21, 's')
    s.rect(9, 34, 12, 37, 'k'); s.rect(15, 34, 18, 37, 'k')
    s.outline(); return s


def recolor(im, f):
    out = im.copy(); px_ = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g_, b_, a_ = px_[x, y]
            if a_ and (r, g_, b_) != (24, 14, 30): px_[x, y] = f(r, g_, b_) + (a_,)
    return out
