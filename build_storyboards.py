"""Renders storyboards/index.html from the per-concept storyboard folders. usage: python3 build_storyboards.py"""
import html, json, os, re, shutil, subprocess
from concepts_v2 import CONCEPTS, LPS

e = html.escape
SB = '/Users/farooq.chisty/claude fc/brevo-ads-meta/storyboards'
OUT = 'storyboards'
PICKS = [1, 3, 4, 5, 8]
CAST = [('simone', 'Simone', '03, 04', 'Ad Studio identity, locked for new takes'), ('arjun', 'Arjun', '03', 'Ad Studio identity'),
        ('nadia', 'Nadia', '01', 'host'), ('claire', 'Claire', '04', 'founder'), ('leah', 'Leah', '05', 'marketer'),
        ('marcus', 'Marcus', '03', 'cold-brew creator'), ('tess', 'Tess', '03', 'protein-bar creator')]


def md(text):
    """Small markdown to HTML: headings, tables, lists, code fences, paragraphs, bold, inline code."""
    out, lines, i = [], text.split('\n'), 0
    inl = lambda s: re.sub(r'`([^`]+)`', r'<code>\1</code>', re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', e(s)))
    while i < len(lines):
        l = lines[i]
        if l.startswith('```'):
            j = i + 1
            while j < len(lines) and not lines[j].startswith('```'):
                j += 1
            out.append('<pre>' + e('\n'.join(lines[i + 1:j])) + '</pre>'); i = j + 1; continue
        if re.match(r'^#{1,4} ', l):
            n = min(len(l) - len(l.lstrip('#')) + 2, 5); out.append(f'<h{n}>{inl(l.lstrip("#").strip())}</h{n}>'); i += 1; continue
        if l.strip().startswith('|') and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            head = [c.strip() for c in l.strip().strip('|').split('|')]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip().startswith('|'):
                rows.append([c.strip() for c in lines[j].strip().strip('|').split('|')]); j += 1
            out.append('<div class="tbl"><table><thead><tr>' + ''.join(f'<th>{inl(h)}</th>' for h in head) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')
            i = j; continue
        if re.match(r'^\s*([-*]|\d+\.) ', l):
            tag = 'ol' if re.match(r'^\s*\d+\.', l) else 'ul'; items = []
            while i < len(lines) and re.match(r'^\s*([-*]|\d+\.) ', lines[i]):
                items.append(re.sub(r'^\s*([-*]|\d+\.) ', '', lines[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inl(x)}</li>' for x in items) + f'</{tag}>'); continue
        if l.strip():
            para = [l]; i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|\s*([-*]|\d+\.) )', lines[i]):
                para.append(lines[i]); i += 1
            out.append('<p>' + inl(' '.join(para)) + '</p>'); continue
        i += 1
    return '\n'.join(out)


def jpg(src, dst, width=1080, q=82):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(q), '-Z', str(int(width * 1920 / 1080)), src, '--out', dst], capture_output=True)


os.makedirs(OUT, exist_ok=True)
sections, nav = [], []
for c in [c for c in CONCEPTS if c['n'] in PICKS]:
    n = c['n']; d = f'{SB}/c{n:02d}'; o = f'{OUT}/c{n:02d}'
    if not os.path.isdir(d):
        continue
    os.makedirs(o, exist_ok=True)
    shots = json.load(open(f'{d}/shots.json')) if os.path.exists(f'{d}/shots.json') else []
    frames = sorted(f for f in os.listdir(f'{d}/frames') if re.match(r'f\d+.*\.png$', f)) if os.path.isdir(f'{d}/frames') else []
    for f in frames:
        jpg(f'{d}/frames/{f}', f'{o}/{f[:-4]}.jpg')
    anim = ''
    if os.path.exists(f'{d}/animatic.mp4'):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{d}/animatic.mp4', '-vf', 'scale=720:-2', '-c:v', 'libx264', '-crf', '24', '-preset', 'veryfast',
                        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', f'{o}/animatic.mp4'], check=True)
        first = frames[0] if frames else None
        anim = f'<video class="tall" src="c{n:02d}/animatic.mp4" poster="c{n:02d}/{first[:-4]}.jpg" controls playsinline preload="none"></video>' if first else ''
    byid = {s.get('id'): s for s in shots}
    tiles = ''
    for f in frames:
        s = byid.get(f[:-4].split('_')[0], {})
        t = f"{s.get('t0', '')}-{s.get('t1', '')} s" if s else ''
        tiles += (f'<figure class="sf"><a href="c{n:02d}/{f[:-4]}.jpg" target="_blank"><img src="c{n:02d}/{f[:-4]}.jpg" loading="lazy" alt=""></a>'
                  f'<figcaption><b>{e(f[:-4])}</b> <span class="tc">{e(t)}</span> <span class="ty">{e(s.get("type", ""))}</span><br>{e(s.get("picture", ""))}'
                  + (f'<br><i>Motion:</i> {e(s.get("motion", ""))}' if s.get('motion') else '') + '</figcaption></figure>')
    plan = md(open(f'{d}/PLAN.md').read()) if os.path.exists(f'{d}/PLAN.md') else ''
    lp = LPS[c['lp']]
    script = ''.join(f'<div class="line"><div class="who">{e(w)}<small>{a}-{b} s</small></div><p>{e(t)}</p></div>' for w, a, b, t, _ in c['script'])
    nav.append(f'<a href="#c{n:02d}">{n:02d} {e(c["title"])}</a>')
    sections.append(f'''
<section id="c{n:02d}" class="sb">
  <div class="kicker">{e(lp['name'])} · {c['length']} s</div><h2>{n:02d} · {e(c['title'])}</h2>
  <p class="lede">{e(c['logline'])}</p>
  <div class="sbtop"><div class="anim">{anim}<p class="note">Animatic: style frames on the planned timing with scratch narration. Final voices are native audio from the generated takes; final motion is fully animated.</p></div>
  <div><h4>Locked script</h4><div class="script">{script}</div></div></div>
  <h4>Style frames</h4><div class="frames">{tiles}</div>
  <details><summary>Production plan (units, prompts, graphics, cost)</summary><div class="plan">{plan}</div></details>
</section>''')

cast_html = ''
for key, name, used, note in CAST:
    src = f'{SB}/cast/{key}_sheet.png'
    if os.path.exists(src):
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '80', '-Z', '1400', src, '--out', f'{OUT}/cast_{key}.jpg'], capture_output=True)
        cast_html += f'<figure><img src="cast_{key}.jpg" loading="lazy" alt="{e(name)}"><figcaption><b>{e(name)}</b> · concept {e(used)} · {e(note)}</figcaption></figure>'
for key in ('coldbrew_pack', 'proteinbar_pack'):
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '82', '-Z', '700', f'{SB}/cast/{key}.png', '--out', f'{OUT}/{key}.jpg'], capture_output=True)

extra_css = '''
.sb{border-top:1px solid var(--line);padding-top:10px}
.sbtop{display:grid;grid-template-columns:360px 1fr;gap:28px;align-items:start}
@media (max-width:860px){.sbtop{grid-template-columns:1fr}}
.anim .note{font-size:13px;color:var(--mute)}
.frames{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
@media (max-width:1000px){.frames{grid-template-columns:repeat(3,1fr)}}@media (max-width:640px){.frames{grid-template-columns:repeat(2,1fr)}}
.sf img{aspect-ratio:9/16;object-fit:cover;border-radius:10px}
.sf figcaption{font-size:12.5px;line-height:1.45}.sf .tc{font:500 11px "JetBrains Mono",monospace;color:var(--forest)}.sf .ty{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--mute)}
.script{display:grid;gap:8px}.line{display:grid;grid-template-columns:150px 1fr;gap:12px;background:var(--soft);border-radius:12px;padding:10px 12px}
.line .who{font-weight:700;font-size:13px}.line .who small{display:block;font:500 11px "JetBrains Mono",monospace;color:var(--mute)}.line p{margin:0;font-size:15px}
@media (max-width:640px){.line{grid-template-columns:1fr}}
details{margin:18px 0;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 16px}summary{cursor:pointer;font-weight:700}
.plan pre{white-space:pre-wrap;background:var(--chip);padding:12px;border-radius:10px;font-size:12.5px}
.castg{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}@media (max-width:760px){.castg{grid-template-columns:1fr}}
'''
body = f'''
<nav class="top"><div class="wrap">{''.join(nav)}<a href="#cast">Cast</a><a href="#next">Next</a><a href="../v2/">Concepts v2</a></div></nav>
<div class="wrap">
<section class="hero"><div class="kicker">Ad Studio by Brevo · Meta video ads · storyboards · {{DATE}}</div>
<h1>Storyboards for 01, 03, 04, 05 and 08.</h1>
<p class="lede">Each concept has a timed animatic with scratch narration, a style frame for every shot, the locked script and the production plan. Every person comes from treg (Seedance 2.5, face-locked first frames, native audio); every screen is the real Ad Studio UI.</p>
<span class="status">Production underway: finals for review next</span></section>
{''.join(sections)}
<section id="cast"><h2>Cast and demo products</h2><p class="lede">Face-locked identity sheets used as references for every keyframe and every generated take. Simone and Arjun are the creators Ad Studio made for us.</p>
<div class="castg">{cast_html}</div>
<div class="grid g4" style="margin-top:16px"><figure><img src="coldbrew_pack.jpg" alt=""><figcaption>Northline cold brew (fictional, matches LP B’s demo)</figcaption></figure><figure><img src="proteinbar_pack.jpg" alt=""><figcaption>Fieldday protein bar (fictional)</figcaption></figure></div></section>
<section id="next"><h2>Production (running now)</h2><div class="card"><ol class="tldr">{{NEXT}}</ol></div></section>
<footer>Sources: <code>~/claude fc/brevo-ads-meta/storyboards/</code> (kit, cast, c01 to c08).</footer>
</div>'''
NEXT = ['Clean re-recordings of the real product flows in a fresh workspace (USD only), at 2x with click logs.',
        'Seedance 2.5 takes through treg for every on-camera unit (one take each, flaws listed for you; brand words verified on the vocal stem).',
        'Motion graphics built in HyperFrames from these frames: fully animated, 1080x1920, real UI replicas.',
        'Narration for 08, a composed music bed, sparse sound, assembly and QA, then the finals for your review.']
body = body.replace('{NEXT}', ''.join(f'<li>{e(x)}</li>' for x in NEXT)).replace('{DATE}', '27 Oct 2026')
shell = open('shell.html').read().replace('</style>', extra_css + '</style>').replace('<title>Ad Studio Meta Ads</title>', '<title>Ad Studio Storyboards</title>')
page = shell.replace('{{BODY}}', body)
page = page.replace('href="c', 'href="c')
for bad in ('—', '–'):
    page = page.replace(bad, ', ')
open(f'{OUT}/index.html', 'w').write(page)
print(f'{OUT}/index.html', len(page) // 1024, 'KB;', len(sections), 'concepts')
