"""Renders cinematic/index.html: round 3, ten fresh cinematic concepts. usage: python3 build_cinematic.py"""
import html, os, subprocess
from concepts_cine import CINE, FIRST
from concepts_v2 import LPS

e = html.escape
KEYS = ['Relevance', 'Scroll-stop', 'Virality', 'Creativity', 'Catchiness', 'Uniqueness']
TAG = {'Radar': 't-radar', 'Clone': 't-clone', 'AI influencers': 't-ai', 'Ads Agent': 't-ai', 'Static ads': 't-static'}
for c in CINE:
    src = f'cinematic/hook_{c["n"]}.png'
    if os.path.exists(src):
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '84', '-Z', '1400', src, '--out', f'cinematic/hook_{c["n"]}.jpg'], capture_output=True)

cards = ''
for c in CINE:
    lp = LPS[c['lp']]; tot = sum(c['score']); first = c['n'] in FIRST
    beats = ''.join(f'<tr><td class="tc">{e(t)} s</td><td><b>{e(b)}</b><br>{e(p)}</td><td>{e(l)}</td></tr>' for b, t, p, l in c['beats'])
    tags = ''.join(f'<span class="tag {TAG.get(f, "t-static")}">{e(f)}</span>' for f in c['feature'])
    sc = ''.join(f'<span>{e(k)} <b>{v}</b></span>' for k, v in zip(KEYS, c['score']))
    cards += f'''
<article class="concept{' first' if first else ''}" id="c{c['n']}">
 <div class="cine">
  <figure><img src="hook_{c['n']}.jpg" alt="Hook frame for {e(c['title'])}"><figcaption>Hook frame (concept art, first 3 s)</figcaption></figure>
  <div>
   <header><div class="cn">{c['n']}</div><div><h3>{e(c['title'])}</h3>
   <div class="meta"><span class="lp lp{c['lp']}">{e(lp['name'])}</span>{tags}<span class="fmt">{e(c['genre'])}</span><span class="len">{c['length']} s</span>{'<span class="pick">My pick</span>' if first else ''}</div></div>
   <div class="score"><b>{tot}</b>/60</div></header>
   <p class="idea">{e(c['logline'])}</p>
   <div class="hook"><div><h5>First 3 seconds</h5><p>{e(c['hook_pic'])}</p></div><div><h5>First line</h5><p class="big">“{e(c['hook_line'])}”</p></div><div><h5>Why it stops the scroll</h5><p>{e(c['why_stop'])}</p></div></div>
  </div>
 </div>
 <div class="tbl"><table><thead><tr><th>Time</th><th>Beat and picture</th><th>Key lines</th></tr></thead><tbody>{beats}</tbody></table></div>
 <dl class="prod"><dt>Cast and places</dt><dd>{e(c['cast'])}</dd><dt>How it proves the product</dt><dd>{e(c['proof'])}</dd><dt>Devices</dt><dd>{e(c['devices'])}</dd><dt>Why it can travel</dt><dd>{e(c['viral'])}</dd><dt>Risks</dt><dd>{e(c['risks'])}</dd><dt>Est. cost</dt><dd>About ${c['cost']} at 1080p (Seedance via treg), plus a few cents of keyframes and about $0.50 of music.</dd><dt>Lands on</dt><dd><a href="{lp['url']}" target="_blank" rel="noopener">{e(lp['url'])}</a>: “{e(lp['hero'])}”</dd></dl>
 <div class="scores">{sc}</div>
</article>'''

rank = sorted(CINE, key=lambda c: -sum(c['score']))
rows = ''.join(f'<tr><td><a href="#c{c["n"]}">{c["n"]} {e(c["title"])}</a></td><td>{e(c["genre"])}</td><td>{e(LPS[c["lp"]]["name"])}</td>' + ''.join(f'<td>{v}</td>' for v in c['score']) + f'<td><b>{sum(c["score"])}</b></td><td>${c["cost"]}</td></tr>' for c in rank)
extra = '''
.lp{font-size:12px;font-weight:800;padding:3px 10px;border-radius:999px;color:#fff}.lpA{background:#1D5FA8}.lpB{background:#6B2BB5}
.cine{display:grid;grid-template-columns:300px 1fr;gap:24px;align-items:start}@media (max-width:820px){.cine{grid-template-columns:1fr}}
.cine figure img{aspect-ratio:9/16;object-fit:cover;border-radius:14px}
.cine .hook{grid-template-columns:1fr}
.cine .hook p.big{font-size:18px}
'''
body = f'''
<nav class="top"><div class="wrap"><a href="#how">How I thought</a>{''.join(f'<a href="#c{c["n"]}">{c["n"]}</a>' for c in CINE)}<a href="#rank">Ranking</a><a href="../v2/">Concepts v2</a><a href="../storyboards/">Storyboards</a></div></nav>
<div class="wrap">
<section class="hero"><div class="kicker">Ad Studio by Brevo · Meta video ads · round 3 · cinematic</div>
<h1>Ten fresh cinematic concepts, each built around a first frame people stop on.</h1>
<p class="lede">No borrowed formats this time. Each concept is its own small film (a nature documentary, an autopsy, a heist, a draft night) where the story itself proves one thing the product really does. Every spoken line keeps the calm, explanatory register; every product moment uses the real Ad Studio UI; every person is generated with native audio and a natural grade.</p>
<span class="status">Waiting on you: pick five</span></section>
<section id="how"><h2>How I approached it</h2><div class="card"><ul class="tldr">
<li><b>A frame you cannot scroll past.</b> Each hook is an image that should not exist (a flock of ads, an ad in a tank, an ad on an autopsy table) paired with one line that makes you need the next sentence.</li>
<li><b>The genre does the explaining.</b> Documentaries, forensic dramas and broadcasts already have a calm narrator who explains, so the professor register feels native instead of salesy.</li>
<li><b>The twist is the product.</b> In every concept the turn of the story is a real feature: the survivors are what Ad Radar finds, the skeleton is what Clone keeps, the draft picks are the agent’s casting, "it was never locked" is why Radar matters.</li>
<li><b>Built to be shared.</b> Each has one quotable line ("Time of death: day eleven", "There is no salary cap", "I already did") and a reason to rewatch.</li>
<li><b>Balanced across your two test pages:</b> 11 to 15 lead to Winners (Ad Radar and Clone), 16 to 20 lead to the Agent page (AI creators and the agent). Production of the current five is running in the background and is not affected.</li>
</ul></div></section>
<section id="concepts"><h2>The ten concepts</h2>{cards}</section>
<section id="rank"><h2>Ranking</h2><div class="tbl"><table><thead><tr><th>Concept</th><th>Genre</th><th>Lands on</th><th>Rel</th><th>Stop</th><th>Viral</th><th>Creat</th><th>Catch</th><th>Uniq</th><th>Total</th><th>Cost</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="callout">My five, balancing virality with how reliably each can be produced: <b>11 Planet Ads</b>, <b>12 Ad Autopsy</b>, <b>16 Creator Draft Day</b>, <b>17 Spot the AI</b>, <b>20 The Interview</b>. If you want more spectacle, swap 20 for <b>13 Specimen 730</b> or <b>18 The Mirror Hallway</b>.</p></section>
<footer>Hook frames are concept art from Nano Banana Pro via treg; final shots come from the storyboard stage. Glowday is a fictional demo brand.</footer>
</div>'''
shell = open('shell.html').read().replace('</style>', extra + '</style>').replace('<title>Ad Studio Meta Ads</title>', '<title>Ad Studio Cinematic Concepts</title>')
page = shell.replace('{{BODY}}', body)
for bad in ('—', '–'):
    assert bad not in page, bad
open('cinematic/index.html', 'w').write(page)
print('cinematic/index.html', len(page) // 1024, 'KB')
