"""打包《守卫任家镇的中心的龙脉》：
原游戏的 game_template.html（角色、法器、怪物、界面）+ 防守地图 map_defense.py + 防守玩法 defense.js
→ src/longmai.html（本地测试）和 public/longmai.html（上线用）。原游戏的文件一个都不改。

    cd src && python3 gen_defense.py
"""
import base64, io, json, os, glob, time
from PIL import Image, ImageDraw, ImageFont
import map_defense

SITE = 'https://jiangshidaozhang.netlify.app/'
URL = SITE + 'longmai.html'
TITLE = '守卫任家镇的中心的龙脉'

# ---- 角色和怪物的像素图：直接跑 gen_assets.py 里生成精灵的那一段（不生成原地图，也不写文件）----
src = open('gen_assets.py', encoding='utf-8').read().split('bg, objsprites, data = map_gen5.build()')[0]
ns = {'__name__': 'gen_defense'}
exec(src, ns)
sprites = ns['sprites']
import qrcode
_q = qrcode.QRCode(border=2, box_size=1, error_correction=qrcode.constants.ERROR_CORRECT_M)
_q.add_data(URL); _q.make(fit=True)
sprites['qr'] = _q.make_image(fill_color='black', back_color='white').convert('RGBA')
G = ns['g']
exec(open('defense_sprites.py', encoding='utf-8').read(), G)
for k, f in (('wangpo', lambda: G['wangpo']()), ('wangpoG', lambda: G['wangpo_ghost']()), ('tanG', lambda: G['tan_ghost']()), ('banditA', lambda: G['bandit']()), ('banditB', lambda: G['bandit'](True)),
             ('dabao', lambda: G['dabao']()), ('xiaobao', lambda: G['xiaobao']()), ('oilG', lambda: G['oil_ghost']()), ('iceZ', lambda: G['ice_corpse']()), ('iceW', lambda: G['ice_corpse'](True)),
             ('thugA', lambda: G['thug']()), ('thugB', lambda: G['thug'](True)), ('jiuju', lambda: G['jiuju']()), ('jiujuD', lambda: G['jiuju'](True)), ('feitou', lambda: G['feitou']()),
             ('xiaozun', lambda: G['xiaozun']()), ('moth', lambda: G['moth']()), ('xuemo', lambda: G['xuemo']()), ('cixi', lambda: G['cixi']()), ('qingbing', lambda: G['qingbing']()),
             ('feiZ', lambda: G['fei_zombie']()), ('youZ', lambda: G['you_zombie']()), ('fuZ', lambda: G['fu_zombie']()), ('bugu', lambda: G['bugu']()),
             ('xuankui', lambda: G['xuankui']()), ('yangfy', lambda: G['yangfy']()), ('xieshen', lambda: G['xieshen']())):
    sprites[k] = f().img()
sprites['capP'] = G['possessed'](sprites['cap']); sprites['soldP'] = G['possessed'](sprites['sold'])
bg, objsprites, data = map_defense.build()
sprites.update(objsprites)


def b64(im):
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


assets = {k: b64(v) for k, v in sprites.items()}
assets['bg'] = b64(bg.convert('RGB'))
# 语音：只带这里用得上的（阿威、四目、阵亡、作弊时的黑白无常和神仙）；开场剧情的配音不带
SKIP = ('bride', 'opera', 'z_', 'p1', 'p2', 'p3', 'p4')
vo = {}
for f in sorted(glob.glob('tts/vo/*.mp3')):
    k = os.path.splitext(os.path.basename(f))[0]
    if k[:2].isdigit() or k.startswith(SKIP): continue
    vo[k] = 'data:audio/mpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()

html = open('game_template.html', encoding='utf-8').read()


def rep(old, new, count=1):
    global html
    n = html.count(old)
    assert n == count, f'patch anchor found {n}x (want {count}): {old[:70]!r}'
    html = html.replace(old, new)


# ---------------- 界面 ----------------
rep('<title>暂时停止呼吸</title>', f'<title>{TITLE}</title>')
rep('<div id="clock"><b id="shichen">子时</b><span class="lbl" id="till">距鸡鸣 5:00</span><span id="combo"></span></div>',
    '<div id="clock"><b id="shichen">准备</b><span class="lbl" id="till"></span><div class="bar" id="coreb"><i></i></div><span class="lbl" id="coreV">龙脉 100</span><span id="bossV" hidden></span><span id="combo"></span></div>')
rep('<div id="stats">伏尸 <span id="kills">0</span><br>', '<div id="stats">伏尸 <span id="kills">0</span><br>铜钱 <span id="gold">0</span> 文<br>')
rep('<div id="banner" hidden></div>',
    '<div id="banner" hidden></div>\n  <button id="shopBtn" type="button" hidden>铺<small>B</small></button><button id="callBtn" type="button" hidden>战</button>')
rep('  <div class="modal" id="pause" hidden>', '  <div class="modal" id="shop" hidden><div class="card"><h2>杂货铺</h2><p style="margin:0">掌柜：「道长要什么，任老爷说了……钱还是得给。」<br>身上铜钱 <b id="shopGold" style="color:var(--talisman);font-weight:400">0</b> 文</p>'
    '<div class="opts" id="shopItems"></div><button class="btn" id="shopClose" type="button">走了（B）</button></div></div>\n  <div class="modal" id="pause" hidden>')
rep('<h1>暂时停止呼吸</h1>\n      <p>荒坟夜里尸变了。撑到鸡鸣天亮，便算你赢。</p>',
    '<h1 class="lmT">守卫任家镇的<br>中心的龙脉</h1>\n      <p>鬼门关开，三路阴兵直扑任家镇。<br>守住镇中心的龙脉，撑过三十波。</p>')
rep('''        <span>屏息</span><span>空格：僵尸闻不到人气，会乱跳</span>''',
    '''        <span>守城</span><span>怪沿三条路去龙脉，靠近你才会扑你</span>
        <span>商铺</span><span>回到镇里（牌坊以内）点「铺」或按 B</span>
        <span>开战</span><span>一波刷完后点「战」或按 N，提前开打多拿钱</span>
        <span>屏息</span><span>空格：怪闻不到人气，只顾往前走</span>''')
rep('<button class="btn" id="startBtn">开坛 · 普通</button><button class="btn hard" id="hardBtn">开坛 · 困难</button>',
    '<button class="btn" id="startBtn">守镇 · 普通</button><button class="btn hard" id="hardBtn">守镇 · 困难</button>')
rep('功德簿 · 排名</button>', '龙脉功德簿 · 排名</button>')
rep('<div class="chks"><label class="storyChk"><input type="checkbox" id="storyChk"> 播放开场剧情</label><label class="storyChk"><input type="checkbox" id="tipChk"> 新手提示</label></div>',
    '<div hidden><input type="checkbox" id="storyChk"><input type="checkbox" id="tipChk"></div><p class="hint"><a href="./" style="color:var(--muted)">← 回《暂时停止呼吸》</a></p>')
rep('<button class="btn" id="againBtn">再来一夜</button>', '<button class="btn" id="againBtn">再守一次</button>')
rep('</style>', '''#coreb { max-width: 132px; margin: 4px auto 0; height: 8px; }
#coreb i { background: linear-gradient(#7af0b0, #2a9a62); }
#coreb.mid i { background: linear-gradient(#f0d870, #b88a20); }
#coreb.low i { background: linear-gradient(#ff7a6a, #a81818); animation: lowcore .5s steps(2) infinite; }
@keyframes lowcore { 50% { opacity: .45; } }
#coreV { display: block; font-size: 12px; margin-top: 1px; }
#bossV { display: block; font-size: 13px; color: #ff8a7a; text-shadow: 1px 1px 0 var(--ink); animation: sblink 1s steps(2) infinite; }
#mmPanel { background: rgba(12, 6, 22, .7); }
#gold { color: var(--talisman); }
#gold.pop { color: #fff6c0; }
#mm { top: calc(env(safe-area-inset-top, 0px) + 92px); }
#mmCv { width: 84px; height: 140px; }
#mmT { width: 84px; }
h1.lmT { font-size: clamp(30px, 8.6vw, 54px); line-height: 1.15; letter-spacing: .1em; }
#shopBtn, #callBtn { position: absolute; left: max(16px, env(safe-area-inset-left, 0px)); border-radius: 50%; border: 3px solid var(--ink); color: var(--ink); font: 22px var(--display); box-shadow: 0 0 0 2px var(--line), 0 4px 0 var(--ink); cursor: pointer; padding: 0; }
#shopBtn { bottom: calc(env(safe-area-inset-bottom, 0px) + 46px); width: 64px; height: 64px; background: radial-gradient(circle at 40% 35%, #ffe9a0, #c89018); }
#shopBtn small { display: block; font-size: 11px; }
#shopBtn.dim { filter: grayscale(.7) brightness(.7); }
#callBtn { bottom: calc(env(safe-area-inset-bottom, 0px) + 124px); width: 64px; height: 64px; background: radial-gradient(circle at 40% 35%, #ff9a8a, #c8302c); color: var(--paper); font-size: 15px; animation: rdy 1.2s ease-out infinite; }
#shop .opt:disabled { opacity: .45; cursor: default; }
#shop .card { max-height: calc(100dvh - 32px); overflow-y: auto; }
#shopItems { margin-bottom: 10px; }
</style>''')

# ---------------- 逻辑补丁（原游戏的函数里插几处钩子） ----------------
rep('  if (S.en.length < 200) {', '  if (false) {   // 防守模式：不在玩家身边刷怪，改由 updateEvents 按波次从鬼门关刷')
rep('  if (e.jsT > S.t) dmg *= 1.3;', '  if (e.jsT > S.t) dmg *= 1.3;\n  if (e.dr != null || e.ice) dmg *= dDR(e, tag);')
rep("if (kb) { const dx = e.x - fromX, dy = e.y - fromY, l = Math.hypot(dx, dy) || 1, k = e.type === 'king'", "if (kb) { const dx = e.x - fromX, dy = e.y - fromY, l = Math.hypot(dx, dy) || 1, k = e.kbk != null ? e.kbk : e.type === 'king'")
rep('  const ml = Math.hypot(mx, my);', '  if (dCharm()) { mx = -mx; my = -my; }\n  const ml = Math.hypot(mx, my);')
rep('    if (lost) { tx = e.wx; ty = e.wy; }', '    if (lost) { tx = e.wx; ty = e.wy; }\n    { const dT = dTarget(e); if (dT) { tx = dT[0]; ty = dT[1]; } if (e.gone) continue; }')
rep('    if (e.onDie) e.onDie(e);', '    dKill(e); if (e.onDie) e.onDie(e);')
rep('const T = ETYPE[type], t = S.t,', 'const T = ETYPE[type], t = dEffT(),')
rep('    if (it.p) {\n', '    if (it.p) {\n      if (S.p.down) continue;\n')
rep('  if (ml) {', '  if (ml && !P.down) {')
rep('  updateWeapons();\n  updateMonk();\n  updatePriest();\n  updateUlts();', '  if (!P.down) { updateWeapons(); updateMonk(); updatePriest(); updateUlts(); }')
rep("const sc = e.skin === 'bride' ?", "const sc = e.bsc ? e.bsc : e.skin === 'bride' ?")
rep('function drawEventSprites(list) {', 'function drawEventSprites0(list) {')
rep("location.origin + location.pathname : SITE) + '?v=' + BUILD;", "location.origin + location.pathname : SITE + 'longmai.html') + '?v=' + BUILD;")
html = html.replace("'暂时停止呼吸.png'", "'守卫龙脉.png'").replace("title: '暂时停止呼吸'", "title: '守卫龙脉'").replace('download="暂时停止呼吸.png"', 'download="守卫龙脉.png"')
# 防守模式的脚本接在最后
rep('\n</script>', '\n' + open('defense.js', encoding='utf-8').read() + '\n</script>')

html = html.replace('/*ASSETS*/{}', json.dumps(assets)).replace('/*MAP*/{}', json.dumps(data, separators=(',', ':'))).replace('/*VO*/{}', json.dumps(vo)).replace('/*BUILD*/', time.strftime('%y%m%d%H%M'))
open('longmai.html', 'w', encoding='utf-8').write(html)
print('longmai.html', len(html) // 1024, 'KB')

# ---------------- 上线用的独立页面 public/longmai.html ----------------
pub = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public')
if os.path.isdir(pub):
    cov = bg.crop((300, 1290, 660, 1650)).convert('RGBA').resize((360, 360), Image.NEAREST)
    cov = Image.alpha_composite(cov, Image.new('RGBA', cov.size, (20, 12, 34, 110)))
    def put(im, x, by, s, flip=False):
        im = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
        im = im.resize((im.width * s, im.height * s), Image.NEAREST); cov.alpha_composite(im, (x - im.width // 2, by - im.height))
    put(sprites['longmai'], 180, 250, 2); put(sprites['jumperM'], 60, 330, 3); put(sprites['king'], 300, 330, 3, True); put(sprites['taoist'], 180, 350, 4)
    cov = cov.resize((600, 600), Image.NEAREST); d = ImageDraw.Draw(cov)
    try: f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 60)
    except Exception: f = ImageFont.load_default()
    for dx, col in ((4, (26, 14, 30)), (2, (200, 48, 44)), (0, (244, 228, 168))):
        d.text((300 + dx, 70 + dx), '守卫龙脉', font=f, fill=col, anchor='mm')
    cov.convert('RGB').save(os.path.join(pub, 'longmai.png'), optimize=True)
    he = html.index('</style>') + len('</style>')
    meta = ('<meta name="description" content="鬼门关开，三路阴兵直扑任家镇。守住镇中心的龙脉，撑过三十波。像素风僵尸防守小游戏。">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:title" content="{TITLE}">\n'
            '<meta property="og:description" content="鬼门关开，三路阴兵直扑任家镇，你能守几波？">\n'
            f'<meta property="og:url" content="{URL}">\n<meta property="og:image" content="{SITE}longmai.png">\n'
            '<meta name="twitter:card" content="summary_large_image">\n')
    page = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">\n'
            + meta + html[:he] + f'\n</head>\n<body><div style="display:none"><img src="longmai.png" alt="{TITLE}"></div>' + html[he:] + '\n</body>\n</html>\n')
    open(os.path.join(pub, 'longmai.html'), 'w', encoding='utf-8').write(page)
    print('wrote', os.path.normpath(os.path.join(pub, 'longmai.html')))
