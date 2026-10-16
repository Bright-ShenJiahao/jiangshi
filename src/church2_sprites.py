# 教堂后院新增：西洋棺材、吸血鬼新娘、狼人、吸血鬼小怪
PAL.update({'1': (46, 42, 50), '2': (78, 74, 88), '3': (206, 210, 220), '4': (132, 138, 154), '5': (122, 24, 46), '6': (112, 98, 88), '7': (66, 56, 54), '8': (156, 140, 122), 'i': (244, 238, 226)})


def _hexcoffin(s, ox, oy, fill='1', hi='2', rim='4', cross=True, hollow=False):
    """六边形西洋棺（上宽下窄）：宽 20 高 40，银边；hollow=打开的棺（内衬红绒）"""
    def hw(y):
        return 3.5 + y / 10 * 6.5 if y < 10 else 10 - (y - 10) / 29 * 5
    for y in range(40):
        h = hw(y)
        x0, x1 = int(round(9.5 - h)), int(round(9.5 + h))
        for x in range(x0, x1 + 1):
            c = fill
            if x <= x0 + 1: c = hi
            if hollow and x0 + 3 <= x <= x1 - 3 and 4 <= y <= 36: c = '5' if (x + y) % 5 else '7'
            s.px(ox + x, oy + y, c)
        if not hollow:
            ix0, ix1 = x0 + 2, x1 - 2
            if 2 <= y <= 37:
                s.px(ox + ix0, oy + y, rim); s.px(ox + ix1, oy + y, rim)
    if not hollow:
        for x in range(5, 15): s.px(ox + x, oy + 2, rim) if 0 else None
        for x in range(int(round(9.5 - hw(2))) + 2, int(round(9.5 + hw(2))) - 1): s.px(ox + x, oy + 2, rim)
        for x in range(int(round(9.5 - hw(37))) + 2, int(round(9.5 + hw(37))) - 1): s.px(ox + x, oy + 37, rim)
    if cross and not hollow:
        for y in range(7, 21): s.px(ox + 9, oy + y, '3'); s.px(ox + 10, oy + y, '3')
        for x in range(6, 14): s.px(ox + x, oy + 11, '3'); s.px(ox + x, oy + 12, '3')


def coffin_w(open_=False):
    if not open_:
        s = Spr(20, 40); _hexcoffin(s, 0, 0); s.outline(); return s
    s = Spr(34, 54)
    _hexcoffin(s, 0, 0, hollow=True)
    _hexcoffin(s, 13, 14)           # 推开的棺盖
    s.outline(); return s


def bride():
    s = Spr(28, 44)
    s.rect(7, 1, 20, 9, 'k'); s.rect(6, 3, 7, 24, 'k'); s.rect(20, 3, 21, 24, 'k')           # 黑长发
    s.rect(9, 3, 18, 11, 'W'); s.rect(9, 3, 10, 10, 'G')                                       # 苍白脸
    s.rect(5, 0, 22, 2, 'i'); s.rect(4, 2, 5, 28, 'g'); s.rect(22, 2, 23, 28, 'g'); s.rect(4, 12, 4, 28, 'G')   # 头纱
    s.rect(10, 6, 12, 6, 'k'); s.rect(15, 6, 17, 6, 'k')
    s.px(11, 7, 'r'); s.px(16, 7, 'r'); s.px(12, 7, 'R'); s.px(15, 7, 'R')                       # 红眼
    s.rect(13, 10, 14, 10, 'r'); s.px(12, 11, 'w'); s.px(15, 11, 'w'); s.px(15, 12, 'R')         # 红唇、獠牙、血滴
    s.rect(12, 12, 15, 13, 'W')
    s.rect(9, 14, 18, 23, 'w'); s.rect(9, 14, 10, 23, 'G'); s.rect(9, 23, 18, 23, 'X')           # 婚纱上身、腰带
    s.rect(13, 15, 14, 17, 'G')
    for y in range(24, 40):                                                                    # 蓬裙
        hwid = 5 + (y - 24) * 0.55
        for x in range(int(14 - hwid), int(14 + hwid) + 1):
            s.px(x, y, 'G' if x >= 14 + hwid - 2 or (x - y) % 7 == 0 else 'w')
    for x in range(4, 25, 2): s.px(x, 40, 'g'); s.px(x + 1, 40, 'G')                          # 蕾丝裙摆
    s.rect(18, 15, 21, 20, 'W'); s.rect(21, 15, 24, 19, 'X'); s.px(22, 15, 'r'); s.px(23, 17, 'r'); s.px(21, 19, 'r'); s.px(22, 14, 'D'); s.px(24, 14, 'D')   # 捧着黑红玫瑰
    s.rect(24, 17, 26, 17, 'D')
    s.rect(5, 15, 8, 21, 'W'); s.px(4, 22, 'k'); s.px(5, 22, 'k')                              # 另一手：利爪
    s.outline(); return s


def wolfman():
    s = Spr(34, 38)
    s.rect(9, 0, 11, 3, '7'); s.rect(17, 0, 19, 3, '7')                                         # 耳
    s.rect(9, 3, 19, 12, '6'); s.rect(9, 3, 10, 11, '7')                                        # 头
    s.rect(19, 7, 25, 11, '8'); s.rect(19, 11, 24, 11, '7'); s.px(25, 7, 'k'); s.px(20, 12, 'w'); s.px(23, 12, 'w'); s.px(25, 11, 'w')   # 吻部、獠牙
    s.rect(14, 5, 18, 5, '7'); s.px(16, 6, 'r'); s.px(17, 6, 'r'); s.px(18, 6, 'R')              # 凶眼
    s.rect(7, 11, 20, 15, '7'); s.px(8, 16, '7'); s.px(12, 16, '7'); s.px(16, 16, '7'); s.px(19, 16, '7')   # 鬃毛
    s.rect(7, 14, 20, 27, '6'); s.rect(7, 14, 8, 27, '7'); s.rect(13, 16, 19, 25, '8')            # 躯干与胸
    s.rect(8, 26, 19, 31, 'B'); s.px(9, 31, 'k'); s.px(13, 31, 'k'); s.px(17, 31, 'k'); s.px(11, 30, 'b')   # 破烂裤
    s.rect(3, 15, 7, 29, '6'); s.rect(2, 29, 7, 31, '8'); s.px(2, 32, 'w'); s.px(4, 32, 'w'); s.px(6, 32, 'w')   # 下垂的臂与爪
    s.rect(20, 16, 28, 19, '6'); s.rect(28, 15, 30, 20, '8'); s.px(31, 15, 'w'); s.px(31, 17, 'w'); s.px(31, 19, 'w')
    s.rect(8, 32, 11, 35, '6'); s.rect(15, 32, 18, 35, '6'); s.rect(7, 36, 12, 36, '7'); s.rect(14, 36, 19, 36, '7')
    s.outline(); return s


def vamp_minion():
    s = Spr(26, 38)
    s.rect(4, 14, 21, 34, 'N'); s.rect(5, 15, 20, 33, 'h'); s.rect(5, 18, 6, 33, 'm'); s.rect(19, 18, 20, 33, 'm')   # 斗篷
    s.rect(6, 10, 8, 17, 'm'); s.rect(17, 10, 19, 17, 'm')                                     # 立领
    s.rect(9, 4, 16, 14, 'W'); s.rect(9, 4, 10, 13, 'G')
    s.rect(8, 1, 17, 5, 'k'); s.px(12, 6, 'k'); s.px(13, 6, 'k')                                # 背头
    s.px(11, 9, 'r'); s.px(14, 9, 'r'); s.rect(11, 8, 12, 8, 'k'); s.rect(14, 8, 15, 8, 'k')
    s.rect(12, 12, 13, 12, 'X'); s.px(11, 13, 'w'); s.px(14, 13, 'w')
    s.rect(10, 15, 15, 26, 'w'); s.rect(12, 15, 13, 18, 'r'); s.rect(10, 26, 15, 26, 'k')       # 衬衣、领结
    s.rect(7, 17, 9, 25, 'h'); s.rect(16, 17, 18, 25, 'h'); s.rect(18, 22, 21, 23, 'h'); s.rect(21, 22, 23, 23, 'W'); s.px(24, 22, 'k'); s.px(24, 23, 'k')
    s.rect(10, 27, 12, 34, 'k'); s.rect(14, 27, 16, 34, 'k'); s.rect(10, 35, 13, 36, 'h'); s.rect(14, 35, 17, 36, 'h')
    s.outline(); return s


def ghost_white(reveal=False):
    """白衣女鬼（水鬼）：长发、湿漉漉的白衣；reveal=False 捂脸哭泣，True=抬头露出青灰的脸与红眼"""
    s = Spr(26, 42)
    s.rect(7, 1, 18, 10, 'k'); s.rect(6, 4, 7, 32, 'k'); s.rect(18, 4, 19, 32, 'k'); s.rect(5, 18, 6, 36, 'k'); s.rect(19, 18, 20, 36, 'k')   # 长发
    if reveal:
        s.rect(9, 4, 16, 14, 'z'); s.rect(9, 4, 10, 13, 'Z'); s.rect(11, 3, 14, 4, 'k')
        s.px(10, 8, 'r'); s.px(11, 8, 'r'); s.px(14, 8, 'r'); s.px(15, 8, 'r'); s.rect(10, 7, 11, 7, 'k'); s.rect(14, 7, 15, 7, 'k')
        s.rect(11, 11, 14, 13, 'k'); s.px(12, 12, 'R'); s.px(13, 12, 'R')                      # 张着嘴
        s.rect(5, 18, 7, 24, 'z'); s.rect(18, 18, 20, 24, 'z'); s.px(4, 25, 'w'); s.px(6, 25, 'w'); s.px(19, 25, 'w'); s.px(21, 25, 'w')   # 伸出的手
    else:
        s.rect(9, 4, 16, 8, 'k'); s.rect(9, 9, 16, 11, 'W')
        s.rect(8, 9, 11, 13, 'W'); s.rect(14, 9, 17, 13, 'W'); s.rect(8, 9, 8, 13, 'G'); s.px(12, 12, 'k')   # 双手捂脸
    s.rect(8, 14, 17, 30, 'w'); s.rect(8, 14, 9, 30, 'G'); s.rect(7, 28, 18, 38, 'w')
    for y in range(28, 39):
        s.px(7, y, 'G'); s.px(18, y, 'G')
    for x in range(7, 19, 2): s.px(x, 39, 'w'); s.px(x + 1, 39, 'G')
    for y in (33, 36): s.px(10, y, 'c'); s.px(15, y + 1, 'c')                                  # 水渍
    s.outline(); return s


def bearer():
    return believer(False)
