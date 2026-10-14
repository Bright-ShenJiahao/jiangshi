# 序章用的人物与道具（原创像素图）
# 需先 exec sprites.py 的定义（Spr / PAL）


def afu(red=False):
    """阿福：胖徒弟，光头冲天辫，灰蓝短褂。red=True 憋气脸红鼓腮"""
    s = Spr(24, 32)
    skin, sk2 = ('P', 'e') if red else ('s', 'S')
    # 冲天辫
    s.rect(11, 0, 12, 3, 'h'); s.px(10, 1, 'h'); s.px(13, 4, 'r')
    # head (round, big)
    s.rect(6, 4, 17, 15, skin); s.clear((6, 4), (17, 4), (6, 15), (17, 15))
    s.rect(6, 5, 7, 14, sk2)
    s.px(11, 8, 'k'); s.px(15, 8, 'k')          # eyes
    if red:
        s.rect(10, 8, 11, 8, 'k'); s.rect(14, 8, 15, 8, 'k')  # squeezed shut
        s.rect(17, 10, 18, 13, skin)             # puffed cheek
        s.rect(13, 12, 14, 12, 'k')
        s.px(5, 6, 'c'); s.px(19, 5, 'c'); s.px(19, 6, 'C')  # sweat
    else:
        s.rect(12, 12, 15, 12, 'k'); s.px(13, 13, 'r')       # grin
        s.px(16, 11, 'R')                                    # cheek
    s.px(18, 10, skin)
    # fat body, grey-blue jacket, sash
    s.rect(4, 16, 19, 25, 'c'); s.rect(3, 19, 20, 24, 'c')
    s.rect(3, 19, 5, 25, 'C'); s.rect(4, 16, 6, 18, 'C')
    s.rect(11, 16, 12, 25, 'C')
    s.rect(3, 23, 20, 23, 'B')
    s.rect(13, 18, 17, 21, 'C')  # belly fold
    # arms
    s.rect(18, 17, 21, 21, 'c'); s.rect(20, 21, 22, 23, skin if not red else 's')
    s.rect(1, 17, 4, 21, 'C'); s.rect(1, 21, 3, 23, 's')
    # trousers + shoes
    s.rect(5, 26, 10, 28, 'h'); s.rect(13, 26, 18, 28, 'h')
    s.rect(4, 29, 10, 30, 'k'); s.rect(13, 29, 19, 30, 'k')
    s.rect(5, 29, 9, 29, 'w'); s.rect(14, 29, 18, 29, 'w')
    s.outline()
    return s


def ren():
    """任老爷：瓜皮帽红顶珠、八字胡、绛紫团花马褂、长衫"""
    s = Spr(24, 36)
    s.rect(11, 0, 12, 1, 'r')                    # 顶珠
    s.rect(7, 2, 16, 5, 'h'); s.clear((7, 2), (16, 2)); s.rect(7, 5, 16, 5, 'H')
    s.rect(11, 2, 12, 5, 'H')
    s.rect(7, 6, 16, 15, 's'); s.clear((7, 15), (16, 15))
    s.rect(7, 6, 8, 14, 'S')
    s.px(11, 9, 'k'); s.px(14, 9, 'k'); s.rect(10, 8, 11, 8, 'h'); s.rect(14, 8, 15, 8, 'h')
    s.px(17, 10, 's')
    # 八字胡
    s.rect(11, 12, 15, 12, 'k'); s.px(10, 13, 'k'); s.px(16, 13, 'k'); s.px(9, 14, 'k'); s.px(17, 14, 'k')
    s.rect(12, 14, 14, 14, 'S')
    # 马褂
    s.rect(5, 16, 18, 24, 'm'); s.rect(5, 16, 7, 24, 'M')
    s.rect(11, 16, 12, 24, 'o')
    for y in (18, 20, 22): s.px(11, y, 'O')
    s.rect(14, 18, 16, 20, 'o'); s.px(15, 19, 'm')   # 团花
    s.rect(4, 20, 4, 24, 'M')
    # 长衫 below
    s.rect(6, 25, 17, 32, 'n'); s.rect(6, 25, 7, 32, 'N')
    s.rect(11, 26, 11, 32, 'N')
    # sleeves, hands clasped (拱手)
    s.rect(15, 17, 20, 21, 'm'); s.rect(19, 21, 21, 23, 's')
    s.rect(3, 17, 6, 22, 'M'); s.rect(3, 22, 5, 23, 's')
    # gold fan
    s.rect(20, 18, 22, 20, 'o')
    s.rect(7, 33, 10, 34, 'k'); s.rect(13, 33, 16, 34, 'k')
    s.outline()
    return s


def coffin():
    """侧面棺材（无盖），头大尾小"""
    s = Spr(46, 18)
    for x in range(46):
        top = 4 - (x * 3) // 45            # tail lower, head higher
        s.rect(x, top + 2, x, 15, 'X')
    s.rect(0, 13, 45, 15, 'M')
    s.rect(38, 1, 45, 15, 'm'); s.rect(42, 3, 44, 13, 'o')  # head plate
    s.rect(43, 6, 43, 10, 'r')
    s.rect(1, 6, 37, 6, 'm')
    s.rect(2, 16, 4, 17, 'h'); s.rect(36, 16, 38, 17, 'h')
    s.outline()
    return s


def coffin_lid():
    s = Spr(48, 6)
    s.rect(0, 1, 47, 4, 'X'); s.rect(0, 1, 47, 1, 'm'); s.rect(40, 0, 47, 5, 'm')
    s.rect(18, 2, 21, 3, 'p'); s.px(19, 2, 'r'); s.px(20, 3, 'r')  # 封条符
    s.outline()
    return s


def rooster():
    s = Spr(18, 18)
    s.rect(11, 0, 13, 2, 'r'); s.rect(10, 3, 14, 7, 'w'); s.px(13, 4, 'k')
    s.rect(15, 5, 16, 5, 'o'); s.rect(13, 7, 13, 8, 'r')
    s.rect(4, 7, 13, 13, 'w'); s.rect(4, 9, 8, 12, 'W')
    s.rect(1, 3, 4, 8, 'f'); s.rect(0, 2, 2, 5, 'j'); s.px(3, 9, 'f')
    s.rect(8, 14, 8, 16, 'o'); s.rect(11, 14, 11, 16, 'o'); s.rect(7, 16, 12, 16, 'o')
    s.outline()
    return s
