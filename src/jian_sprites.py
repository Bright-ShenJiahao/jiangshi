# 第四位主角：青城剑仙 · 温。需先 exec sprites.py（Spr / PAL）；热血物语式大头，身高与道长一致
# 站立 jianke()；御剑 jian_fly()；行走 jian_walk(1/2)（游戏里不用）；刺剑式 jian_thrust()；劈剑式 jian_cleave()
# 出招图比站立图宽：人物身体都画在左边 0~25 列，游戏里按 JIAN_AX（身体中心 = 13）对齐
import math
PAL.update({'ql': (70, 170, 190), 'qd': (30, 96, 120), 'qr': (190, 232, 240)})


def _jbody(s, step=0, back=True, rarm='down', fierce=False):
    R, P = s.rect, s.px
    if back:   # 背后的巨剑：斜背，剑柄在右肩上方，剑尖越过左髋
        for t in range(0, 22):
            x, y = 21 - t, 11 + t
            R(x - 2, y, x + 2, y, 'G'); R(x - 1, y, x + 1, y, 'W'); P(x + 1, y, 'g'); P(x - 2, y, 'E')
        for t in (4, 10, 16): R(21 - t - 2, 11 + t, 21 - t + 2, 11 + t, 'E')
        P(0, 32, 'G'); P(1, 32, 'W'); P(0, 33, 'G')
        for k in range(0, 5):
            x, y = 22 + k, 10 - k
            P(x - 1, y, 'B'); P(x, y, 'B' if k % 2 else 'O'); P(x + 1, y, 'B')
        R(25, 5, 26, 6, 'r'); P(25, 7, 'r')
        for k in range(-3, 4):
            x, y = 21 + k, 10 + k
            P(x, y, 'o'); P(x + 1, y, 'O')
    # 发带（青白相间）从发髻飘向右后方
    for x, y, c in [(15, 1, 'ql'), (16, 1, 'qr'), (17, 2, 'ql'), (18, 2, 'qr'), (19, 3, 'ql'), (20, 4, 'qr'), (21, 6, 'ql'), (20, 8, 'qr'), (21, 10, 'ql')]:
        P(x, y, c); P(x, y + 1, c)
    # 头发：高髻 + 玉簪 + 鬓发
    R(11, 0, 14, 2, 'k'); P(12, 0, 'H'); R(8, 3, 17, 7, 'k'); R(6, 5, 7, 14, 'k'); R(18, 5, 19, 14, 'k'); R(7, 4, 8, 4, 'k'); R(17, 4, 18, 4, 'k')
    R(11, 2, 14, 2, 'qd'); P(12, 2, 'j'); P(13, 2, 'j')
    # 脸
    R(7, 7, 18, 16, 's'); R(7, 7, 7, 15, 'S'); s.clear((7, 16), (18, 16)); P(7, 16, 'k'); P(18, 16, 'k')
    R(8, 6, 17, 6, 'k'); R(8, 7, 9, 8, 'k'); R(16, 7, 17, 8, 'k'); P(12, 7, 'k'); P(13, 7, 'k')
    R(8, 10, 11, 10, 'k'); R(14, 10, 17, 10, 'k'); P(8, 9, 'k'); P(17, 9, 'k')               # 剑眉
    R(9, 11, 10, 13, 'k'); P(10, 11, 'w'); R(15, 11, 16, 13, 'k'); P(16, 11, 'w')            # 眼
    if fierce:   # 出招：眉头压低、眼神更凌厉、抿嘴
        P(11, 11, 'k'); P(14, 11, 'k'); P(10, 11, 'k'); P(16, 11, 'k'); P(9, 12, 'w'); P(15, 12, 'w')
        R(11, 15, 14, 15, 'S')
    else:
        R(12, 14, 13, 14, 'S')
    # 青色短道袍 + 白交领
    R(8, 17, 17, 28, 'ql'); R(8, 17, 9, 28, 'qd'); R(16, 17, 17, 28, 'qd')
    R(10, 17, 15, 17, 'w'); P(11, 18, 'w'); P(12, 19, 'w'); P(13, 20, 'w'); P(12, 18, 'w'); P(14, 18, 'w'); P(15, 19, 'w'); R(12, 17, 13, 18, 'S')
    R(8, 23, 17, 25, 'N'); R(8, 23, 17, 23, 'n'); P(14, 24, 'j'); P(14, 25, 'j'); P(15, 26, 'qr'); P(15, 27, 'qr')
    for t in range(0, 10): P(16 - t, 18 + t, 'B'); P(15 - t, 18 + t, 'B')                # 斜挎的剑带
    P(12, 22, 'o'); P(13, 21, 'o')
    # 手臂：行走时前后摆
    la = [0, 1, -1][step]; ra = -la
    R(5, 18 + la, 7, 24 + la, 'ql'); R(5, 18 + la, 5, 24 + la, 'qd'); R(5, 25 + la, 7, 26 + la, 'w'); R(5, 27 + la, 7, 28 + la, 's')
    if rarm == 'down':
        R(18, 18 + ra, 20, 22 + ra, 'ql'); R(18, 18 + ra, 18, 22 + ra, 'qd'); R(18, 23 + ra, 20, 25 + ra, 'w'); R(17, 25 + ra, 19, 26 + ra, 's')
    elif rarm == 'fwd':
        R(18, 18, 22, 20, 'ql'); R(18, 20, 22, 20, 'qd'); R(23, 18, 24, 20, 'w'); R(25, 18, 26, 20, 's')
    elif rarm == 'up':
        R(18, 13, 20, 18, 'ql'); R(18, 13, 18, 18, 'qd'); R(19, 11, 21, 12, 'w'); R(20, 9, 22, 10, 's')
    # 腿：深蓝裤、白绑腿、黑布鞋；step=1/2 迈左/右腿（抬 3 格）
    lh = [0, 3, 0][step]; rh = [0, 0, 3][step]
    R(9, 29, 12, 33 - lh, 'n'); R(14, 29, 17, 33 - rh, 'n'); R(9, 31 - lh, 12, 32 - lh, 'w'); R(14, 31 - rh, 17, 32 - rh, 'w')
    R(8, 34 - lh, 12, 35 - lh, 'k'); R(14, 34 - rh, 18, 35 - rh, 'k'); P(9, 34 - lh, 'H'); P(15, 34 - rh, 'H')


def jianke(drawn=False, step=0):
    """青城剑仙：站立（step=0）或行走帧（1/2），背巨剑"""
    s = Spr(26, 37); _jbody(s, step); s.outline(); return s


def jian_walk(step):
    return jianke(False, step)


def jian_fly():
    """天罗步五重：背上的巨剑落到脚下御剑飞行，人物背后不再背剑（剑在游戏里画在脚下）"""
    s = Spr(26, 37); _jbody(s, 0, back=False); s.outline(); return s


def jian_thrust():
    """刺剑式：右臂平伸，巨剑水平刺出，上下带青色剑气"""
    s = Spr(48, 37)
    _jbody(s, 1, back=False, rarm='fwd', fierce=True)
    s.rect(26, 19, 27, 19, 'B'); s.px(27, 18, 'O'); s.px(27, 20, 'O')
    s.rect(28, 16, 29, 22, 'o'); s.rect(29, 16, 29, 22, 'O')
    s.rect(30, 17, 44, 21, 'G'); s.rect(30, 18, 44, 20, 'W'); s.rect(30, 21, 44, 21, 'E'); s.rect(30, 17, 44, 17, 'g')
    s.rect(45, 18, 45, 20, 'G'); s.px(46, 19, 'W')
    s.px(25, 17, 'r'); s.px(24, 16, 'r')
    s.outline()
    for x in range(31, 47):
        if x % 2: s.px(x, 15, 'ql')
        else: s.px(x, 23, 'ql')
    for x in range(36, 48):
        if s.g[19][x] is None: s.px(x, 19, 'qr')
    return s


def jian_cleave():
    """劈剑式：巨剑高举过头，身后一道青色弧光"""
    s = Spr(44, 37)
    _jbody(s, 2, back=False, rarm='up', fierce=True)
    for t in range(0, 15):
        x, y = 24 + t, 6 - int(t * 0.4)
        s.rect(x, y - 2, x, y + 2, 'G'); s.rect(x, y - 1, x, y + 1, 'W'); s.px(x, y + 2, 'E'); s.px(x, y - 2, 'g')
    s.rect(22, 4, 23, 9, 'o'); s.rect(23, 4, 23, 9, 'O')
    s.px(21, 8, 'B'); s.px(20, 8, 'B'); s.px(19, 9, 'r'); s.px(18, 10, 'r')
    s.px(39, 0, 'G'); s.px(39, 1, 'W'); s.px(40, 0, 'W')
    s.outline()
    for a in range(-70, 60, 3):
        t = math.radians(a)
        for r, c in ((19, 'qr'), (18, 'ql')):
            x = int(23 + r * math.cos(t)); y = int(19 - r * math.sin(t))
            if 0 <= x < s.w and 0 <= y < s.h and s.g[y][x] is None: s.g[y][x] = c
    return s


def jian_flysword():
    """飞剑：小号青钢剑（剑尖朝右），环绕、御剑、剑阵共用"""
    s = Spr(15, 5)
    s.rect(0, 2, 2, 2, 'B'); s.px(3, 1, 'o'); s.px(3, 2, 'o'); s.px(3, 3, 'o')
    s.rect(4, 1, 12, 3, 'G'); s.rect(4, 2, 12, 2, 'W'); s.px(13, 2, 'W'); s.px(14, 2, 'G')
    s.outline(); return s
