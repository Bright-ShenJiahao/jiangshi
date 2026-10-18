import base64, io, json
from PIL import Image
import map_gen5

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
    'villager': map_gen5.villager_spr(g),
}
exec(open('story_sprites.py').read(), g)
g['PAL']['P'] = (236, 112, 104)
sprites.update({'afu': g['afu']().img(), 'afuR': g['afu'](True).img(), 'ren': g['ren']().img(),
                'coffin': g['coffin']().img(), 'lid': g['coffin_lid']().img(), 'rooster': g['rooster']().img()})
exec(open('easter_sprites.py').read(), g)
sprites.update({'cap': g['captain']().img(), 'capN': g['captain'](False).img(), 'sold': g['soldier']().img(),
                'watch': g['watchman']().img(), 'watchR': g['watchman'](False).img(), 'gong': g['gong']().img(), 'pcap': g['police_cap']().img()})
def _redface(im, k):
    out = im.copy(); px_ = out.load(); S1, S2 = (246, 198, 146), (204, 140, 92)
    to = {1: ((246, 160, 132), (214, 112, 84)), 2: ((240, 112, 100), (196, 70, 64))}[k]
    for y in range(min(out.height, 26)):
        for x in range(out.width):
            r, g_, b_, a_ = px_[x, y]
            if a_ and (r, g_, b_) == S1: px_[x, y] = to[0] + (a_,)
            elif a_ and (r, g_, b_) == S2: px_[x, y] = to[1] + (a_,)
    return out
sprites['taoistR1'] = _redface(sprites['taoist'], 1); sprites['taoistR2'] = _redface(sprites['taoist'], 2)
exec(open('new_chars.py').read(), g)
sprites.update({'renZ': g['ren_zombie']().img(), 'simu': g['simu']().img(), 'corpse': g['corpse']().img(), 'believer': g['believer']().img(), 'believerS': g['believer'](False).img(),
                'thrall': g['believer'](False, True).img(), 'bananaG': g['banana_ghost']().img(), 'bananaT': g['banana_ghost'](True).img(),
                'bikeG': g['qiusheng_bike_bride']().img(), 'bike': g['qiusheng_bike'](False).img(), 'operaDan': g['opera_dan']().img(), 'operaJing': g['opera_jing']().img(), 'wuW': g['wuchang']().img(), 'wuB': g['wuchang'](False).img()})
sprites['monk'] = g['monk']('pole').img(); sprites['monkR1'] = _redface(sprites['monk'], 1); sprites['monkR2'] = _redface(sprites['monk'], 2)
exec(open('priest_sprites.py').read(), g)
for _gun in (False, True):
    for _f, _n in (('', 'priest'), ('v', 'priestV'), ('l', 'priestL')):
        _k = _n + ('G' if _gun else ''); sprites[_k] = g['priest'](_gun, _f).img()
        sprites[_k + 'R1'] = _redface(sprites[_k], 1); sprites[_k + 'R2'] = _redface(sprites[_k], 2)
sprites.update({'angel': g['angel']().img(), 'cherub': g['cherub']().img()})
exec(open('jian_sprites.py').read(), g)   # 青城剑仙：站立、御剑（背后无剑）、刺剑、劈剑（出招图身体在左，游戏里按 JIAN_AX 对齐）
for _k, _im in (('jian', g['jianke']().img()), ('jianF', g['jian_fly']().img()), ('jianT', g['jian_thrust']().img()), ('jianC', g['jian_cleave']().img())):
    sprites[_k] = _im; sprites[_k + 'R1'] = _redface(_im, 1); sprites[_k + 'R2'] = _redface(_im, 2)
sprites['jfly'] = g['jian_flysword']().img()
exec(open('gods_sprites.py').read(), g)
sprites.update({'zhongkui': g['zhongkui']().img(), 'yanluo': g['yanluo']().img(), 'erlang': g['erlang']().img(), 'dog': g['dog']().img(), 'rulai': g['rulai']().img(), 'baoda': g['baoda']().img()})
exec(open('gan_sprites.py').read(), g)   # 湘西赶尸王：本人、钟馗附体（借用钟馗图）、尸傀、小鬼、驭灵五物、献祭三妖
_im = g['ganshi']().img(); sprites.update({'gan': _im, 'ganR1': _redface(_im, 1), 'ganR2': _redface(_im, 2)})
sprites.update({'ganZ': sprites['zhongkui'], 'ganZR1': sprites['zhongkui'], 'ganZR2': sprites['zhongkui']})
sprites.update({'gCorpse': g['gan_corpse']().img(), 'gImp': g['gan_imp']().img(), 'gToad': g['gan_toad']().img(), 'gScorp': g['gan_scorp']().img(), 'gSnake': g['gan_snake']().img(),
                'gChang': g['gan_chang']().img(), 'gTiger': g['gan_tiger']().img(), 'gShan': g['gan_shangui']().img(), 'gYecha': g['gan_yecha']().img(), 'gHanba': g['gan_hanba']().img(), 'gHou': g['gan_hou']().img()})
exec(open('monsters2.py').read(), g)
exec(open('church2_sprites.py').read(), g)
def _red(im):
    im = im.convert('RGBA'); px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, gg, b, a = px[x, y]
            if a:
                l = (r + gg + b) / 3
                px[x, y] = (min(255, int(40 + l * 1.15)), int(l * 0.22), int(l * 0.3), a)
    return im
sprites.update({'coffinR': _red(g['coffin_w']().img()), 'coffinRo': _red(g['coffin_w'](True).img())})
sprites.update({'coffinW': g['coffin_w']().img(), 'coffinWo': g['coffin_w'](True).img(), 'coffinWh': g['coffin_w']().img().rotate(90, expand=True), 'bride': g['bride']().img(), 'wolf': g['wolfman']().img(), 'wolfC': g['wolfman'](True).img(), 'vampM': g['vamp_minion']().img(), 'ghostW': g['ghost_white']().img(), 'ghostWf': g['ghost_white'](True).img(), 'bearer': g['believer'](False).img()})
sprites.update({'vampire': g['vampire']().img(), 'ghostR': g['red_ghost'](g), 'jumperM': g['hairy'](g['zombie']('m', 'M').img()),
                'chest': g['chest']().img(), 'chestB': g['chest'](True).img()})
m3 = {}
exec(open('monsters3.py').read().split('# ---------- 拼图')[0], m3)
sprites.update({'zP': m3['purple'], 'zW': m3['white'], 'zG': m3['green'], 'walkF': m3['female'](), 'walkS': m3['skeleton'](), 'shasha': m3['shasha'](True)})
import qrcode
_q = qrcode.QRCode(border=2, box_size=1, error_correction=qrcode.constants.ERROR_CORRECT_M)
_q.add_data('https://jiangshidaozhang.netlify.app/'); _q.make(fit=True)
sprites['qr'] = _q.make_image(fill_color='black', back_color='white').convert('RGBA')
bg, objsprites, data = map_gen5.build()
sprites.update(objsprites)
# ---- 章节地图：每章单独打包成 public/ch/<id>.js，选中时才下载；标题页只带小缩略图 ----
import map_heian, map_london, map_nanyang, map_qin
CHAPTERS = {}
def _qpng(im, colors=112):
    q = im.convert('RGB').quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    buf = io.BytesIO(); q.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
def _thumb(im):
    t = im.convert('RGB'); sc = 132 / t.width; return t.resize((132, max(1, round(t.height * sc))), Image.BOX)
def _pv(im):
    t = im.convert('RGB'); sc = 360 / t.width; return t.resize((360, max(1, round(t.height * sc))), Image.BOX)
sprites['th_ren'] = _thumb(bg); PV = {'ren': _pv(bg)}
for _cid, _mod in (('heian', map_heian), ('london', map_london), ('nanyang', map_nanyang), ('qin', map_qin)):
    _bg, _sp, _data, _ = _mod.build()
    _as = {k: b64(v) for k, v in _sp.items()}; _as['bg_' + _cid] = _qpng(_bg)
    CHAPTERS[_cid] = (_data, _as); sprites['th_' + _cid] = _thumb(_bg); PV[_cid] = _pv(_bg)
assets = {k: b64(v) for k, v in sprites.items()}
assets['bg'] = b64(bg.convert('RGB'))
for _k, _v in PV.items(): assets['pv_' + _k] = _qpng(_v, 64)
import glob, os
vo = {os.path.splitext(os.path.basename(f))[0]: 'data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob('tts/vo/*.mp3'))}
html = open('game_template.html').read().replace('/*ASSETS*/{}', json.dumps(assets)).replace('/*MAP*/{}', json.dumps(data, separators=(',', ':'))).replace('/*VO*/{}', json.dumps(vo)).replace('/*BUILD*/', __import__('time').strftime('%y%m%d%H%M'))
open('game.html', 'w').write(html)
print(len(html) // 1024, 'KB')

# also write the standalone page used by Netlify (public/index.html next to this src folder)
import os
from PIL import ImageDraw, ImageFont
SITE = 'https://jiangshidaozhang.netlify.app/'
pub = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
if os.path.isdir(pub):
    # share cover (used by og:image and WeChat's legacy first-image thumbnail)
    cov = bg.crop((1030, 1200, 1390, 1560)).convert('RGBA').resize((360, 360), Image.NEAREST)
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
    # 章节文件默认不进 public（章节尚未对外开放）；CHAPTERS_LIVE=1 才写进 public/ch；CHAPTERS_TEST_DIR=目录 可另存一份做测试
    _dirs = ([os.path.join(pub, 'ch')] if os.environ.get('CHAPTERS_LIVE') == '1' else []) + ([os.environ['CHAPTERS_TEST_DIR']] if os.environ.get('CHAPTERS_TEST_DIR') else [])
    for chd in _dirs: os.makedirs(chd, exist_ok=True)
    for _cid, (_data, _as) in CHAPTERS.items():
        _js = "(window.__CH=window.__CH||{})[%s]={map:%s,assets:%s};" % (json.dumps(_cid), json.dumps(_data, separators=(',', ':')), json.dumps(_as, separators=(',', ':')))
        for chd in _dirs: open(os.path.join(chd, _cid + '.js'), 'w', encoding='utf-8').write(_js)
        print('chapter', _cid, len(_js) // 1024, 'KB', '(written)' if _dirs else '(not written)')
    print('wrote', os.path.normpath(os.path.join(pub, 'index.html')))


# ---- 防作弊：记录发布页面脚本的 SHA-256，服务器据此识别被改过的客户端 ----
import re as _re, hashlib as _h
_pp = os.path.join(pub, 'index.html')
if os.path.exists(_pp):
    _src = open(_pp, encoding='utf-8').read()
    _m = _re.search(r'<script>(.*?)</script>', _src, _re.S)
    _hash = _h.sha256(_m.group(1).encode('utf-8')).hexdigest()
    _hp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'netlify', 'functions', 'hashes.mjs')
    _old = _re.findall(r"'([0-9a-f]{64})'", open(_hp).read()) if os.path.exists(_hp) else []
    _all = ([x for x in _old if x != _hash] + [_hash])[-40:]
    open(_hp, 'w').write('// 自动生成：官方页面脚本哈希（保留最近 40 个版本）\nexport default [\n' + ''.join("  '%s',\n" % x for x in _all) + '];\n')
    print('script hash', _hash[:12])
