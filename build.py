"""Renders index.html for the Ad Studio Meta video ads report. usage: python3 build.py"""
import html, json, os
from concepts import CONCEPTS, SCORE_KEYS, FIRST_BATCH

e = html.escape
REFS = json.load(open('/Users/farooq.chisty/claude fc/brevo-ads-meta/refs/more/REFERENCES.json'))
IG = 'https://www.instagram.com/reel/'

def vid(src, poster, cls='wide'):
    return f'<video class="{cls}" src="{src}" poster="{poster}" controls playsinline preload="none"></video>'

def tags(fs):
    return ''.join(f'<span class="tag t-{f.split()[0].lower()}">{e(f)}</span>' for f in fs)

def concept_card(c):
    total = sum(c['score'])
    first = c['n'] in FIRST_BATCH
    beats = ''.join(f'<tr><td class="tc">{e(t)} s</td><td>{e(v)}</td><td>{e(s)}</td></tr>' for t, v, s in c['beats'])
    refs = ' · '.join(f'<a href="{IG}{code}/" target="_blank" rel="noopener">{e(code)}</a> ({e(why)})' for code, why in c['refs'])
    sc = ''.join(f'<span>{e(k)} <b>{v}</b></span>' for k, v in zip(SCORE_KEYS, c['score']))
    hv, ht, hs = c['hook']
    return f'''
<article class="concept{' first' if first else ''}" id="c{c['n']}">
  <header><div class="cn">{c['n']:02d}</div><div><h3>{e(c['title'])}</h3>
  <div class="meta">{tags(c['feature'])}<span class="fmt">{e(c['fmt'])}</span><span class="len">{e(c['length'])}</span>{'<span class="pick">First batch</span>' if first else ''}</div></div>
  <div class="score" title="Sum of 6 scores out of 60"><b>{total}</b>/60</div></header>
  <p class="idea">{e(c['idea'])}</p>
  <div class="hook"><div><h5>Hook, first 3 s</h5><p>{e(hv)}</p></div><div><h5>On screen</h5><p class="big">{e(ht)}</p></div><div><h5>Spoken</h5><p>“{e(hs)}”</p></div></div>
  <div class="tbl"><table><thead><tr><th>Time</th><th>What we see</th><th>What is said / shown</th></tr></thead><tbody>{beats}</tbody></table></div>
  <dl class="prod"><dt>Product footage</dt><dd>{e(c['product'])}</dd><dt>AI footage</dt><dd>{e(c['ai'])}</dd><dt>Watch out</dt><dd>{e(c['watch'])}</dd><dt>Modeled on</dt><dd>{refs}</dd></dl>
  <div class="scores">{sc}</div>
</article>'''

ranked = sorted(CONCEPTS, key=lambda c: -sum(c['score']))
rank_rows = ''.join(f'<tr><td><a href="#c{c["n"]}">{c["n"]:02d} {e(c["title"])}</a></td><td>{" / ".join(c["feature"])}</td><td>{e(c["length"])}</td>' + ''.join(f'<td>{v}</td>' for v in c['score']) + f'<td><b>{sum(c["score"])}</b></td></tr>' for c in ranked)

picks = REFS['picks']
ref_rows = ''
for p in picks:
    img = f'media/refs/more_{p["shortcode"]}.jpg'
    thumb = f'<img src="{img}" alt="" loading="lazy">' if os.path.exists(img) else ''
    ref_rows += f'<tr><td class="rt">{thumb}</td><td><a href="{p["url"]}" target="_blank" rel="noopener">@{e(p["handle"])}</a><br><small>{p["plays"]:,} plays · {p.get("multiple_vs_median") or ""}x median</small></td><td>{e(p["family_label"] if p.get("family_label") else p["family"])}</td><td>{e((p.get("hook") or "")[:150])}</td><td>{e(p.get("brevo_feature") or "")}</td></tr>'
patterns = ''.join(f'<li><b>{e(x["name"])}</b>: <a href="{x["best"]}" target="_blank" rel="noopener">best example</a></li>' for x in REFS['patterns'])

import re
body = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), open('body.html').read())
J = 'media/journeys/'
for i, n in enumerate(['01_paste_link_to_5_ads', '02_radar_to_clone_static', '03_ai_influencer_testimonial', '04_radar_to_clone_ugc_video'], 1):
    body = body.replace(f'<div>VIDEO{i}</div>', f'<div>{vid(J + n + ".mp4", J + n + "_poster.jpg")}</div>')
O = 'media/outputs/'
body = body.replace('<figure>VIDS</figure>', f'<figure>{vid(O + "glowday_simone_testimonial.mp4", O + "glowday_simone_testimonial_poster.jpg", "tall")}<figcaption>Simone for Glowday, 720p, 14 s</figcaption></figure>')
body = body.replace('<figure>VIDA</figure>', f'<figure>{vid(O + "drift_arjun_commentreply.mp4", O + "drift_arjun_commentreply_poster.jpg", "tall")}<figcaption>Arjun for Drift, cloned from a 9-month ad, 480p, 15 s</figcaption></figure>')
body = body.replace('{{CONCEPTS}}', ''.join(concept_card(c) for c in CONCEPTS)).replace('{{RANK_ROWS}}', rank_rows).replace('{{REF_ROWS}}', ref_rows).replace('{{PATTERNS}}', patterns)
page = open('shell.html').read().replace('{{BODY}}', body)
for bad in ('—', '–'):
    assert bad not in page, f'dash {bad!r} found'
open('index.html', 'w').write(page)
print('index.html', len(page) // 1024, 'KB')
