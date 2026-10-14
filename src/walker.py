from PIL import Image, ImageDraw, ImageFont
g = {}
exec(open('sprites.py').read().split('\nsheet()')[0], g)
Spr, PAL = g['Spr'], g['PAL']
PAL.update({'u': (150, 160, 128), 'U': (98, 110, 88), 'd': (112, 98, 82), 'D': (72, 60, 52), 'E': (52, 50, 56)})


def walker():
    s = Spr(26, 32)
    # hunched back + ragged shirt
    s.rect(7, 14, 12, 17, 'd'); s.rect(8, 15, 16, 24, 'd'); s.rect(7, 15, 9, 24, 'D')
    for x in range(8, 17, 2): s.px(x, 25, 'd')
    s.rect(12, 18, 14, 20, 'u'); s.rect(12, 19, 14, 19, 'U')  # torn hole showing ribs
    s.rect(8, 21, 16, 21, 'B')  # rope belt
    # head thrust forward and low (shifted down/forward for a stronger hunch)
    def R(x0, y0, x1, y1, c): s.rect(x0 + 1, y0 + 2, x1 + 1, y1 + 2, c)
    def P(x, y, c): s.px(x + 1, y + 2, c)
    R(11, 8, 19, 15, 'u'); s.clear((20, 10), (20, 17), (12, 17))
    R(11, 9, 12, 14, 'U'); P(20, 12, 'u')
    R(15, 10, 17, 12, 'E'); P(16, 11, 'w')
    R(15, 14, 18, 14, 'k'); P(16, 14, 'w'); P(18, 13, 'U')
    R(9, 6, 17, 8, 'h'); R(10, 9, 12, 13, 'h')
    for x, y in [(8, 9), (8, 10), (9, 11), (9, 12), (9, 13), (13, 9), (14, 9), (18, 7)]: P(x, y, 'h')
    s.rect(7, 12, 10, 15, 'd'); s.rect(7, 13, 8, 15, 'D')  # raised hump behind the head
    # dangling arms
    s.rect(15, 16, 19, 18, 'd'); s.px(19, 18, 'D')
    s.rect(19, 18, 21, 20, 'u'); s.rect(19, 20, 21, 20, 'U')
    s.px(20, 21, 'U'); s.px(22, 21, 'U'); s.px(21, 22, 'U')
    s.rect(13, 17, 16, 18, 'D')
    # legs mid-step, bare feet
    s.rect(9, 25, 11, 28, 'D'); s.rect(8, 29, 11, 29, 'u')
    s.rect(14, 25, 16, 28, 'D'); s.rect(14, 29, 17, 29, 'u')
    s.outline()
    return s


if __name__ == '__main__':
    sc = 8
    FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
    f1, f2 = ImageFont.truetype(FONT, 40, index=2), ImageFont.truetype(FONT, 22, index=2)
    W, H = 1500, 520
    im = Image.new('RGB', (W, H), (30, 22, 48)); d = ImageDraw.Draw(im)
    Z, Wk = g['zombie']().img(), walker().img()

    def cell(x0, w, title, sub):
        d.rectangle([x0, 20, x0 + w, 400], fill=(42, 32, 66))
        d.text((x0 + w // 2, 440), title, font=f1, fill=(244, 214, 110), anchor='mm')
        d.text((x0 + w // 2, 488), sub, font=f2, fill=(200, 190, 225), anchor='mm')

    def put(sp, cx, base, cut=1.0):
        h = int(sp.height * cut)
        part = sp.crop((0, 0, sp.width, h)).resize((sp.width * sc, h * sc), Image.NEAREST)
        im.paste(part, (cx - part.width // 2, base - part.height), part)

    cell(20, 330, '僵尸', '对比：清朝官服、蹦着走')
    d.ellipse([105, 360, 265, 384], fill=(18, 12, 30)); put(Z, 185, 372)
    cell(370, 330, '行尸', '血 8 · 速度 30 · 走路追人')
    d.ellipse([455, 360, 615, 384], fill=(18, 12, 30)); put(Wk, 535, 372)
    cell(720, 760, '从坟里爬出来', '先冒头 → 爬出半身 → 站起来追人（约 1 秒）')
    for i, cut in enumerate((0.3, 0.62, 1.0)):
        cx = 850 + i * 250
        d.ellipse([cx - 95, 300, cx + 95, 400], fill=(24, 14, 30)); d.ellipse([cx - 90, 305, cx + 90, 395], fill=(98, 72, 92)); d.ellipse([cx - 70, 312, cx + 45, 360], fill=(118, 92, 112))
        put(Wk, cx, 352 if cut < 1 else 340, cut)
        if cut < 1:
            d.rectangle([cx - 80, 352, cx + 80, 362], fill=(98, 72, 92))
            for k in range(7):
                x = cx - 70 + k * 23; y = 330 - (k % 3) * 14 - int(cut * 20)
                d.rectangle([x, y, x + 10, y + 10], fill=(24, 14, 30)); d.rectangle([x + 2, y + 2, x + 8, y + 8], fill=(126, 98, 120))
    im.save('walker.png')
