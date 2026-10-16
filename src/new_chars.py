# 第三批新角色（原创像素图）：任老爷僵尸、四目道长、赶尸尸体、信徒/血仆、芭蕉精、秋生骑车+后座女鬼、蜻蜓
# 需先 exec sprites.py（Spr / PAL）
PAL.update({'D': (40, 110, 70), 'l': (90, 170, 90), 'u': (150, 150, 165), 'U': (90, 90, 105)})
PAL.setdefault('P', (236, 112, 104))


def ren_zombie():
    """任老爷尸变：瓜皮帽红顶珠、地主团花大马褂、长衫，脸青灰，双臂伸直"""
    s = Spr(30, 40)
    s.rect(12, 0, 13, 1, 'r')
    s.rect(8, 2, 17, 5, 'h'); s.clear((8, 2), (17, 2)); s.rect(8, 5, 17, 5, 'H'); s.rect(12, 2, 13, 5, 'H')
    s.rect(8, 6, 17, 15, 'z'); s.clear((8, 15), (17, 15)); s.rect(8, 6, 9, 14, 'Z')
    s.rect(14, 9, 16, 10, 'E'); s.px(15, 10, 'k')                         # 死鱼眼
    s.rect(12, 12, 16, 12, 'k'); s.px(11, 13, 'k'); s.px(17, 13, 'k')      # 八字胡
    s.px(14, 14, 'w'); s.px(16, 14, 'w')                                   # 獠牙
    s.px(18, 10, 'z')
    # 大马褂：宽，深紫，金色团花，盘扣
    s.rect(4, 16, 21, 27, 'M'); s.rect(5, 16, 20, 26, 'm'); s.rect(4, 16, 6, 27, 'M')
    s.rect(12, 16, 13, 27, 'o')
    for y in (18, 21, 24): s.px(12, y, 'O'); s.px(13, y, 'O')
    for cx, cy in ((8, 19), (17, 19), (8, 24), (17, 24)):
        s.rect(cx - 1, cy - 1, cx + 1, cy + 1, 'o'); s.px(cx, cy, 'm')
    # 长衫
    s.rect(7, 28, 18, 35, 'n'); s.rect(7, 28, 8, 35, 'N'); s.rect(12, 29, 12, 35, 'N')
    # 双臂伸直（宽袖）+ 长指甲
    s.rect(18, 17, 27, 20, 'm'); s.rect(18, 20, 27, 20, 'M'); s.rect(26, 17, 27, 20, 'M')
    s.rect(27, 18, 29, 20, 'z'); s.px(29, 21, 'k')
    s.rect(1, 17, 5, 20, 'M')
    s.rect(8, 36, 11, 38, 'k'); s.rect(14, 36, 17, 38, 'k')
    s.outline()
    return s


def simu():
    """四目道长：圆眼镜、黄道袍、道冠，一手摇铃"""
    s = Spr(26, 36)
    s.rect(9, 0, 15, 4, 'h'); s.rect(8, 4, 16, 5, 'H'); s.rect(11, 1, 13, 2, 'o')
    s.rect(8, 6, 16, 15, 's'); s.rect(8, 6, 9, 14, 'S'); s.clear((8, 15), (16, 15))
    # 圆眼镜（四目）
    for cx in (12, 15):
        s.px(cx - 1, 9, 'k'); s.px(cx + 1, 9, 'k'); s.px(cx, 8, 'k'); s.px(cx, 10, 'k'); s.px(cx, 9, 'c')
    s.px(13, 9, 'k')
    s.rect(12, 13, 15, 13, 'S'); s.px(13, 14, 'h'); s.px(14, 14, 'h')
    s.rect(7, 16, 17, 30, 'y'); s.rect(7, 16, 8, 30, 'Y'); s.rect(6, 25, 18, 30, 'y')
    s.rect(10, 16, 14, 16, 'w'); s.rect(7, 22, 17, 22, 'r')
    s.rect(10, 18, 11, 19, 'k'); s.px(11, 19, 'w')
    # 摇铃的手
    s.rect(16, 17, 20, 19, 'y'); s.rect(20, 15, 21, 17, 's')
    s.rect(21, 11, 24, 15, 'o'); s.rect(22, 10, 23, 10, 'O'); s.px(22, 16, 'O')
    s.rect(4, 17, 7, 22, 'Y'); s.rect(4, 22, 5, 23, 's')
    s.rect(8, 31, 11, 33, 'h'); s.rect(13, 31, 16, 33, 'h')
    s.outline()
    return s


def corpse():
    """四目赶的尸体：黑袍、斗笠、额头贴符"""
    s = Spr(24, 34)
    s.rect(3, 4, 20, 6, 'B'); s.rect(6, 1, 17, 4, 'b'); s.rect(9, 0, 14, 1, 'b')        # 斗笠
    s.rect(7, 7, 16, 15, 'z'); s.rect(7, 7, 8, 14, 'Z'); s.clear((7, 15), (16, 15))
    s.rect(11, 6, 13, 13, 'p'); s.px(12, 8, 'r'); s.px(12, 10, 'r'); s.px(12, 12, 'r')  # 符
    s.rect(6, 16, 17, 29, 'h'); s.rect(6, 16, 7, 29, 'k'); s.rect(9, 16, 14, 16, 'H')
    s.rect(16, 17, 22, 19, 'h'); s.rect(22, 18, 23, 19, 'z')
    s.rect(7, 30, 10, 32, 'k'); s.rect(13, 30, 16, 32, 'k')
    s.outline()
    return s


def believer(kneel=True, thrall=False):
    """教堂信徒：灰布衣、手里捧十字架；thrall=被转化的血仆（苍白、红眼、伸爪）"""
    if kneel:
        s = Spr(22, 26)
        s.rect(8, 2, 15, 9, 's'); s.rect(8, 1, 15, 3, 'h'); s.rect(8, 2, 9, 8, 'h')
        s.px(13, 6, 'k')
        s.rect(6, 10, 15, 19, 'u'); s.rect(6, 10, 7, 19, 'U')
        s.rect(14, 12, 17, 14, 'u'); s.rect(17, 10, 17, 15, 'O'); s.rect(16, 11, 18, 11, 'O')   # 捧十字架
        s.rect(4, 19, 16, 22, 'U'); s.rect(3, 22, 9, 23, 'k')                                   # 跪着
    else:
        s = Spr(22, 32)
        face, eye = ('W', 'r') if thrall else ('s', 'k')
        s.rect(7, 1, 14, 9, face); s.rect(7, 0, 14, 2, 'h'); s.rect(7, 1, 8, 8, 'h')
        s.px(12, 5, eye); s.px(14, 5, eye)
        if thrall: s.px(12, 8, 'w'); s.px(14, 8, 'w'); s.rect(11, 7, 14, 7, 'X')
        s.rect(6, 10, 15, 22, 'U' if thrall else 'u'); s.rect(6, 10, 7, 22, 'h')
        if thrall: s.px(9, 13, 'X'); s.px(10, 14, 'X')          # 颈上血痕
        s.rect(14, 11, 20, 13, 'U' if thrall else 'u'); s.rect(20, 11, 21, 13, face); s.px(21, 14, 'k')
        s.rect(7, 23, 10, 28, 'h'); s.rect(12, 23, 15, 28, 'h'); s.rect(6, 29, 10, 30, 'k'); s.rect(12, 29, 16, 30, 'k')
    s.outline()
    return s


def banana_ghost(true_form=False):
    """芭蕉精：妖艳女鬼（绿衣、长黑发插芭蕉叶、红唇）；true_form=现出芭蕉原形"""
    if true_form:
        s = Spr(28, 34)
        s.rect(12, 14, 15, 33, 'f'); s.rect(12, 14, 12, 33, 'D')
        for x0, y0, x1, y1 in ((2, 4, 13, 12), (14, 2, 26, 10), (4, 12, 12, 18), (15, 11, 25, 17)):
            s.rect(x0, y0, x1, y1, 'D'); s.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, 'l')
        s.rect(11, 18, 16, 21, 'D'); s.px(12, 19, 'r'); s.px(15, 19, 'r')     # 一对红眼
        s.outline(); return s
    s = Spr(24, 38)
    s.rect(6, 1, 17, 30, 'k'); s.rect(5, 6, 6, 28, 'k')                    # 长发
    s.rect(15, 0, 21, 4, 'D'); s.rect(16, 1, 20, 3, 'l')                   # 发间芭蕉叶
    s.rect(9, 3, 16, 12, 'W'); s.clear((9, 12), (16, 12))
    s.rect(12, 6, 13, 6, 'k'); s.px(15, 6, 'k'); s.px(12, 5, 'h'); s.px(15, 5, 'h')
    s.rect(12, 9, 14, 9, 'r'); s.px(15, 8, 'R')                            # 红唇、腮红
    s.rect(8, 13, 17, 31, 'D'); s.rect(9, 13, 16, 30, 'f'); s.rect(9, 13, 16, 14, 'l')
    s.rect(7, 26, 18, 34, 'f'); s.rect(7, 30, 18, 34, 'D')
    s.rect(16, 15, 21, 17, 'f'); s.rect(21, 13, 22, 16, 'W')                # 招手
    s.rect(11, 20, 14, 20, 'o')
    s.outline()
    return s


def qiusheng_bike(ghost=True):
    """秋生骑自行车，女鬼侧坐在后座、搂着他（朝左骑）"""
    s = Spr(52, 40)
    # 车轮
    for cx in (9, 41):
        for a in range(0, 360, 12):
            import math
            x = cx + round(7 * math.cos(math.radians(a))); y = 32 + round(7 * math.sin(math.radians(a)))
            s.px(x, y, 'k')
        s.rect(cx - 1, 31, cx + 1, 33, 'u')
    # 车架
    for t in range(0, 17):
        s.px(9 + t, 32 - t // 3, 'U'); s.px(25 + t, 27 + t // 3, 'U')
    s.rect(25, 26, 37, 26, 'U'); s.rect(36, 26, 44, 26, 'U')                 # 后座架
    s.rect(9, 20, 9, 31, 'U'); s.rect(6, 19, 11, 19, 'k')                    # 车把
    # 秋生（朝左，前倾骑车）
    s.rect(15, 3, 22, 10, 's'); s.rect(15, 2, 22, 4, 'k'); s.rect(20, 3, 22, 8, 'k')
    s.px(16, 6, 'k'); s.px(14, 7, 's')
    s.rect(15, 11, 24, 20, 'w'); s.rect(22, 11, 24, 20, 'g')
    s.rect(10, 13, 16, 15, 'w'); s.rect(9, 15, 10, 18, 's')                  # 手握车把
    s.rect(17, 21, 25, 24, 'N'); s.rect(16, 25, 18, 30, 'N'); s.rect(15, 30, 18, 31, 'k')
    if ghost:
        # 后座女鬼：白衣长发，侧坐，搂着秋生的腰
        s.rect(31, 6, 38, 25, 'k')
        s.rect(31, 9, 37, 15, 'W'); s.px(32, 12, 'k'); s.px(31, 13, 'W'); s.rect(32, 14, 33, 14, 'r')
        s.rect(30, 16, 39, 26, 'g'); s.rect(30, 16, 31, 26, 'W')
        s.rect(24, 18, 30, 19, 'g'); s.px(23, 18, 'W')                            # 搂腰的手
        s.rect(31, 27, 34, 33, 'g'); s.rect(30, 33, 34, 34, 'W')                 # 垂下的腿

    s.outline()
    return s


def dragonfly():
    s = Spr(9, 5)
    s.rect(1, 2, 7, 2, 'C'); s.px(8, 2, 'r')
    s.rect(4, 0, 4, 4, 'g'); s.rect(5, 0, 5, 4, 'g'); s.px(3, 1, 'g'); s.px(6, 3, 'g')
    return s


def opera_dan():
    """京剧旦角：点翠头面（珠花）、粉红褶子、白水袖"""
    s = Spr(22, 34)
    s.rect(6, 0, 15, 4, 'C'); s.px(5, 2, 'p'); s.px(16, 2, 'p'); s.px(8, 0, 'p'); s.px(13, 0, 'p'); s.rect(10, 1, 11, 2, 'r')
    s.rect(5, 3, 6, 12, 'k'); s.rect(15, 3, 16, 12, 'k')
    s.rect(7, 4, 14, 12, 'W'); s.rect(8, 7, 9, 9, 'P'); s.rect(12, 7, 13, 9, 'P')      # 胭脂
    s.px(9, 6, 'k'); s.px(12, 6, 'k'); s.rect(8, 5, 9, 5, 'k'); s.rect(12, 5, 13, 5, 'k'); s.rect(10, 10, 11, 10, 'r')
    s.rect(6, 13, 15, 27, 'P'); s.rect(6, 13, 7, 27, 'e'); s.rect(9, 13, 12, 13, 'w')
    for y in (16, 20, 24): s.px(10, y, 'o'); s.px(11, y + 1, 'o')
    s.rect(15, 14, 20, 16, 'P'); s.rect(18, 16, 21, 22, 'g'); s.rect(1, 15, 6, 17, 'P'); s.rect(0, 17, 3, 25, 'g')   # 水袖
    s.rect(5, 28, 16, 32, 'P'); s.rect(7, 33, 9, 33, 'k'); s.rect(12, 33, 14, 33, 'k')
    s.outline(); return s


def opera_jing():
    """京剧花脸：红黑脸谱、长髯口、蟒袍、背插靠旗"""
    s = Spr(26, 36)
    for x0, c in ((1, 'r'), (21, 'o')):
        s.rect(x0, 0, x0 + 3, 6, c); s.rect(x0 + 1, 6, x0 + 2, 14, 'k')                   # 靠旗
    s.rect(8, 0, 17, 4, 'o'); s.rect(9, 1, 16, 2, 'r'); s.px(12, 0, 'p')
    s.rect(8, 5, 17, 13, 'r'); s.rect(8, 5, 17, 6, 'k'); s.rect(10, 7, 11, 8, 'w'); s.rect(14, 7, 15, 8, 'w'); s.px(11, 8, 'k'); s.px(14, 8, 'k')
    s.rect(12, 9, 13, 11, 'k'); s.rect(9, 10, 10, 12, 'k'); s.rect(15, 10, 16, 12, 'k')
    s.rect(9, 13, 16, 20, 'k'); s.rect(10, 20, 15, 22, 'k')                                # 髯口
    s.rect(6, 14, 19, 29, 'f'); s.rect(6, 14, 8, 29, 'D'); s.rect(9, 23, 16, 24, 'o')
    for x, y in ((8, 17), (17, 18), (7, 26), (17, 26)): s.px(x, y, 'o')
    s.rect(19, 15, 24, 17, 'f'); s.rect(23, 11, 24, 15, 's'); s.rect(1, 15, 6, 17, 'f'); s.rect(1, 17, 2, 19, 's')
    s.rect(7, 30, 11, 33, 'k'); s.rect(14, 30, 18, 33, 'k'); s.rect(7, 34, 11, 35, 'w'); s.rect(14, 34, 18, 35, 'w')
    s.outline(); return s


def qiusheng_bike_bride():
    """同 qiusheng_bike，但后座女鬼穿红嫁衣、戴红盖头般的头饰"""
    s = qiusheng_bike()
    for y in range(s.h):
        for x in range(28, 42):
            c = s.g[y][x]
            if c == 'g': s.g[y][x] = 'o' if (x * 3 + y * 5) % 17 == 0 else 'r'
    for x in range(30, 40):
        if s.g[16 - 0][x] in ('r', 'o'): s.g[16][x] = 'o'
    s.rect(31, 5, 38, 7, 'R'); s.px(34, 4, 'o'); s.px(36, 4, 'o')                         # 凤冠头饰
    s.rect(24, 18, 29, 19, 'r'); s.px(23, 18, 'W')
    s.outline(); return s


def wuchang(white=True):
    """黑白无常：高帽、长舌（白）、锁魂链、哭丧棒"""
    s = Spr(26, 48)
    hat, robe, shade, face = ('W', 'g', 'G', 'W') if white else ('k', 'h', 'k', 'E')
    s.rect(8, 0, 15, 15, hat); s.rect(7, 13, 16, 15, hat); s.rect(8, 0, 9, 15, 'G' if white else 'H')
    for y in (3, 6, 9, 12): s.rect(11, y, 12, y, 'r' if white else 'o')            # 帽上字（示意）
    s.rect(8, 16, 15, 25, face); s.clear((8, 25), (15, 25))
    s.rect(10, 19, 10, 19, 'k'); s.rect(13, 19, 13, 19, 'k')
    if white: s.rect(11, 23, 12, 30, 'r'); s.px(11, 31, 'R')                          # 长舌
    else: s.rect(10, 23, 13, 23, 'k')
    s.rect(6, 26, 17, 43, robe); s.rect(6, 26, 8, 43, shade); s.rect(5, 38, 18, 44, robe)
    s.rect(9, 26, 14, 26, 'k' if white else 'G')
    s.rect(17, 28, 21, 30, robe); s.rect(21, 27, 22, 29, face)                      # 前手
    for i in range(6): s.px(22 + (i % 2), 30 + i * 2, 'u'); s.px(23 - (i % 2), 31 + i * 2, 'U')   # 锁魂链
    s.rect(2, 28, 6, 30, robe); s.rect(1, 22, 2, 41, 'B' if white else 'b'); s.rect(0, 20, 3, 23, 'w')  # 哭丧棒
    s.outline()
    return s
