import base64, io, json
from PIL import Image
import map_gen2

g = {}
exec(open('sprites.py').read().split('\nsheet()')[0], g)
wg = {}
exec(open('walker.py').read().split('\nif __name__')[0], wg)


def b64(im):
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


sprites = {
    'taoist': g['taoist']().img(),
    'zombie': g['zombie']().img(),
    'jumper': g['zombie']('m', 'M', jump=False).img(),
    'ghost': g['ghost']().img(),
    'king': g['king']().img(),
    'walker': wg['walker']().img(),
    'villager': map_gen2.villager_spr(g),
}
exec(open('story_sprites.py').read(), g)
g['PAL']['P'] = (236, 112, 104)
sprites.update({'afu': g['afu']().img(), 'afuR': g['afu'](True).img(), 'ren': g['ren']().img(),
                'coffin': g['coffin']().img(), 'lid': g['coffin_lid']().img(), 'rooster': g['rooster']().img()})
import qrcode
_q = qrcode.QRCode(border=2, box_size=1, error_correction=qrcode.constants.ERROR_CORRECT_M)
_q.add_data('https://jiangshidaozhang.netlify.app/'); _q.make(fit=True)
sprites['qr'] = _q.make_image(fill_color='black', back_color='white').convert('RGBA')
bg, objsprites, data = map_gen2.build()
sprites.update(objsprites)
assets = {k: b64(v) for k, v in sprites.items()}
assets['bg'] = b64(bg.convert('RGB'))
import glob, os
vo = {os.path.basename(f)[:2]: 'data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob('tts/vo/*.mp3'))}
html = open('game_template.html').read().replace('/*ASSETS*/{}', json.dumps(assets)).replace('/*MAP*/{}', json.dumps(data, separators=(',', ':'))).replace('/*VO*/{}', json.dumps(vo))
open('game.html', 'w').write(html)
print(len(html) // 1024, 'KB')

# also write the standalone page used by Netlify (public/index.html next to this src folder)
import os
from PIL import ImageDraw, ImageFont
SITE = 'https://jiangshidaozhang.netlify.app/'
pub = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
if os.path.isdir(pub):
    # share cover (used by og:image and WeChat's legacy first-image thumbnail)
    cov = bg.crop((1030, 870, 1390, 1230 if bg.height >= 1230 else bg.height)).convert('RGBA').resize((360, 360), Image.NEAREST)
    shade = Image.new('RGBA', cov.size, (20, 12, 34, 120)); cov = Image.alpha_composite(cov, shade)
    def put(im, x, by, s, flip=False):
        im = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
        im = im.resize((im.width * s, im.height * s), Image.NEAREST); cov.alpha_composite(im, (x - im.width // 2, by - im.height))
    put(sprites['king'], 180, 190, 3, True); put(sprites['zombie'], 60, 330, 3); put(sprites['jumper'], 300, 330, 3, True); put(sprites['taoist'], 180, 350, 4)
    cov = cov.resize((600, 600), Image.NEAREST); d = ImageDraw.Draw(cov)
    try: f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 64)
    except Exception: f = ImageFont.load_default()
    for dx, col in ((4, (26, 14, 30)), (2, (200, 48, 44)), (0, (244, 228, 168))):
        d.text((300 + dx, 70 + dx), '暂时停止呼吸', font=f, fill=col, anchor='mm')
    cov.convert('RGB').save(os.path.join(pub, 'share.png'), optimize=True)
    he = html.index('</style>') + len('</style>')
    meta = ('<meta name="description" content="荒坟尸变，道长撑到鸡鸣就算你赢。像素风僵尸割草小游戏。">\n'
            '<meta property="og:type" content="website">\n<meta property="og:title" content="暂时停止呼吸">\n'
            '<meta property="og:description" content="荒坟尸变，道长撑到鸡鸣就算你赢。你能撑多久？">\n'
            f'<meta property="og:url" content="{SITE}">\n<meta property="og:image" content="{SITE}share.png">\n'
            '<meta name="twitter:card" content="summary_large_image">\n')
    page = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n'
            + meta + html[:he] + '\n</head>\n<body><div style="display:none"><img src="share.png" alt="暂时停止呼吸"></div>' + html[he:] + '\n</body>\n</html>\n')
    open(os.path.join(pub, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.normpath(os.path.join(pub, 'index.html')))
