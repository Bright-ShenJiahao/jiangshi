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


def wolfman(crawl=False):
    """狼人：深灰黑长毛、弓背前倾、长吻尖耳、红眼、利爪，反关节后腿；crawl=四肢着地的爬行形态"""
    PAL.update({'wf': (34, 30, 38), 'wF': (58, 54, 66), 'wl': (92, 86, 100), 'we': (255, 60, 50), 'wc': (232, 226, 214)})
    if crawl:
        s = Spr(42, 26)
        R, P = s.rect, s.px
        R(6, 8, 30, 16, 'wf'); R(8, 6, 26, 8, 'wF'); R(10, 5, 22, 5, 'wF')                 # 拱起的背
        for x in range(7, 29, 3): P(x, 5 + (x % 2), 'wl')                                   # 背上炸起的鬃毛
        R(26, 9, 33, 15, 'wf'); R(27, 8, 32, 8, 'wF')                                       # 前胸低伏
        R(31, 10, 39, 13, 'wF'); R(33, 14, 38, 14, 'wf'); R(39, 11, 40, 11, 'k')            # 长吻贴地
        P(34, 15, 'wc'); P(36, 15, 'wc'); P(38, 14, 'wc')                                   # 獠牙
        R(29, 5, 30, 8, 'wf'); R(32, 6, 33, 9, 'wf'); P(29, 4, 'wF'); P(32, 5, 'wF')        # 后贴的尖耳
        R(32, 10, 33, 10, 'we'); P(34, 10, 'we')                                           # 红眼
        R(26, 16, 28, 22, 'wf'); R(31, 16, 33, 21, 'wf'); R(25, 22, 29, 23, 'wF'); R(31, 21, 35, 22, 'wF')   # 前肢
        for x in (25, 27, 29, 32, 34, 35): P(x, 24 if x < 30 else 23, 'wc')                 # 前爪
        R(6, 16, 9, 19, 'wf'); R(4, 19, 7, 22, 'wf'); R(3, 22, 7, 23, 'wF')                 # 后腿（反关节）
        R(11, 16, 14, 19, 'wf'); R(10, 19, 12, 22, 'wf'); R(9, 22, 13, 23, 'wF')
        P(3, 24, 'wc'); P(9, 24, 'wc')
        R(0, 6, 6, 8, 'wf'); P(0, 5, 'wF')                                                 # 尾巴
        s.outline(); return s
    s = Spr(36, 42)
    R, P = s.rect, s.px
    R(17, 0, 18, 6, 'wf'); R(22, 1, 23, 6, 'wf'); P(17, 0, 'wF'); P(22, 1, 'wF')            # 竖起的尖耳
    R(15, 5, 25, 13, 'wf'); R(16, 4, 24, 5, 'wF')                                           # 头
    R(24, 8, 33, 12, 'wF'); R(25, 13, 32, 14, 'wf'); R(33, 9, 34, 10, 'k')                  # 长吻
    P(26, 15, 'wc'); P(28, 15, 'wc'); P(31, 14, 'wc'); P(33, 12, 'wc')                      # 獠牙
    R(21, 7, 23, 7, 'we'); P(23, 8, 'we')                                                  # 红眼
    R(9, 10, 24, 14, 'wF')                                                                 # 炸起的颈鬃
    for x in range(9, 24, 2): P(x, 9 + (x % 3), 'wl')
    R(6, 13, 23, 26, 'wf'); R(6, 13, 9, 26, 'wF'); R(14, 15, 21, 23, 'wl')                  # 弓背前倾的躯干、胸毛
    R(5, 11, 12, 14, 'wf')                                                                 # 驼起的背
    R(20, 15, 26, 18, 'wf'); R(25, 17, 28, 27, 'wf'); R(27, 27, 31, 28, 'wF')               # 前伸的长臂
    for x in (27, 29, 31): P(x + 1, 29, 'wc')                                              # 利爪
    R(3, 15, 7, 25, 'wf'); R(2, 25, 5, 28, 'wF'); P(1, 29, 'wc'); P(3, 29, 'wc'); P(5, 29, 'wc')   # 后侧的手臂
    R(7, 26, 21, 30, 'B'); P(9, 30, 'k'); P(14, 30, 'k'); P(19, 30, 'k')                     # 破烂短裤
    R(8, 30, 12, 33, 'wf'); R(6, 33, 9, 37, 'wf'); R(8, 37, 12, 39, 'wf'); R(8, 40, 13, 40, 'wF')   # 反关节后腿
    R(15, 30, 19, 33, 'wf'); R(14, 33, 17, 37, 'wf'); R(16, 37, 20, 39, 'wf'); R(16, 40, 21, 40, 'wF')
    P(13, 41, 'wc'); P(21, 41, 'wc')
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
