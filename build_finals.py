"""Renders finals/index.html from production/c<NN>/final/*_share.mp4 + NOTES.md. usage: python3 build_finals.py"""
import glob, html, os, re, shutil, subprocess
from concepts_v2 import CONCEPTS, LPS
from mdlite import md

e = html.escape
PROD = '/Users/farooq.chisty/claude fc/brevo-ads-meta/production'
OUT = 'finals'
PICKS = [1, 3, 4, 5, 8]
os.makedirs(OUT, exist_ok=True)
cards, rows = [], []
for c in [c for c in CONCEPTS if c['n'] in PICKS]:
    n = c['n']; d = f'{PROD}/c{n:02d}'
    shares = sorted(glob.glob(f'{d}/final/*_share.mp4')) or sorted(glob.glob(f'{d}/final/*.mp4'))
    lp = LPS[c['lp']]
    if not shares:
        cards.append(f'<article class="concept" id="c{n:02d}"><h3>{n:02d} · {e(c["title"])}</h3><p class="obs">Not finished yet.</p></article>')
        continue
    src = shares[-1]; dst = f'{OUT}/c{n:02d}.mp4'
    shutil.copy(src, dst)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '1.5', '-i', dst, '-frames:v', '1', '-vf', 'scale=540:-2', f'{OUT}/c{n:02d}.jpg'])
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', dst]))
    notes = md(open(f'{d}/NOTES.md').read()) if os.path.exists(f'{d}/NOTES.md') else ''
    rows.append(f'<tr><td><a href="#c{n:02d}">{n:02d} {e(c["title"])}</a></td><td>{e(lp["name"])}</td><td>{dur:.1f} s</td></tr>')
    cards.append(f'''
<article class="concept" id="c{n:02d}">
  <div class="fin"><div><video class="tall" src="c{n:02d}.mp4" poster="c{n:02d}.jpg" controls playsinline preload="metadata"></video>
  <p><a href="c{n:02d}.mp4" download>Download</a> · {dur:.1f} s · 1080x1920</p></div>
  <div><div class="kicker">{e(lp['name'])}</div><h3>{n:02d} · {e(c['title'])}</h3><p class="idea">{e(c['logline'])}</p>
  <p>Lands on <a href="{lp['url']}" target="_blank" rel="noopener">{e(lp['url'])}</a>. Storyboard: <a href="../storyboards/#c{n:02d}">open</a>.</p>
  <details open><summary>Production notes, checks and flaws</summary><div class="plan">{notes}</div></details></div></div>
</article>''')

extra_css = '''
.fin{display:grid;grid-template-columns:380px 1fr;gap:28px;align-items:start}@media (max-width:860px){.fin{grid-template-columns:1fr}}
details{margin:14px 0;background:var(--soft);border-radius:14px;padding:12px 16px}summary{cursor:pointer;font-weight:700}
.plan{font-size:14.5px}.plan pre{white-space:pre-wrap;background:var(--chip);padding:12px;border-radius:10px;font-size:12.5px}
'''
body = f'''
<nav class="top"><div class="wrap">{''.join(f'<a href="#c{n:02d}">{n:02d}</a>' for n in PICKS)}<a href="../storyboards/">Storyboards</a><a href="../v2/">Concepts v2</a></div></nav>
<div class="wrap">
<section class="hero"><div class="kicker">Ad Studio by Brevo · Meta video ads · finals v1</div>
<h1>Five finished ads for your review.</h1>
<p class="lede">Each one is 1080x1920 for Reels, built from the approved storyboard: on-camera people from Seedance 2.5 with native audio, the real Ad Studio UI, and fully animated motion graphics. Every flaw we noticed is listed under its video for you to judge.</p>
<span class="status">Waiting on you: review the five cuts</span></section>
<div class="tbl"><table><thead><tr><th>Ad</th><th>Lands on</th><th>Length</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
{''.join(cards)}
<footer>Masters, takes and ledgers: <code>~/claude fc/brevo-ads-meta/production/</code>.</footer>
</div>'''
shell = open('shell.html').read().replace('</style>', extra_css + '</style>').replace('<title>Ad Studio Meta Ads</title>', '<title>Ad Studio Finals</title>')
page = shell.replace('{{BODY}}', body)
for bad in ('—', '–'):
    page = page.replace(bad, ', ')
open(f'{OUT}/index.html', 'w').write(page)
print(f'{OUT}/index.html', len(rows), 'finals')
