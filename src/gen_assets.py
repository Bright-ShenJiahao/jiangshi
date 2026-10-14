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
he = html.index('</style>') + len('</style>')
page = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n'
        + html[:he] + '\n</head>\n<body>' + html[he:] + '\n</body>\n</html>\n')
pub = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
if os.path.isdir(pub):
    open(os.path.join(pub, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.normpath(os.path.join(pub, 'index.html')))
